---
note: 2009-03-17_dynamically-loaded-modules.md
note_dir: texts
note_sha256: 9689786b64ee111f728140a71c48039e57d6172809345134e38a4b85383df154
title: "Dynamically Loaded Modules"
author: Guido van Rossum
created: 2009-03-17T13:07:00
ideas: 8
quotes_found: 8/8
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### c-extension-modules-easy-from-the-start
- **What**: Python's implementation architecture was built so that extension modules written in C were easy to write from the beginning.
- **Quote**: "Python's implementation architecture made it easy to write extension modules written in C right from the start." (line 2)

### early-static-linking-of-extensions
- **What**: In the early days, because dynamic loading technology was obscure, C extensions had to be statically linked into the interpreter at build time, which required adding them to a shell script that generated the Makefile.
- **Quote**: "in the early days, dynamic loading technology was obscure enough that such extensions had to be statically linked into Python interpreter at build time." (line 2)

### community-growth-demanded-separate-loading
- **What**: As the community produced new extension modules faster than anticipated, it demanded that modules could be compiled and loaded separately, which led to interfacing the import statement with the platform's dynamic linking API so import could look for a shared library as well as a ".py" file.
- **Quote**: "the Python community started producing new extension modules at an unanticipated rate, and demanded that extension modules could be compiled and loaded separately." (line 4)
- **Also at**: lines 4 ("code interfacing to the platform-specific dynamic linking API was contributed which allowed the import statement to go out to disk looking for a shared library as well as a ".py" file")

### dynamic-linking-maintenance-nightmare
- **What**: The dynamic linking support was very useful but introduced a maintenance problem, because each platform used a different API and some had additional constraints.
- **Quote**: "The dynamic linking support proved to be very useful, but also introduced a maintenance nightmare.  Each platform used a different API and some platforms had additional constraints." (line 6)

### restructuring-dynamic-linking-code
- **What**: The dynamic linking code was restructured over time: first concentrated into a single source file (which then became cluttered with #ifdef conditional compilation), later split so each platform's code sits in its own file, with Greg Stein's help.
- **Quote**: "the dynamic linking support was restructured so that all the dynamic linking code was concentrated in a single source file.  However, the approach resulted in a large file cluttered with conditional compilation directives (#ifdef)." (line 6)
- **Also at**: lines 6 ("it was restructured again with the help of Greg Stein so that the platform-specific code for each platform was placed in a file specific to that platform")

### building-modules-remained-a-mystery
- **What**: Even with support for dynamically loadable modules, the procedure for building them stayed obscure to many users, and distributing an extension faced major hurdles across the combinations of platforms, compilers, and linkers.
- **Quote**: "the procedure for building such modules often remained a mystery to many users." (line 8)
- **Also at**: lines 8 ("a user wishing to distribute an extension module faced major hurdles getting the module to compile on all possible combinations of platforms, compilers, and linkers")

### distutils-builds-from-anywhere-via-saved-options
- **What**: The distutils tool, largely by Greg Ward, let users build and install extension modules from anywhere; Python's makefile wrote the needed compiler and linker options to a data file that distutils then consulted, and it was integrated as a standard library module starting with Python 1.6.
- **Quote**: "a Python extension building tool called distutils was invented that allowed building and installing extension modules from anywhere. The necessary compiler and linker options were written by Python's makefile to a data file, which was then consulted by distutils when building extension modules." (line 10)
- **Also at**: lines 10 ("Starting with Python 1.6 it was integrated into Python distributions as a standard library module")

### distutils-scope-complexity-and-fragmentation
- **What**: distutils does far more than build C extensions (installing pure Python modules and packages, creating Windows installers, running tools like SWIG), but its complexity and lack of maintenance led to third-party alternatives (ez_install / "eggs") and fragmentation in the community; Guido reflects that the problem in full generality seems inherently difficult.
- **Quote**: "distutils does far more than simply building extension modules from C source code." (line 12)
- **Also at**: lines 12 ("its complexity has caused many folks to curse it, and it has not received the maintenance attention it deserved"), 12 ("3rd party alternatives (especially ez_install, a.k.a. "eggs") have become popular, unfortunately causing fragmentation in the development community"), 12 ("It seems that the problem in its full generality is just inherently difficult")
- **Open**: Guido states the packaging problem in its full generality seems inherently difficult, leaving it unresolved.
