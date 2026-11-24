"""Specialize immutable Flatpak child policy with declared executable paths."""
from pathlib import Path

def render(root, executables):
    template = (Path(root)/'usr/lib/confos/flatpak-profile.apparmor').read_text()
    marker = '  # DECLARED_EXECUTABLES\n'
    assert template.count(marker) == 1
    lines = []
    for path in sorted(executables):
        # Flatpak runtime /usr and application /app are immutable inside its sandbox.
        # Other exposed program paths must come from the assembled declaration.
        if path.startswith(('/usr/', '/app/')): continue
        if '"' in path or '\n' in path: raise ValueError('unsupported executable pathname')
        escaped = ''.join('\\'+c if c in '\\[]{}*?^' else c for c in path)
        lines.append('  "'+escaped+'" mrix,\n')
    import flatpak_readers
    return template.replace(marker, flatpak_readers.policy(root)+''.join(lines))
