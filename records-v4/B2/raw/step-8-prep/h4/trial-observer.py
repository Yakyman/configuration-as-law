def collect():
    import pathlib, subprocess
    return {'preparation_only': True,
            'boot_id': pathlib.Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
            'last_success': pathlib.Path('/var/lib/stand/last-success.json').read_text(),
            'worker_stat': subprocess.run(['stat','/opt/stand/pkgs/dev-worker/bin/worker'],capture_output=True,text=True).stdout}
