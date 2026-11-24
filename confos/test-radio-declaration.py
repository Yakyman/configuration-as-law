#!/usr/bin/python3
"""Pure draft tests: no native commands, network, boot or production imports."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import radio_declaration as radio

KEY='00010203040506070809000102030405'
INFO=('[General]\nName=BlueZ 5.82\nClass=0x400000\nSupportedTechnologies=BR/EDR;\n'
      'Trusted=false\nBlocked=false\n\n[LinkKey]\nKey='+KEY+'\nType=5\nPINLength=0\n').encode()

class TestRadio(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.ap={'ssid_hex':b'ConfOS-radio-fixture'.hex(),'psk':'12'*32,'address':'192.0.2.1/24','channel':1}
        self.fixture={'format':1,'wifi':self.ap,'bluetooth':True}
        self.network={'format':1,'fixture':'lab','ssid_hex':self.ap['ssid_hex'],'psk':self.ap['psk'],'address':'192.0.2.2/24'}
    def row(self,kind,name,obj):
        data=json.dumps(obj).encode() if isinstance(obj,dict) else obj
        digest=hashlib.sha256(data).hexdigest()
        (self.root/digest).write_bytes(data)
        return f'{kind} {name} {digest} {digest}'
    def rows(self):
        a,b=radio.ADAPTERS
        return [self.row('radio-fixture','lab',self.fixture),self.row('network','saved',self.network),
                self.row('bluetooth-pair',a+' '+b,INFO),self.row('bluetooth-pair',b+' '+a,INFO)]
    def derive(self,rows):
        return radio.derive('\n'.join(rows),self.root)
    def test_order_and_independent_input_roots(self):
        rows=self.rows(); initial=self.derive(rows)
        self.assertEqual(initial,self.derive(list(reversed(rows))))
        with tempfile.TemporaryDirectory() as elsewhere:
            for source in self.root.iterdir():
                (Path(elsewhere)/source.name).write_bytes(source.read_bytes())
            self.assertEqual(initial,radio.derive('\n'.join(rows),elsewhere))
        self.assertIn(b'ssid=436f6e664f532d726164696f2d66697874757265',initial['files'][radio.PREFIX+'/wpa.conf']['data'])
        self.assertEqual(initial['files'][radio.PREFIX+'/bluez/'+radio.ADAPTERS[0]+'/'+radio.ADAPTERS[1]+'/info']['data'],INFO)
        self.assertTrue(all(f['mode']==0o600 and f['uid']==f['gid']==0 for f in initial['files'].values()))
    def test_removal_ownership(self):
        rows=self.rows()
        result=self.derive([rows[0],rows[3]])
        self.assertNotIn(radio.PREFIX+'/wpa.conf',result['files'])
        self.assertEqual(len(result['plan']['bonds']),1)
        self.assertNotIn(radio.PREFIX+'/bluez/'+radio.ADAPTERS[0]+'/'+radio.ADAPTERS[1]+'/info',result['files'])
        self.assertIn(radio.PREFIX+'/hostapd.conf',result['files'])
        empty=self.derive([])
        self.assertEqual(empty['required_packages'],{})
        self.assertEqual(len(empty['files']),1)
    def test_duplicates_and_unknown_rows(self):
        rows=self.rows()
        for bad in (rows+[rows[1]],['radio-unknown x'],[rows[0].replace('lab','bad/name')]):
            with self.assertRaises(ValueError): self.derive(bad)
    def test_hash_paths_and_symlink(self):
        rows=self.rows(); fields=rows[0].split(); original=self.root/fields[-1]
        original.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'checksum'): self.derive(rows)
        for name in ('../secret','/etc/passwd'):
            with self.assertRaises(ValueError): radio.read_input(self.root,fields[-2],name)
        (self.root/'link').symlink_to(original)
        with self.assertRaisesRegex(ValueError,'symlink'): radio.read_input(self.root,fields[-2],'link')
    def test_input_schema(self):
        for malformed in ({**self.fixture,'extra':True},{**self.fixture,'format':True},
                          {**self.fixture,'wifi':{**self.ap,'channel':True}},
                          {**self.fixture,'wifi':{**self.ap,'ssid_hex':'aa\npsk=oops'}},
                          b'{"format":1,"format":1,"wifi":null,"bluetooth":false}'):
            with self.assertRaises(ValueError): self.derive([self.row('radio-fixture','lab',malformed)])
    def test_network_invariants(self):
        fixture=self.row('radio-fixture','lab',self.fixture)
        for delta in ({'fixture':'absent'},{'psk':'ff'*32},{'address':'192.0.2.1/24'},
                      {'address':'192.0.3.2/24'},{'address':'192.0.2.0/24'}):
            with self.assertRaises(ValueError):
                self.derive([fixture,self.row('network','saved',{**self.network,**delta})])
    def test_bond_validation(self):
        for malformed in (INFO.replace(b'Type=5',b'Type=4'),INFO.replace(b'BR/EDR;',b'LE;'),
                          INFO+b'\n[Unknown]\nKey=x\n',INFO.replace(b'Key=',b'Other='),
                          INFO+b'\n[DEFAULT]\nHidden=true\n'):
            with self.assertRaises(ValueError): radio.bond(malformed)
        rows=self.rows()
        a,b=radio.ADAPTERS
        rows[-1]=self.row('bluetooth-pair',b+' '+a,INFO.replace(KEY.encode(),b'ff'*16))
        with self.assertRaisesRegex(ValueError,'keys differ'): self.derive(rows)
        with self.assertRaisesRegex(ValueError,'requires declared'): self.derive([rows[2]])

if __name__=='__main__': unittest.main(verbosity=2)
