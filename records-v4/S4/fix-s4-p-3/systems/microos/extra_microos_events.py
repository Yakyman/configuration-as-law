"""Additional source and current-use records; no historical actor inference."""
from main import write_tsv
from microos_event_queries import queries

def collect(ctx):
    if ctx.meta.get('system') != 'microos':
        return
    rows = []
    shared = [
        ('all', 'structured-journal', 'journalctl --no-pager --all -o json\n'),
        ('all', 'installation-records', "find /var/log/zypp /var/log/YaST2 -type f -printf 'SOURCE %p %s\\n' -exec grep -aEn 'NetworkManager|jeos-firstboot|mdcheck_continue|network.service|sudoers|visudo|grubenv|editenv|saved_entry|next_entry|ca-certificates|p11-kit|trust anchor' {} +\n")]
    for fact, route, script in queries():
        if route == 'audit':
            shared.append((fact, route, script))
        elif fact == 'M14' and route == 'installation-current':
            shared.append((fact, 'current-trust-use', script[script.index('command -v trust'):]))
    for fact, route, script in shared:
        data, rc, evidence = ctx.query('s4-microos-'+route, script, 120)
        rows.append([fact, route, rc, evidence, 'unknown:historical-chooser-not-established', 'bounded-current-snapshot' if route == 'current-trust-use' else 'retained-source-query'])
    write_tsv(ctx.out/'s4-microos-event-routes.tsv', ['fact_id','route','query_exit','evidence','historical_chooser','scope'], rows)
