# Language package classification notes

Only the assigned pip, pip3, gem and Flatpak rows were classified. Registry summaries establish function, not the inventory labels. Root/user and pip/pip3 duplicates remain distinct input objects. No removal or executable probes were performed.

## Literal decision rule

S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

Rule L: Distributions documented as executable interpreter libraries, native bindings, or commands receive MUST under S2.2-9 and S2.2-10. Package membership alone is insufficient. Each distinct distribution function was checked against the publisher description below; the script applies the same executable-code criterion after that check. This includes modules that generate logs or manipulate documents: these objects are the generating code, not the resulting logs or documents.

The certifi distribution includes callable Python code exposing its trust bundle; it is not classified merely from the certificate data. The rbs distribution includes a parser and executable processing library, not just signatures. The same-name registry entries for crit and setools describe different projects; upstream distribution documentation replaces those entries. The rpm and selinux modules use distribution upstream documentation, not similarly named registry shims.

## Manual rule checks

Each check compared input name and version membership, documentation of function, and whether the documented operation executes as interpreter or native library code. All passed Rule L. Twenty checks cover both ecosystems (ten per ecosystem):

- tumbleweed-91003489d9c6d84b6bd5a5e7 — bcrypt: Hashes passwords using executable cryptographic routines. Executable code, Rule L applies.
- tumbleweed-8efb93d0f65e02d08d825b05 — brotli: Compresses and decompresses data using Python bindings. Executable code, Rule L applies.
- tumbleweed-4f4472d16a42b1f89c38355c — cffi: Calls native C functions from Python. Executable code, Rule L applies.
- tumbleweed-03570c53d3d665aace086b68 — configobj: Reads writes and validates configuration files. Executable code, Rule L applies.
- tumbleweed-9c9a5af6cd79f480cfe794d9 — h2: Implements HTTP/2 networking protocol. Executable code, Rule L applies.
- tumbleweed-5389f1cad541525a16e30701 — psutils: Manipulates PDF and PostScript pages. Executable code, Rule L applies.
- tumbleweed-bc22e130404255602beef624 — pycparser: Parses C source code. Executable code, Rule L applies.
- tumbleweed-c29fe5ad92614b05a5b9696a — requests: Makes HTTP requests. Executable code, Rule L applies.
- tumbleweed-38ba6e0ada70367cb00323c9 — six: Provides Python version compatibility routines. Executable code, Rule L applies.
- tumbleweed-2bb73fd5c1d1cf9e3090ad0a — zstandard: Compresses and decompresses data. Executable code, Rule L applies.
- tumbleweed-cd665989a3023f589b8c955c — abbrev: Calculates unique abbreviations for strings. Executable code, Rule L applies.
- tumbleweed-19f11611aab12cf15951c710 — base64: Encodes and decodes Base64 data. Executable code, Rule L applies.
- tumbleweed-712c0b6b0feccc3784259371 — cfa: Reads and modifies configuration files. Executable code, Rule L applies.
- tumbleweed-213114cb508c754fa48336c8 — cheetah: Executes external commands from Ruby. Executable code, Rule L applies.
- tumbleweed-6ea0372074481e2fb1d67cc5 — fileutils: Copies moves and removes files. Executable code, Rule L applies.
- tumbleweed-47c2a344efbc750e157de2cd — irb: Runs an interactive Ruby interpreter. Executable code, Rule L applies.
- tumbleweed-d5182a2190fd7dc51159ca33 — json: Parses and generates JSON data. Executable code, Rule L applies.
- tumbleweed-8c2da33af6ad8dc27dcd837f — net-http: Performs HTTP requests. Executable code, Rule L applies.
- tumbleweed-880947f6f5d67baa5dd38ca1 — rbs: Parses and processes Ruby type signatures. Executable code, Rule L applies.
- tumbleweed-2c852d4eafbf03d1c83b723f — syslog: Writes messages to system logging. Executable code, Rule L applies.

## Documentation evidence

Publisher metadata was retrieved from the linked package-registry API; quoted excerpts are at most twenty words. Raw inventory membership is in the evidence file named by each input row.

- gem abbrev — https://rubygems.org/api/v1/gems/abbrev.json — “Calculates a set of unique abbreviations for a given set of strings”
- gem abstract_method — https://rubygems.org/api/v1/gems/abstract_method.json — “Abstract Method is a tiny library enabling you to define abstract methods in Ruby classes and modules.”
- gem base64 — https://rubygems.org/api/v1/gems/base64.json — “Support for encoding and decoding binary data using a Base64 representation.”
- gem benchmark — https://rubygems.org/api/v1/gems/benchmark.json — “a performance benchmarking library”
- gem bigdecimal — https://rubygems.org/api/v1/gems/bigdecimal.json — “This library provides arbitrary-precision decimal floating-point number class.”
- gem bundler — https://rubygems.org/api/v1/gems/bundler.json — “Bundler manages an application's dependencies through its entire life, across many machines, systematically and repeatably”
- gem cfa — https://rubygems.org/api/v1/gems/cfa.json — “Library offering separation of parsing and file access from the rest of the logic for managing configuraton files. It has”
- gem cfa_grub2 — https://rubygems.org/api/v1/gems/cfa_grub2.json — “Models allowing easy read and modification of GRUB2 configuration files. It is a plugin for cfa framework.”
- gem cgi — https://rubygems.org/api/v1/gems/cgi.json — “Support for the Common Gateway Interface protocol.”
- gem cheetah — https://rubygems.org/api/v1/gems/cheetah.json — “Your swiss army knife for executing external commands in Ruby safely and conveniently.”
- gem csv — https://rubygems.org/api/v1/gems/csv.json — “The CSV library provides a complete interface to CSV files and data. It offers tools to enable you to read”
- gem date — https://rubygems.org/api/v1/gems/date.json — “The official date library for Ruby.”
- gem debug — https://rubygems.org/api/v1/gems/debug.json — “Debugging functionality for Ruby. This is completely rewritten debug.rb which was contained by the ancient Ruby versions.”
- gem delegate — https://rubygems.org/api/v1/gems/delegate.json — “Provides three abilities to delegate method calls to an object.”
- gem did_you_mean — https://rubygems.org/api/v1/gems/did_you_mean.json — “The gem that has been saving people from typos since 2014.”
- gem digest — https://rubygems.org/api/v1/gems/digest.json — “Provides a framework for message digest libraries.”
- gem drb — https://rubygems.org/api/v1/gems/drb.json — “Distributed object system for Ruby”
- gem english — https://rubygems.org/api/v1/gems/english.json — “Require 'English.rb' to reference global variables with less cryptic names.”
- gem erb — https://rubygems.org/api/v1/gems/erb.json — “An easy to use but powerful templating system for Ruby.”
- gem error_highlight — https://rubygems.org/api/v1/gems/error_highlight.json — “The gem enhances Exception#message by adding a short explanation where the exception is raised”
- gem etc — https://rubygems.org/api/v1/gems/etc.json — “Provides access to information typically stored in UNIX /etc directory.”
- gem fast_gettext — https://rubygems.org/api/v1/gems/fast_gettext.json — “A simple, fast, memory-efficient and threadsafe implementation of GetText”
- gem fcntl — https://rubygems.org/api/v1/gems/fcntl.json — “Loads constants defined in the OS fcntl.h C header file”
- gem fiddle — https://rubygems.org/api/v1/gems/fiddle.json — “A libffi wrapper for Ruby.”
- gem fileutils — https://rubygems.org/api/v1/gems/fileutils.json — “Several file utility methods for copying, moving, removing, etc.”
- gem find — https://rubygems.org/api/v1/gems/find.json — “This module supports top-down traversal of a set of file paths.”
- gem forwardable — https://rubygems.org/api/v1/gems/forwardable.json — “Provides delegation of specified methods to a designated object.”
- gem gem2rpm — https://rubygems.org/api/v1/gems/gem2rpm.json — “Generate source rpms and rpm spec files from a Ruby Gem. The spec file tries to follow the gem as”
- gem getoptlong — https://rubygems.org/api/v1/gems/getoptlong.json — “GetoptLong for Ruby”
- gem io-console — https://rubygems.org/api/v1/gems/io-console.json — “add console capabilities to IO instances.”
- gem io-nonblock — https://rubygems.org/api/v1/gems/io-nonblock.json — “Enables non-blocking mode with IO class”
- gem io-wait — https://rubygems.org/api/v1/gems/io-wait.json — “Deprecated: All functionality ships with Ruby 3.2 and higher.”
- gem ipaddr — https://rubygems.org/api/v1/gems/ipaddr.json — “IPAddr provides a set of methods to manipulate an IP address. Both IPv4 and IPv6 are supported.”
- gem irb — https://rubygems.org/api/v1/gems/irb.json — “Interactive Ruby command-line tool for REPL (Read Eval Print Loop).”
- gem json — https://rubygems.org/api/v1/gems/json.json — “This is a JSON implementation as a Ruby extension in C.”
- gem logger — https://rubygems.org/api/v1/gems/logger.json — “Provides a simple logging utility for outputting messages.”
- gem matrix — https://rubygems.org/api/v1/gems/matrix.json — “An implementation of Matrix and Vector classes.”
- gem minitest — https://rubygems.org/api/v1/gems/minitest.json — “minitest provides a complete suite of testing facilities supporting TDD, BDD, and benchmarking.”
- gem mutex_m — https://rubygems.org/api/v1/gems/mutex_m.json — “Mixin to extend objects to be handled like a Mutex.”
- gem net-ftp — https://rubygems.org/api/v1/gems/net-ftp.json — “Support for the File Transfer Protocol.”
- gem net-http — https://rubygems.org/api/v1/gems/net-http.json — “HTTP client api for Ruby.”
- gem net-imap — https://rubygems.org/api/v1/gems/net-imap.json — “Ruby client api for Internet Message Access Protocol”
- gem net-pop — https://rubygems.org/api/v1/gems/net-pop.json — “Ruby client library for POP3.”
- gem net-protocol — https://rubygems.org/api/v1/gems/net-protocol.json — “The abstract interface for net-* client.”
- gem net-smtp — https://rubygems.org/api/v1/gems/net-smtp.json — “Simple Mail Transfer Protocol client library for Ruby.”
- gem nkf — https://rubygems.org/api/v1/gems/nkf.json — “Ruby extension for Network Kanji Filter”
- gem nokogiri — https://rubygems.org/api/v1/gems/nokogiri.json — “Nokogiri (鋸) makes it easy and painless to work with XML and HTML from Ruby. It provides a sensible, easy-to-understand”
- gem observer — https://rubygems.org/api/v1/gems/observer.json — “Implementation of the Observer object-oriented design pattern.”
- gem open-uri — https://rubygems.org/api/v1/gems/open-uri.json — “An easy-to-use wrapper for Net::HTTP, Net::HTTPS and Net::FTP.”
- gem open3 — https://rubygems.org/api/v1/gems/open3.json — “Popen, but with stderr, too”
- gem openssl — https://rubygems.org/api/v1/gems/openssl.json — “OpenSSL for Ruby provides access to SSL/TLS and general-purpose cryptography based on the OpenSSL library.”
- gem optparse — https://rubygems.org/api/v1/gems/optparse.json — “OptionParser is a class for command-line option analysis. It is much more advanced, yet also easier to use, than GetoptLong,”
- gem ostruct — https://rubygems.org/api/v1/gems/ostruct.json — “Class to build custom data structures, similar to a Hash.”
- gem power_assert — https://rubygems.org/api/v1/gems/power_assert.json — “Power Assert shows each value of variables and method calls in the expression. It is useful for testing, providing which”
- gem pp — https://rubygems.org/api/v1/gems/pp.json — “Provides a PrettyPrinter for Ruby objects”
- gem prettyprint — https://rubygems.org/api/v1/gems/prettyprint.json — “Implements a pretty printing algorithm for readable structure.”
- gem prime — https://rubygems.org/api/v1/gems/prime.json — “Prime numbers and factorization library.”
- gem prism — https://rubygems.org/api/v1/gems/prism.json — “Prism Ruby parser”
- gem pstore — https://rubygems.org/api/v1/gems/pstore.json — “Transactional File Storage for Ruby Objects”
- gem psych — https://rubygems.org/api/v1/gems/psych.json — “Psych is a YAML parser and emitter. Psych leverages libyaml[https://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting capabilities. In addition to”
- gem racc — https://rubygems.org/api/v1/gems/racc.json — “Racc is an LALR(1) parser generator. It is written in Ruby itself, and generates Ruby program. NOTE: Ruby 1.8.x comes”
- gem rake — https://rubygems.org/api/v1/gems/rake.json — “Rake is a Make-like program implemented in Ruby. Tasks and dependencies are specified in standard Ruby syntax. Rake has the”
- gem rbs — https://github.com/ruby/rbs/blob/master/docs/architecture.md — “The parser is implemented in C extension.”
- gem rdoc — https://rubygems.org/api/v1/gems/rdoc.json — “RDoc produces HTML and command-line documentation for Ruby projects. RDoc includes the +rdoc+ and +ri+ tools for generating and displaying”
- gem readline — https://rubygems.org/api/v1/gems/readline.json — “This is just a loader for "readline". If Ruby has the "readline-ext" gem that is a native extension, this gem”
- gem reline — https://rubygems.org/api/v1/gems/reline.json — “Alternative GNU Readline or Editline implementation by pure Ruby.”
- gem repl_type_completor — https://rubygems.org/api/v1/gems/repl_type_completor.json — “Type based completion for REPL.”
- gem resolv — https://rubygems.org/api/v1/gems/resolv.json — “Thread-aware DNS resolver library in Ruby.”
- gem resolv-replace — https://rubygems.org/api/v1/gems/resolv-replace.json — “Replace Socket DNS with Resolv.”
- gem rexml — https://rubygems.org/api/v1/gems/rexml.json — “An XML toolkit for Ruby”
- gem rinda — https://rubygems.org/api/v1/gems/rinda.json — “The Linda distributed computing paradigm in Ruby.”
- gem rss — https://rubygems.org/api/v1/gems/rss.json — “Family of libraries that support various formats of XML "feeds".”
- gem ruby-augeas — https://rubygems.org/api/v1/gems/ruby-augeas.json — “Provides bindings for augeas.”
- gem ruby-dbus — https://rubygems.org/api/v1/gems/ruby-dbus.json — “Pure Ruby module for interaction with D-Bus IPC system”
- gem ruby2_keywords — https://rubygems.org/api/v1/gems/ruby2_keywords.json — “Shim library for Module#ruby2_keywords”
- gem securerandom — https://rubygems.org/api/v1/gems/securerandom.json — “Interface for secure random number generator.”
- gem shellwords — https://rubygems.org/api/v1/gems/shellwords.json — “Manipulates strings with word parsing rules of UNIX Bourne shell.”
- gem simpleidn — https://rubygems.org/api/v1/gems/simpleidn.json — “This gem allows easy conversion from punycode ACE strings to unicode UTF-8 strings and vice-versa.”
- gem singleton — https://rubygems.org/api/v1/gems/singleton.json — “The Singleton module implements the Singleton pattern.”
- gem stringio — https://rubygems.org/api/v1/gems/stringio.json — “Pseudo `IO` class from/to `String`.”
- gem strscan — https://rubygems.org/api/v1/gems/strscan.json — “Provides lexical scanning operations on a String.”
- gem syntax_suggest — https://rubygems.org/api/v1/gems/syntax_suggest.json — “When you get an "unexpected end" in your syntax this gem helps you find it”
- gem syslog — https://rubygems.org/api/v1/gems/syslog.json — “Ruby interface for the POSIX system logging facility.”
- gem tempfile — https://rubygems.org/api/v1/gems/tempfile.json — “A utility class for managing temporary files.”
- gem test-unit — https://rubygems.org/api/v1/gems/test-unit.json — “test-unit (Test::Unit) is unit testing framework for Ruby, based on xUnit principles.”
- gem time — https://rubygems.org/api/v1/gems/time.json — “Extends the Time class with methods for parsing and conversion.”
- gem timeout — https://rubygems.org/api/v1/gems/timeout.json — “Auto-terminate potentially long-running operations in Ruby.”
- gem tmpdir — https://rubygems.org/api/v1/gems/tmpdir.json — “Extends the Dir class to manage the OS temporary file path.”
- gem tsort — https://rubygems.org/api/v1/gems/tsort.json — “Topological sorting”
- gem typeprof — https://rubygems.org/api/v1/gems/typeprof.json — “TypeProf performs a type analysis of non-annotated Ruby code. It abstractly executes input Ruby code in a level of types”
- gem un — https://rubygems.org/api/v1/gems/un.json — “Utilities to replace common UNIX commands”
- gem uri — https://rubygems.org/api/v1/gems/uri.json — “URI is a module providing classes to handle Uniform Resource Identifiers”
- gem weakref — https://rubygems.org/api/v1/gems/weakref.json — “Allows a referenced object to be garbage-collected.”
- gem yaml — https://rubygems.org/api/v1/gems/yaml.json — “YAML Ain't Markup Language”
- gem zlib — https://rubygems.org/api/v1/gems/zlib.json — “Ruby interface for the zlib compression/decompression library”
- pip PyGObject — https://pypi.org/pypi/PyGObject/json — “Python bindings for GObject Introspection”
- pip PySocks — https://pypi.org/pypi/PySocks/json — “A Python SOCKS client module.”
- pip bcrypt — https://pypi.org/pypi/bcrypt/json — “Modern password hashing for your software and your servers”
- pip brotli — https://pypi.org/pypi/brotli/json — “Python bindings for the Brotli compression library”
- pip certifi — https://pypi.org/project/certifi/ — “you can use the built-in function:”
- pip cffi — https://pypi.org/pypi/cffi/json — “Foreign Function Interface for Python calling C code.”
- pip charset-normalizer — https://pypi.org/pypi/charset-normalizer/json — “The Real First Universal Charset Detector. Open, modern and actively maintained alternative to Chardet.”
- pip cmdln — https://pypi.org/pypi/cmdln/json — “An improved cmd.py for writing multi-command scripts and shells.”
- pip configobj — https://pypi.org/pypi/configobj/json — “Config file reading, writing and validation.”
- pip createrepo_c — https://pypi.org/pypi/createrepo_c/json — “C implementation of createrepo”
- pip crit — https://criu.org/GSoC_completed_projects — “Currently CRIT is implemented in Python”
- pip cryptography — https://pypi.org/pypi/cryptography/json — “cryptography is a package which provides cryptographic recipes and primitives to Python developers.”
- pip cupshelpers — https://github.com/OpenPrinting/system-config-printer/blob/master/Makefile.am — “cupshelpers/cupshelpers.py”
- pip decorator — https://pypi.org/pypi/decorator/json — “Decorators for Humans”
- pip h2 — https://pypi.org/pypi/h2/json — “Pure-Python HTTP/2 protocol implementation”
- pip hpack — https://pypi.org/pypi/hpack/json — “Pure-Python HPACK header encoding”
- pip hyperframe — https://pypi.org/pypi/hyperframe/json — “Pure-Python HTTP/2 framing”
- pip idna — https://pypi.org/pypi/idna/json — “Internationalized Domain Names in Applications (IDNA)”
- pip nftables — https://wiki.iptables.org/wiki-nftables/index.php/Scripting — “The same functionality provided by the nft command-line utility is available from within Python programs”
- pip pip — https://pypi.org/pypi/pip/json — “The PyPA recommended tool for installing Python packages.”
- pip protobuf — https://protobuf.dev/reference/python/python-generated/ — “The Python Protobuf implementation is a little different from C++ and Java.”
- pip psutil — https://pypi.org/pypi/psutil/json — “Cross-platform lib for process and system monitoring.”
- pip psutils — https://pypi.org/pypi/psutils/json — “Manipulate PDF and PostScript documents”
- pip puremagic — https://pypi.org/pypi/puremagic/json — “Pure python implementation of magic file detection”
- pip pyOpenSSL — https://pypi.org/pypi/pyOpenSSL/json — “Python wrapper module around the OpenSSL library”
- pip pycairo — https://pypi.org/pypi/pycairo/json — “Python interface for cairo”
- pip pycparser — https://pypi.org/pypi/pycparser/json — “C parser in Python”
- pip pycriu — https://packages.debian.org/sid/python3-pycriu — “This package provides the criu Python bindings”
- pip pycups — https://pypi.org/pypi/pycups/json — “Python bindings for libcups”
- pip pycurl — https://pypi.org/pypi/pycurl/json — “PycURL -- A Python Interface To The cURL library”
- pip pygdbmi — https://pypi.org/pypi/pygdbmi/json — “Parse gdb machine interface output with Python”
- pip pyinotify — https://pypi.org/pypi/pyinotify/json — “Linux filesystem events monitoring”
- pip pypdf — https://pypi.org/pypi/pypdf/json — “A pure-python PDF library capable of splitting, merging, cropping, and transforming PDF files”
- pip pysmbc — https://pypi.org/pypi/pysmbc/json — “Python bindings for libsmbclient”
- pip python-linux-procfs — https://packagehub.suse.com/packages/python-linux-procfs/ — “Abstractions to extract information from the Linux kernel /proc files.”
- pip pyudev — https://pypi.org/pypi/pyudev/json — “A libudev binding”
- pip requests — https://pypi.org/pypi/requests/json — “Python HTTP for Humans.”
- pip rpm — https://rpm.org/docs/4.20.x/api/ — “This documents the librpm API as available to rpm itself”
- pip selinux — https://github.com/SELinuxProject/selinux/wiki/Userspace-Packages — “libselinux is the runtime SELinux library”
- pip sepolicy — https://github.com/SELinuxProject/selinux/wiki/Tools — “front-end for inspecting or generating policy”
- pip setools — https://github.com/SELinuxProject/setools — “libraries designed to facilitate SELinux policy analysis.”
- pip setuptools — https://pypi.org/pypi/setuptools/json — “Most extensible Python build backend with support for C/C++ extension modules”
- pip six — https://pypi.org/pypi/six/json — “Python 2 and 3 compatibility utilities”
- pip urllib3 — https://pypi.org/pypi/urllib3/json — “HTTP library with thread-safe connection pooling, file post, and more.”
- pip zstandard — https://pypi.org/pypi/zstandard/json — “Zstandard bindings for Python”

## Eight Flatpak rows, individually assessed

https://docs.flatpak.org/en/latest/extension.html: “stable mesa fallback build”; “support for patented codecs”; “Extension point for Gtk3 themes.” These document the two GL rows, the codecs-extra successor, and the shared theme respectively. Graphics and codec libraries are executed with application rights. The theme is provided by the runtime to multiple applications, so S2.2-7 does not exempt it.

https://docs.flatpak.org/en/latest/basic-concepts.html: “Runtimes provide the basic dependencies used by applications.” The platform is executable runtime support, required by S2.2-2 and S2.2-10.

https://apps.gnome.org/Calculator/: “Calculator is an application that solves mathematical equations.” Calculator receives MUST under S2.2-9 and S2.2-12.

https://docs.flatpak.org/en/latest/flatpak-builder-command-reference.html: “Separate out locale files and translations to an extension runtime.” Both Locale rows receive HOLE: translated strings can be read as content whose removal leaves operations intact, or as the ability to produce a localized interface. S2.2-2 and S2.2-4 do not specify the boundary; S2.2-7 additionally comes close for calculator-only localization. This is a classification boundary, not a choice of state migration design.

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

## Verification

The append-resumable script language-write.py verifies the assigned input/output ID sets and counts, uniqueness, allowed decisions, and word limits. Result after review: 378 rows; MUST 375, HOLE 3, NOT 0, UNKNOWN 0, MIXED 0.

## Review amendment

The shared GTK theme row tumbleweed-6aa862424bccb9f5ca9b17cc was initially MUST because the theme affects multiple applications, excluding S2.2-7. That inference did not resolve S2.2-4: documentation establishes shared styling but does not establish executable theme code. The same distinction between lost presentation capability and unavailable presentation content that affects translations also applies here. Decision amended to HOLE, citing S2.2-2, S2.2-4, and S2.2-7. This amendment supersedes the initial theme assessment above.

Version limitation: package-registry summaries and some upstream documentation describe the currently published project, not necessarily the exact installed version. They establish the stable functional role of the identified distribution, rather than exact installed contents or version-specific behavior. Recorded versions and related package identities were checked for obvious project-name collisions; replacements are documented above. No exact-version source audit is claimed.
