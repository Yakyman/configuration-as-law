#!/usr/bin/env python3
"""Member-level rules for stored groups under the home trees of part-developer (classification c2).

classify(member) -> (decision, label)
The rules are stated in A3/c2/part-developer.notes.md. Every rule follows from the cited sentences.
"""
import os, re

# End of the installing action for each package tree (mtime of the action log, operator record).
END = {
    'julia': '2026-11-23T11:13:59.999',
    'tools': '2026-11-23T11:14:05.999',   # bun add -g, gem install, uv tool install (developer_global_tools)
    'brew': '2026-11-23T11:15:23.999',
}

# Interpreters/runtimes installed on this machine (rpm list raw/0013, action logs):
# bash/sh, python3, perl, tcl, ruby, java (source launcher), go (go run), gawk, make, docker, julia, bun.
CODE_EXT = {
    '.sh', '.bash', '.py', '.pyw', '.pl', '.pm', '.tcl', '.rb', '.rake', '.gemspec', '.ru', '.java', '.go',
    '.jl', '.js', '.mjs', '.cjs', '.ts', '.mts', '.cts', '.jsx', '.tsx', '.awk', '.mk', '.so',
}
CODE_NAMES = {'activate', 'Makefile', 'makefile', 'GNUmakefile', 'Dockerfile', 'Rakefile', 'Gemfile', 'Brewfile',
              'Containerfile'}
NONCODE_SUFFIX = ('.d.ts', '.d.mts', '.d.cts', '.map')
FOREIGN = re.compile(r'(darwin|windows|freebsd|openbsd|netbsd|arm64|aarch64|\.exe$|\.dll$|\.dylib$|\.bat$|\.cmd$|\.ps1$)', re.I)


def ext_of(path):
    b = os.path.basename(path)
    if '.' not in b.lstrip('.'):
        return ''
    return '.' + b.rsplit('.', 1)[1].lower()


GOOS = {'aix', 'android', 'darwin', 'dragonfly', 'freebsd', 'hurd', 'illumos', 'ios', 'js', 'linux', 'nacl', 'netbsd',
        'openbsd', 'plan9', 'solaris', 'wasip1', 'windows', 'zos'}
GOARCH = {'386', 'amd64', 'amd64p32', 'arm', 'armbe', 'arm64', 'arm64be', 'loong64', 'mips', 'mipsle', 'mips64',
          'mips64le', 'mips64p32', 'mips64p32le', 'ppc', 'ppc64', 'ppc64le', 'riscv', 'riscv64', 's390', 's390x',
          'sparc', 'sparc64', 'wasm'}


def go_builds_here(path):
    """File-name build constraints of go/build (https://pkg.go.dev/go/build#hdr-Build_Constraints):
    *_GOOS, *_GOARCH, *_GOOS_GOARCH (after stripping .go and _test). Here GOOS=linux, GOARCH=amd64.
    Packages golang.org/x/sys/windows and /plan9 build only for those systems (package documentation)."""
    if re.search(r'golang\.org/x/sys(@[^/]*)?/(windows|plan9)/', path):
        return False
    stem = os.path.basename(path)[:-3]
    if stem.endswith('_test'):
        stem = stem[:-5]
    parts = stem.split('_')
    if len(parts) >= 3 and parts[-2] in GOOS and parts[-1] in GOARCH:
        return parts[-2] == 'linux' and parts[-1] == 'amd64'
    if len(parts) >= 2:
        if parts[-1] in GOOS:
            return parts[-1] == 'linux'
        if parts[-1] in GOARCH:
            return parts[-1] == 'amd64'
    return True


TEXT_EXT = {'.md', '.txt', '.json', '.yml', '.yaml', '.toml', '.html', '.htm', '.css', '.png', '.jpg', '.jpeg',
            '.gif', '.svg', '.xml', '.csv', '.lock', '.rst', '.ini', '.cfg', '.gz', '.zip', '.tar', '.map'}

BASH_NAMES = {'.bashrc', '.bash_profile', '.bash_login', '.bash_logout', '.profile'}


def is_code_file(path, exe, typ):
    """Code that this computer can execute: on its own, at a person's command, or through another program."""
    b = os.path.basename(path)
    if b.endswith(NONCODE_SUFFIX):
        return False
    e = ext_of(path)
    if re.search(r'\.so(\.\d+)*$', b):
        return not FOREIGN.search(path)  # S8.2-20: a library for another system is not a program here
    if e == '.go' and not go_builds_here(path):
        return False  # S8.2-20: Go file excluded on linux/amd64 by its file-name build constraint
    if e in CODE_EXT or b in CODE_NAMES or b in BASH_NAMES:
        return True  # source run by an interpreter installed here, whatever directory it lies in
    if typ == 'file' and exe == 'True':
        if re.match(r'(LICEN[CS]E|COPYING|README|CHANGELOG|AUTHORS|NOTICE)', b, re.I) or e in TEXT_EXT:
            return False  # an executable bit does not make text or data into code
        return not FOREIGN.search(path)  # S8.2-20: binaries built for another OS/architecture
    return False


SHEBANG = set()


def load_shebang(rows):
    import json
    for x in rows:
        if x['kind'] == '2:code-ownership-unresolved':
            if json.loads(x['members']).get('shebang'):
                SHEBANG.add(x['name'])


def classify(m):
    r = _classify(m)
    if re.match(r'/home/user/\.bun/install/cache/[^/]*\.npm$', m['path']):
        # doc:https://github.com/oven-sh/bun/blob/main/src/install/npm.rs - header "#!/usr/bin/env bun\n
        # bun-npm-manifest-cache-v0.0.8\n" followed by a serialized manifest: data, not code.
        return ('RECORD', 'bun npm manifest cache: #! format header then serialized manifest data, not code')
    if r and m['path'] in SHEBANG and r[0] in ('RECORD', 'MATERIAL') and \
            not is_code_file(m['path'], m['exec'], m['type']):
        return ('UNKNOWN', 'file starts with #!; its interpreter is not recorded: a program if installed here, else ' + r[0])
    return r


def symlink_is_code(path):
    # Rule L: a symbolic link holds a path that the kernel and programs read as a value (S8.2-23);
    # it is not itself code. Links that are part of a package archive are decided by question 1.
    return False


def _unused_symlink_is_code(path):
    b = os.path.basename(path)
    d = os.path.dirname(path)
    if FOREIGN.search(path):
        return False
    if re.search(r'/(bin|sbin|shims|libexec|\.bin)(/|$)', d + '/') or d.endswith(('/bin', '/sbin', '/.bin')):
        return True
    if ext_of(path) in CODE_EXT or b in CODE_NAMES or re.search(r'\.so(\.\d+)*$', b):
        return True
    return False


def _classify(m):
    p, typ, exe, ctime = m['path'], m['type'], m['exec'], m['ctime']
    H = '/home/user'
    B = '/home/linuxbrew/.linuxbrew'

    # ---------------- Julia versions installed by juliaup (packages) ----------------
    jm = re.match(H + r'/\.julia/juliaup/(julia-[^/]+)(/.*)?$', p)
    if jm:
        if jm.group(2) is None:
            return ('INSTALLED-OWN', 'Julia version package installed at a person\'s command (juliaup)')
        if typ == 'file' and ctime and ctime > END['julia']:
            return ('PROGRAM-OWN' if is_code_file(p, exe, typ) else 'RECORD', 'changed after installation')
        return ('INSTALLED-PACKAGE', 'file of a Julia version package, unchanged since installation')
    if p.startswith(H + '/.julia/juliaup/'):
        b = os.path.basename(p)
        if b == 'juliaup.json':
            return ('SETTING-OWN', 'juliaup channel/default configuration: chooses which julia is launched')
        if p == H + '/.julia/juliaup/completions/bash.sh':
            return ('PROGRAM-DERIVED', 'bash completion code generated by juliaup')
        if b == 'completions' or p.startswith(H + '/.julia/juliaup/completions/'):
            return ('RECORD', 'completion files for shells not installed here, or their directory, written by juliaup')
        return ('RECORD', 'juliaup lock and downloaded version database')
    if p == H + '/.julia/juliaup' or p == H + '/.julia':
        return ('RECORD', 'directory created by juliaup for its own storage')

    # ---------------- juliaup itself ----------------
    if p in (H + '/.juliaup/bin/juliaup', H + '/.juliaup/bin/julialauncher', H + '/.juliaup/bin/juliaupgui'):
        return ('GAP-TWO', 'juliaup binary: INSTALLED-PACKAGE if juliaup is a package of itself, else PROGRAM-OWN')
    if p == H + '/.juliaup/bin/julia':
        return ('RECORD', 'julia link written by the juliaup installer (not code)')
    if p == H + '/.juliaup/juliaupself.json':
        return ('GAP-TWO', 'juliaup self-update options set at its installation: SETTING-DEFAULT or SETTING-OWN')
    if p in (H + '/.juliaup', H + '/.juliaup/bin'):
        return ('RECORD', 'directory created by the juliaup installer for its own layout')

    # ---------------- bun ----------------
    if p == H + '/.bun/bin/bun':
        return ('PROGRAM-OWN', 'bun runtime binary placed by bun install script at a person\'s command')
    if p == H + '/.bun/bin/bunx':
        return ('RECORD', 'bunx link written by the bun install script (a link is read as a value, not code)')
    if p == H + '/.bun/bin/eslint':
        return ('RECORD', 'eslint launcher link written by bun (a link is read as a value, not code)')
    if p in (H + '/.bun', H + '/.bun/bin', H + '/.bun/install', H + '/.bun/install/global'):
        return ('RECORD', 'directory created by bun for its own layout')
    if p.startswith(H + '/.bun/install/global/'):
        rel = p[len(H + '/.bun/install/global/'):]
        if rel in ('package.json', 'bun.lock', 'bun.lockb'):
            return ('RECORD', 'bun global manifest/lockfile written by bun as it ran')
        if rel == 'node_modules':
            return ('RECORD', 'directory created by bun for installed packages')
        if rel.startswith('node_modules/.bin'):
            if rel == 'node_modules/.bin':
                return ('RECORD', 'directory created by bun for launcher links')
            return ('RECORD', 'launcher link written by bun (not code)')
        if rel.startswith('node_modules/'):
            parts = rel.split('/')
            # package directory itself: node_modules/<name> or node_modules/@scope/<name> or nested node_modules
            pk = package_dir_depth(parts)
            if pk == 'scope':
                return ('RECORD', 'scope directory created by bun')
            if pk == 'package':
                name = parts[-1]
                if rel == 'node_modules/eslint':
                    return ('INSTALLED-OWN', 'eslint package installed at a person\'s command (bun add -g)')
                return ('INSTALLED-DERIVED', 'npm package installed by bun as a dependency of eslint')
            if typ == 'file' and ctime and ctime > END['tools']:
                return ('PROGRAM-OWN' if is_code_file(p, exe, typ) else 'RECORD', 'changed after installation')
            return ('INSTALLED-PACKAGE', 'file of an npm package, unchanged since installation')
        return ('RECORD', 'bun global state')
    if p.startswith(H + '/.bun/install/cache'):
        if typ == 'file' and is_code_file(p, exe, typ):
            return ('PROGRAM-DERIVED', 'code in bun package cache, obtained by bun for the eslint line')
        if typ == 'symlink' and symlink_is_code(p):
            return ('PROGRAM-DERIVED', 'code link in bun package cache')
        return ('RECORD', 'bun package cache (manifests, data, directories)')

    # ---------------- uv ----------------
    if p in (H + '/.local/bin/uv', H + '/.local/bin/uvx'):
        return ('PROGRAM-OWN', 'uv binary placed by the uv install script at a person\'s command')
    if p == H + '/.local/bin/ruff':
        return ('RECORD', 'ruff launcher link written by uv (not code)')
    if p == H + '/.config/uv/uv-receipt.json':
        return ('RECORD', 'receipt written by the uv installer as it ran')
    if p == H + '/.config/uv':
        return ('RECORD', 'directory created by the uv installer')
    if p.startswith(H + '/.local/share/uv'):
        T = H + '/.local/share/uv/tools/ruff'
        if p in (H + '/.local/share/uv', H + '/.local/share/uv/tools'):
            return ('RECORD', 'directory created by uv for tool environments')
        if p == T:
            return ('INSTALLED-OWN', 'ruff tool environment installed at a person\'s command (uv tool install)')
        rel = p[len(T) + 1:]
        wheel = (rel.startswith('lib/python3.15/site-packages/ruff') or rel == 'bin/ruff')
        if wheel:
            if typ == 'file' and ctime and ctime > END['tools']:
                return ('PROGRAM-OWN' if is_code_file(p, exe, typ) else 'RECORD', 'changed after installation')
            return ('INSTALLED-PACKAGE', 'file of the ruff wheel, unchanged since installation')
        if typ in ('file', 'symlink') and (is_code_file(p, exe, typ) or (typ == 'symlink' and symlink_is_code(p))):
            return ('PROGRAM-DERIVED', 'virtual-environment activation script generated by uv for ruff')
        return ('RECORD', 'virtual-environment scaffolding and receipt generated by uv')
    if p.startswith(H + '/.cache/uv'):
        if typ == 'file' and is_code_file(p, exe, typ):
            return ('PROGRAM-DERIVED', 'executable in uv cache, obtained by uv for the ruff line')
        return ('RECORD', 'uv cache')

    # ---------------- RubyGems (user install of lefthook) ----------------
    G = H + '/.local/share/gem/ruby'
    if p.startswith(G + '/gems/lefthook-2.2.2'):
        if p == G + '/gems/lefthook-2.2.2':
            return ('INSTALLED-OWN', 'lefthook gem installed at a person\'s command (gem install)')
        if typ == 'file' and ctime and ctime > END['tools']:
            return ('PROGRAM-OWN' if is_code_file(p, exe, typ) else 'RECORD', 'changed after installation')
        return ('INSTALLED-PACKAGE', 'file of the lefthook gem, unchanged since installation')
    if p == G + '/cache/lefthook-2.2.2.gem':
        return ('INSTALLED-PACKAGE', 'the lefthook gem archive as received, kept by RubyGems')
    if p == G + '/specifications/lefthook-2.2.2.gemspec':
        return ('PROGRAM-DERIVED', 'Ruby gemspec evaluated by RubyGems, generated at gem install')
    if p.startswith(H + '/.local/share/gem'):
        return ('RECORD', 'directory created by RubyGems')
    if p == H + '/bin/lefthook':
        return ('PROGRAM-DERIVED', 'Ruby wrapper script generated by RubyGems for the lefthook gem')
    if p == H + '/bin':
        return ('RECORD', 'directory created by RubyGems for wrappers')
    if p.startswith(H + '/.cache/gem'):
        return ('RECORD', 'RubyGems specification cache')

    # ---------------- Go build cache ----------------
    if p.startswith(H + '/.cache/go-build'):
        return ('RECORD', 'Go build cache entry (compiled outputs, not executable)')
    if p.startswith(H + '/.config/go'):
        return ('RECORD', 'Go telemetry local data written by the go command')

    # ---------------- Homebrew ----------------
    if p.startswith(H + '/.cache/Homebrew'):
        return ('RECORD', 'Homebrew download/API cache')
    C = B + '/Cellar'
    if p.startswith(C):
        if p == C:
            return ('RECORD', 'directory created by the Homebrew install script')
        if p == C + '/hello':
            return ('INSTALLED-OWN', 'hello formula installed at a person\'s command (brew install)')
        if p == C + '/hello/2.12.3':
            return ('INSTALLED-OWN', 'hello 2.12.3 keg installed at a person\'s command')
        if typ == 'file' and ctime and ctime > END['brew']:
            return ('PROGRAM-OWN' if is_code_file(p, exe, typ) else 'RECORD', 'changed after installation')
        return ('INSTALLED-PACKAGE', 'file of the hello bottle, unchanged since installation')
    HB = B + '/Homebrew'
    if p.startswith(HB):
        return homebrew_repo(p, typ, exe)
    if p.startswith(B) or p == '/home/linuxbrew':
        return brew_prefix(p, typ, exe)

    # ---------------- scc project ----------------
    S = H + '/Projects/scc'
    if p.startswith(S):
        return project(p, typ, exe, S)
    if p == H + '/Projects':
        return ('MATERIAL', 'projects directory created at a person\'s command')
    if p == H + '/Projects/development-web':
        return ('MATERIAL', 'project directory created at a person\'s command')
    if p == H + '/Projects/development-web/Dockerfile':
        return ('PROGRAM-OWN', 'Dockerfile: build instructions docker executes as code')
    if p == H + '/Projects/development-web/index.html':
        return ('MATERIAL', 'web page file of a person\'s project')

    # ---------------- other home files ----------------
    fixed = {
        H + '/.bash_history': ('RECORD', 'shell history written by bash'),
        H + '/.bash_logout': ('PROGRAM-DERIVED', 'bash logout file copied from /etc/skel at account creation, executed by bash'),
        H + '/.bash_profile': ('PROGRAM-OWN', 'shell startup file executed by bash as code'),
        H + '/.bashrc': ('PROGRAM-OWN', 'shell startup file executed by bash as code'),
        H + '/actions-status.tsv': ('RECORD', 'status table written by the action runner'),
        H + '/actions-logs': ('RECORD', 'directory of action output logs'),
        H + '/.cache': ('RECORD', 'cache directory'),
        H + '/.config': ('RECORD', 'configuration directory created by programs'),
        H + '/.config/mozilla': ('RECORD', 'directory created by a browser'),
        H + '/.config/go': ('RECORD', 'directory created by the go command'),
        H + '/.config/micro': ('RECORD', 'directory created by micro'),
        H + '/.config/systemd': ('RECORD', 'directory created by systemctl'),
        H + '/.config/systemd/user': ('RECORD', 'directory created by systemctl'),
        H + '/.config/systemd/user/cal-project-summary.service': ('SETTING-OWN', 'user service unit chosen by a person'),
        H + '/.config/systemd/user/cal-project-summary.timer': ('SETTING-OWN', 'user timer unit chosen by a person; launches the service'),
        H + '/.config/systemd/user/default.target.wants': ('SETTING-OWN', 'enablement directory of a user service'),
        H + '/.config/systemd/user/timers.target.wants': ('SETTING-OWN', 'enablement directory of a user timer'),
        H + '/.config/systemd/user/default.target.wants/cal-project-summary.service': ('SETTING-OWN', 'enablement link of a user service'),
        H + '/.config/systemd/user/timers.target.wants/cal-project-summary.timer': ('SETTING-OWN', 'enablement link of a user timer'),
        H + '/.local': ('RECORD', 'directory created by programs'),
        H + '/.local/bin': ('RECORD', 'directory created by installers'),
        H + '/.local/bin/cal-project-summary': ('PROGRAM-OWN', 'script written by a person, run by the user timer'),
        H + '/.local/share': ('RECORD', 'directory created by programs'),
        H + '/.local/share/cal-developer': ('RECORD', 'output directory of the summary service'),
        H + '/.local/share/cal-developer/project-summary.txt': ('RECORD', 'output written by the summary service'),
        H + '/.local/share/systemd': ('RECORD', 'systemd user state directory'),
        H + '/.local/share/systemd/timers': ('RECORD', 'systemd user timer stamps'),
        H + '/.local/share/systemd/timers/stamp-cal-project-summary.timer': ('RECORD', 'persistent timer stamp written by systemd'),
        H + '/.local/state': ('RECORD', 'state directory'),
        H + '/.local/state/cal-developer': ('RECORD', 'state directory of the action scripts'),
        H + '/.ssh': ('MATERIAL', 'directory of the person\'s SSH files'),
        H + '/.ssh/authorized_keys': ('SETTING-OWN', 'permits key login to this computer'),
        H + '/.ssh/config': ('UNKNOWN', 'SSH client config; content not recorded'),
        H + '/.ssh/id_ed25519_development': ('MATERIAL', 'private key for logging in to other machines'),
        H + '/.ssh/id_ed25519_development.pub': ('MATERIAL', 'public half of that key'),
        H + '/.bun': ('RECORD', 'directory created by the bun installer'),
        H: ('RECORD', 'home directory created by account creation (a directory written by a program)'),
        H + '/.julia': ('RECORD', 'directory created by juliaup'),
        H + '/.juliaup': ('RECORD', 'directory created by the juliaup installer'),
    }
    if p in fixed:
        return fixed[p]
    if p.startswith(H + '/actions-logs/'):
        return ('RECORD', 'output log of an action command')
    if p.startswith(H + '/.local/state/cal-developer/'):
        return ('RECORD', 'copies/notes written by the action scripts as they ran')
    if p.startswith(H + '/.config/micro/plug'):
        if p == H + '/.config/micro/plug':
            return ('RECORD', 'plugin directory created by micro')
        if p in (H + '/.config/micro/plug/editorconfig', H + '/.config/micro/plug/filemanager'):
            return ('INSTALLED-OWN', 'micro plugin installed by micro\'s built-in plugin manager at a person\'s command')
        if typ == 'file' and ctime and ctime > '2026-11-23T11:14:06.999':
            return ('PROGRAM-OWN' if ext_of(p) == '.lua' else 'RECORD', 'changed after installation')
        return ('INSTALLED-PACKAGE', 'file of a micro plugin, unchanged since installation')
    return None


def package_dir_depth(parts):
    """parts: ['node_modules', ...]. Return 'package' if path is a package root, 'scope' if a scope dir, else None."""
    i = 0
    state = None
    while i < len(parts):
        if parts[i] != 'node_modules':
            return None
        i += 1
        if i >= len(parts):
            return None
        if parts[i].startswith('@'):
            i += 1
            if i >= len(parts):
                return 'scope'
        # parts[i] is package name
        i += 1
        if i == len(parts):
            return 'package'
        if parts[i] != 'node_modules':
            return None
    return state


def homebrew_repo(p, typ, exe):
    """Homebrew/brew checkout placed by the Homebrew install script (not a package)."""
    rel = p[len('/home/linuxbrew/.linuxbrew/Homebrew'):]
    if rel.startswith('/.git/') or rel == '/.git':
        return git_internal(rel[len('/.git'):], typ, exe, 'Homebrew checkout')
    if rel.startswith('/Library/Homebrew/vendor/portable-ruby'):
        return ('MATERIAL', 'portable-ruby version pin file/dir of the downloaded checkout')
    if typ == 'directory':
        return ('MATERIAL', 'directory of the downloaded Homebrew checkout')
    if typ == 'file' and is_code_file(p, exe, typ):
        return ('PROGRAM-OWN', 'Homebrew code (Ruby/shell) placed by a person-run install script')
    if typ == 'symlink' and symlink_is_code(p):
        return ('PROGRAM-OWN', 'link to Homebrew code in the downloaded checkout')
    if os.path.basename(p) in ('_brew', 'brew') and '/completions/' in p:
        if '/zsh/' in p or '/fish/' in p:
            return ('MATERIAL', 'completion for a shell not installed here (not executable here)')
        return ('PROGRAM-OWN', 'bash completion code sourced by bash')
    return ('MATERIAL', 'non-code file of the downloaded Homebrew checkout (docs, data)')


def brew_prefix(p, typ, exe):
    B = '/home/linuxbrew/.linuxbrew'
    fixed = {
        B + '/bin/brew': ('RECORD', 'brew link written by the install script (not code)'),
        B + '/bin/hello': ('RECORD', 'hello link written by brew link (not code)'),
        B + '/opt/hello': ('RECORD', 'opt link to the keg written by brew'),
        B + '/lib/ld.so': ('RECORD', 'loader link written by brew (not code)'),
        B + '/etc/bash_completion.d/brew': ('RECORD', 'completion link written by the install script (not code)'),
        B + '/var/homebrew/linked/hello': ('RECORD', 'brew record of the linked keg'),
    }
    if p in fixed:
        return fixed[p]
    if p.startswith(B + '/var/'):
        return ('RECORD', 'Homebrew working state (locks, tmp, link records)')
    if typ == 'directory':
        return ('RECORD', 'prefix directory created by the Homebrew install script or brew link')
    if typ == 'symlink':
        if '/zsh/' in p or '/fish/' in p:
            return ('RECORD', 'completion link for a shell not installed; written by the install script')
        if symlink_is_code(p):
            return ('PROGRAM-DERIVED', 'code link generated by brew link')
        return ('RECORD', 'link (man, doc, info, locale) written by brew link; not code')
    if typ == 'file' and is_code_file(p, exe, typ):
        return ('PROGRAM-DERIVED', 'code file written by brew')
    return ('RECORD', 'file written by brew')


def git_internal(rel, typ, exe, what):
    """rel: path inside .git (starting with '/' or empty)."""
    if rel == '':
        return ('MATERIAL', 'git repository of the downloaded ' + what)
    if rel == '/hooks/pre-commit' and what == 'scc project':
        return ('INSTALLED-OWN', 'git hook installed (and removable) by lefthook, an installer, at a person\'s command')
    if rel.startswith('/hooks/') and typ == 'file':
        if rel.endswith('.sample'):
            return ('PROGRAM-OWN', 'executable sample hook script copied by git clone')
        return ('PROGRAM-OWN', 'git hook script installed at a person\'s command')
    if rel in ('/index', '/FETCH_HEAD', '/ORIG_HEAD', '/HEAD', '/packed-refs', '/description', '/shallow') or \
       rel.startswith('/logs') or rel.endswith('.lock') or rel == '/COMMIT_EDITMSG':
        return ('RECORD', 'git working state written by git as it ran')
    if rel == '/config':
        return ('RECORD', 'git repository config; obeyed only by git, launches nothing')
    if rel.startswith('/info'):
        return ('RECORD', 'git info written by git')
    return ('MATERIAL', 'objects/refs of the downloaded ' + what + ' repository')


def project(p, typ, exe, S):
    rel = p[len(S):]
    if rel == '':
        return ('MATERIAL', 'project directory cloned at a person\'s command')
    if rel.startswith('/.git/') or rel == '/.git':
        return git_internal(rel[len('/.git'):], typ, exe, 'scc project')
    if rel == '/scc':
        return ('PROGRAM-OWN', 'scc binary compiled at a person\'s command (go build)')
    if rel == '/lefthook.yml':
        return ('SETTING-OWN', 'lefthook config: commands its git hook launches')
    if rel.startswith('/.cal-modcache'):
        if typ == 'file' and is_code_file(p, exe, typ):
            return ('PROGRAM-OWN', 'Go module source in module cache, downloaded for a person\'s build')
        return ('RECORD', 'Go module cache data/directories')
    if typ == 'directory':
        return ('MATERIAL', 'directory of the cloned project')
    if typ == 'file' and is_code_file(p, exe, typ):
        return ('PROGRAM-OWN', 'code file of the cloned project executable here')
    if typ == 'symlink' and symlink_is_code(p):
        return ('PROGRAM-OWN', 'link to code in the cloned project')
    if typ == 'file' and FOREIGN.search(p) and exe == 'True':
        return ('MATERIAL', 'code not executable on this computer')
    return ('MATERIAL', 'non-code file of the cloned project (docs, data, foreign-language code)')
