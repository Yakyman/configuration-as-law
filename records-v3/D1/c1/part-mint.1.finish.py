import csv,json
from pathlib import Path
rows=[r for r in csv.DictReader(open('D1/in/part-mint.tsv'),delimiter='\t') if r['kind']=='L1:package:dpkg-query'][:635]
s=json.load(open('D1/c1/part-mint.1.sources.json'));fl=json.load(open('D1/c1/part-mint.1.filelists.json'))
p=Path('D1/c1/part-mint.1.tsv');done={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')}
choices={}
def choose(i,d,ids,what,why,filelist=False):
 n=rows[i]['name'].split(':')[1];url=fl[n]['url'] if filelist else s[n]['url'];choices[i]=[d,ids,what,'doc:'+url,why]
# Individually assessed cases.
for i in [22,33,57,62,176,178,179,183,369,380,392]:
 choose(i,'MUST','S2.2-9',' '.join(s[rows[i]['name'].split(':')[1]]['description'].split()[:15]),'The documented executable function makes this a program required by the explicit program clause.')
for i,what,why in [
(6,'Configures kernel sound drivers','Driver configuration controls hardware availability across programs; removal changes system audio behavior.'),
(7,'Describes hardware audio topology','Hardware topology determines available audio routes, beyond the interface of any single application.'),
(8,'Defines hardware audio input/output routes','Hardware routing controls which sound inputs and outputs can be used across programs.'),
(61,'Supplies trusted certification authorities for secure connections','Removing trusted authorities prevents authentication of otherwise usable secure network connections across programs.'),
(74,'Defines shared desktop settings schemas and translations','Shared schemas establish settings across several applications; their effect is not confined to one program.'),
(98,'Defines scheduled process sets','Removing configuration necessary to define scheduled process sets prevents scheduled system behavior.'),
(102,'Integrates encrypted storage activation into early boot','Removing integration prevents early boot from activating encrypted storage through this mechanism.'),
(121,'Configures messaging between applications and user services','Its behavior spans applications and services; the exception for settings only inside one program does not apply.'),
(122,'Configures system messaging and creates its service account','System bus behavior spans services, and the package creates an account explicitly required to be recorded.'),
(123,'Enables shared user messaging sessions across logins','Removing this package changes documented session semantics and service sharing across login sessions.'),
(148,'Provides DNS root servers and DNSSEC trust anchors','Root server locations and trust anchors enable DNS resolution and validation across programs.'),
(164,'Provides data necessary for speech synthesis','The documented necessary synthesizer data enables speech generation; removing it disables this function.'),
(198,'Describes how to process jobs for supported printers','Printer descriptions control job processing and enable supported printer operation, beyond the availability of document content.'),
(319,'Defines schemas for desktop session settings','Desktop session settings affect multiple programs; removing their schemas prevents those settings from functioning.'),
(327,'Configures common container behavior across tools','These settings are shared by multiple container projects, outside the single-program settings exemption.'),
(328,'Provides shared container configuration and manuals','Shared container configuration affects multiple tools; documentation does not exempt the package’s behavioral configuration.'),
(339,'Excludes incompatible graphics devices from graphical boot handover','Its blacklist prevents black or corrupt boot displays on affected hardware; it changes boot behavior.'),
(343,'Defines settings shared across desktop components','Schemas govern shared desktop settings, not settings in force only inside one program.'),
(419,'Stores keyboard preferences shared by console and graphical sessions','Preferences affect console and graphical input across programs; the single-program exemption does not apply.'),
(425,'Makes partition mapping available during boot','Removing boot integration prevents activation of partitions by this boot mechanism.'),
(449,'Configures shared audio drivers','Audio driver profiles influence sound behavior across applications, beyond a single program.'),
(514,'Supplies headers and object files for compiling C programs','Removing development files prevents compiling and linking programs against the standard library.'),
(571,'Supplies files required to develop programs using cryptographic routines','Removing these development files prevents building applications against this library.')]:
 choose(i,'MUST','S2.2-1,S2.2-2',what,why)
for i,what in [(10,'Updates processor microcode and security firmware'),(181,'Provides firmware and topology needed by audio hardware')]:
 choose(i,'MUST','S2.2-2,S2.2-16',what,'Firmware changes device behavior; the documented update package establishes that software can change it.')
for i,what in [(32,'Provides base system hierarchy and shell startup configuration'),(35,'Executes shell routines to complete command lines'),(78,'Provides desktop session startup scripts and translations'),(162,'Provides shared executable support for editor packages'),(185,'Provides font configuration scripts and settings'),(550,'Provides unstripped executable runtime binaries for debugging'),(598,'Installs shell configuration code selecting a debug information server')]:
 choose(i,'MUST','S2.2-10,S2.2-13',what,'The package includes code executed with its executing program’s rights; data or settings alongside it do not exempt that code.')
for i in [547,583]:
 choose(i,'MUST','S2.2-10,S2.2-13',s[rows[i]['name'].split(':')[1]]['description'],'The documented runtime library executes within calling programs with their rights.')
for i,what,why in [
(25,'Supplies accessibility package documentation','The file list contains only copyright and changelog documents; no executable functionality is removed.'),
(214,'Supplies compiler package documentation','The file list contains documentation only; removing the package removes those documents, not compilation functionality.'),
(216,'Supplies compiler package documentation','The file list contains documentation only; removing the package removes those documents, not compilation functionality.'),
(469,'Supplies a database of service type names','The database supplies descriptive names; removal makes those database contents unavailable.'),
(557,'Supplies translations for the graphics library','The file list contains translations and documentation; removal removes those messages, not the graphics code.'),
(561,'Supplies translations for the graphics abstraction library','The file list contains translations and documentation; removal removes those messages, not the graphics code.'),
(613,'Supplies graphics hardware identification names','The hardware-name database and documentation are content; their removal removes names, not the graphics driver.')]:
 choose(i,'NOT','S2.2-4,S2.2-6',what,why,True)
for i,what,why in [
(69,'Provides desktop scripts, applets and support modules','The file list includes executable Python and JavaScript code, required independently of accompanying data.'),
(374,'Provides executable printing and scanning support scripts','The file list includes executable Python printing, scanning and setup modules, despite the data-package name.')]:
 choose(i,'MUST','S2.2-10,S2.2-13',what,why,True)
choose(167,'MUST','S2.2-1,S2.2-2','Defines activation of calendar and address book services','Service activation definitions enable separate service processes; their effect is not limited to one program.',True)
choose(318,'MUST','S2.2-1,S2.2-2','Triggers sound playback at session login and logout','The documented role is triggering sound events; removing it stops this session behavior.')
# Individual data and settings cases, with distinct roles explicitly stated.
for i,what in [(5,'Supplies desktop icon images'),(13,'Supplies application catalog information and icons'),(19,'Supplies icons and common client data'),(21,'Supplies package-manager data and translations'),(41,'Supplies binary-utility documentation and translations'),(71,'Supplies configuration applet icons, images and translations'),(75,'Supplies desktop translation text'),(80,'Supplies circular flag images'),(141,'Supplies distribution release information'),(147,'Supplies cursor images'),(180,'Supplies browser language text'),(224,'Supplies geographical library icons'),(225,'Supplies geographical country database contents'),(303,'Supplies network extension data and translations'),(305,'Supplies high contrast theme images and values'),(308,'Supplies desktop translation text'),(322,'Supplies terminal help, translations and local appearance data'),(324,'Supplies desktop theme data'),(362,'Supplies filesystem component data and translations'),(371,'Supplies fallback icon theme information'),(376,'Supplies desktop icon themes'),(389,'Supplies organizational identifier listings'),(412,'Supplies DHCP manual pages'),(413,'Supplies standardized codes and their translated names'),(414,'Supplies country flag images'),(426,'Supplies authentication library translated messages'),(427,'Supplies updated English translation messages'),(428,'Supplies English translation messages'),(429,'Supplies updated English desktop translation messages'),(430,'Supplies English desktop translation messages'),(507,'Supplies byte-size library translated messages')]:
 choose(i,'NOT','S2.2-4',what,'Only supplied text, images or descriptive data become unavailable; the programs retain their executable capabilities.')
choose(49,'NOT','S2.2-4,S2.2-7','Supplies disc-burning application help, translations and settings','Its documented files are application content and settings confined to the disc-burning application.',True)
choose(440,'HOLE','S2.2-1,S2.2-7','Configures an audio output library shared by applications','The text does not say whether shared-library settings count as inside one program or across its calling programs.')
choose(465,'HOLE','S2.2-1,S2.2-7','Configures the security auditing library','The text does not determine whether a library’s configuration is confined to one program when many programs load it.')
choose(531,'HOLE','S2.2-2,S2.2-4,S2.2-7','Supplies keyboard layouts for an on-screen input system','Layouts can be treated as content or internal settings, or as capabilities to enter characters; the text does not separate these readings.',True)
for i,what in [(24,'Supplies English spell-checking dictionaries'),(83,'Supplies color profiles and calibration reference data'),(87,'Supplies console fonts and character maps'),(107,'Supplies printer driver description definitions'),(115,'Supplies printer server web pages and administrative templates'),(132,'Supplies translated templates and multibyte display support'),(150,'Defines the structure used to validate document formats'),(377,'Supplies English spell-checking words and morphology'),(378,'Supplies hardware identification and configuration databases'),(379,'Supplies English hyphenation patterns'),(383,'Supplies input method schemas, dictionaries and keyboard maps'),(577,'Supplies printing character sets and banner templates'),(605,'Supplies translated messages and document structure definitions')]:
 choose(i,'HOLE','S2.2-2,S2.2-4',what,'Removal loses the supplied data, but also its specific processing or presentation capability; the text does not distinguish these readings.',i in [83,107,115,383,605])
for i,what in [(44,'Selects Bluetooth support packages through dependencies'),(55,'Lists and selects packages required for software builds'),(201,'Transitions package selection to the replacement file-transfer client'),(395,'Ensures selection of an installed initialization system')]:
 choose(i,'HOLE','S2.2-1,S2.2-2,S2.2-4',what,'The text does not specify whether removing a dependency-only package includes its selected dependencies or only its otherwise inert package record.')
for i,what in [(72,'Supplies desktop control-center debugging symbols'),(73,'Supplies desktop debugging symbols'),(513,'Supplies C runtime debugging symbols'),(546,'Supplies desktop library debugging symbols'),(549,'Supplies menu library debugging symbols'),(582,'Supplies audio abstraction debugging symbols')]:
 choose(i,'HOLE','S2.2-2,S2.2-4',what,'Symbols can be unavailable content or a lost capability for symbolic debugging; the text gives no boundary between these readings.')
# Homogeneous rules: fonts and runtime introspection, each audited on ten rows in notes.
for i in range(186,198):
 choose(i,'HOLE','S2.2-2,S2.2-4','Supplies glyph shapes and font metrics for displaying text','Fonts can be unavailable graphical content or lost character-rendering capabilities; the text does not distinguish these readings.')
for i in range(229,301):
 choose(i,'MUST','S2.2-1,S2.2-2','Provides runtime metadata enabling language bindings to call native library APIs','Removing runtime introspection metadata prevents language bindings from exposing the documented native API; this is functional interface information, not displayed content.')
with p.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 for i in sorted(choices):
  if rows[i]['id'] not in done:w.writerow([rows[i]['id']]+choices[i]);f.flush()
remaining=[(i,r['name']) for i,r in enumerate(rows) if r['id'] not in {r['id'] for r in csv.DictReader(p.open(),delimiter='\t')}]
print('Remaining',remaining)
