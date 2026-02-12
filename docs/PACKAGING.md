# Packaging Guide

This document describes how to build and distribute qnote packages.

## Building .deb Packages

### Requirements

```bash
# Debian/Ubuntu
sudo apt install debhelper dh-python python3-all python3-setuptools devscripts
```

### Quick Build

```bash
# Build package
./build-deb.sh

# Package is created at:
# ../qnote_0.1.0-1_all.deb
```

### Manual Build

```bash
# Clean previous builds
./cleanup-project.sh

# Build using dpkg-buildpackage
dpkg-buildpackage -us -uc -b

# Install
sudo dpkg -i ../qnote_*.deb
```

## Package Structure

### Debian Control Files

Located in `debian/` directory:

```
debian/
├── changelog       # Version history
├── control         # Package metadata
├── copyright       # License information
├── install         # Installation rules
└── rules           # Build rules
```

### debian/control

Defines package metadata:

```
Source: qnote
Section: utils
Priority: optional
Maintainer: Otis L. Crossley <qnote@olcrossley.uk>
Build-Depends: debhelper (>= 10),
               dh-python,
               python3-all,
               python3-setuptools
Standards-Version: 4.1.3

Package: qnote
Architecture: all
Depends: ${python3:Depends},
         ${misc:Depends},
         python3-click,
         python3-rich,
         python3-pygments,
         python3-yaml
Description: Quick note and snippet manager
 A minimalist CLI tool for managing notes, code snippets,
 and TODO items directly from the terminal.
```

### debian/changelog

Version history:

```
qnote (0.1.0-1) unstable; urgency=medium

  * Initial release
  * Core functionality: notes, snippets, TODOs
  * Tag support and search
  * Shell completion

 -- Otis L. Crossley <qnote@olcrossley.uk>  Mon, 10 Feb 2026 12:00:00 +0000
```

### debian/rules

Build rules:

```makefile
#!/usr/bin/make -f

%:
	dh $@ --with python3 --buildsystem=pybuild
```

### debian/install

Installation rules:

```
docs/* usr/share/doc/qnote/
```

## Version Management

### Updating Version

1. Update `pyproject.toml`:
```toml
[project]
version = "0.2.0"
```

2. Update `debian/changelog`:
```bash
dch -i  # Interactive changelog update
```

3. Update `qnote/__init__.py`:
```python
__version__ = "0.2.0"
```

### Version Scheme

Follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

Example: `0.1.0` → `0.2.0` → `1.0.0`

## Distribution Methods

### 1. GitHub Releases

Create a release on GitHub:

```bash
# Tag version
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Upload .deb file to GitHub Releases
# Users download and install:
sudo dpkg -i qnote_0.1.0-1_all.deb
```

### 2. PPA (Ubuntu/Debian)

Create a Personal Package Archive on Launchpad:

```bash
# Build source package
dpkg-buildpackage -S

# Upload to PPA
dput ppa:olc1910/qnote ../qnote_0.1.0-1_source.changes

# Users add PPA:
sudo add-apt-repository ppa:olc1910/qnote
sudo apt update
sudo apt install qnote
```

### 3. Direct Distribution

Share .deb file directly:

```bash
# Build package
./build-deb.sh

# Share ../qnote_0.1.0-1_all.deb via:
# - Email
# - USB drive
# - Network share
# - Web server

# Users install:
sudo dpkg -i qnote_0.1.0-1_all.deb
sudo apt-get install -f  # Fix dependencies
```

## Building for Multiple Distributions

### Debian Stable

```bash
# Build on Debian stable
dpkg-buildpackage -us -uc -b
```

### Ubuntu LTS

```bash
# Build on Ubuntu LTS
dpkg-buildpackage -us -uc -b
```

### Using pbuilder

Build in clean environment:

```bash
# Create base system
sudo pbuilder create

# Build package
sudo pbuilder build qnote_0.1.0-1.dsc
```

## Automated Builds

### GitHub Actions

Create `.github/workflows/build.yml`:

```yaml
name: Build Package

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install debhelper dh-python python3-all
      
      - name: Build package
        run: ./build-deb.sh
      
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: qnote-deb
          path: ../qnote_*.deb
```

## Package Verification

### Test Installation

```bash
# Build package
./build-deb.sh

# Install in clean container
docker run -it debian:latest
apt update
apt install -y ../qnote_0.1.0-1_all.deb

# Test
qnote --version
qnote add "test"
```

### Lintian Checks

```bash
# Check package quality
lintian ../qnote_0.1.0-1_all.deb

# Fix warnings
# - Update debian/control
# - Update debian/copyright
# - Rebuild
```

### Package Info

```bash
# Show package details
dpkg-deb -I ../qnote_0.1.0-1_all.deb

# List package contents
dpkg-deb -c ../qnote_0.1.0-1_all.deb
```

## Cleanup

### Remove Build Artifacts

```bash
# Use cleanup script
./cleanup-project.sh

# Or manually
rm -rf debian/qnote
rm -rf debian/.debhelper
rm -f debian/files
rm -f ../qnote_*.deb
rm -f ../qnote_*.build*
```

## Troubleshooting

### Build Failures

```bash
# Check dependencies
dpkg-checkbuilddeps

# Install missing dependencies
sudo apt-get install <missing-package>

# Clean and retry
./cleanup-project.sh
./build-deb.sh
```

### Installation Issues

```bash
# Check dependencies
apt-cache policy python3-click python3-rich

# Install manually
sudo apt install python3-click python3-rich python3-pygments python3-yaml

# Fix broken dependencies
sudo apt-get install -f
```

### Version Conflicts

```bash
# Remove old version
sudo dpkg -r qnote

# Install new version
sudo dpkg -i ../qnote_0.2.0-1_all.deb
```

## Best Practices

1. **Test before release**
   - Build in clean environment
   - Test installation
   - Run lintian checks

2. **Version carefully**
   - Follow semantic versioning
   - Update all version strings
   - Update changelog

3. **Document changes**
   - Maintain debian/changelog
   - Update CHANGELOG.md
   - Tag releases in git

4. **Sign packages**
   - Use GPG key for signatures
   - Sign both .deb and source packages

## See Also

- [INSTALL.md](INSTALL.md) - Installation guide
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
- Debian Policy Manual: https://www.debian.org/doc/debian-policy/
- Debian New Maintainers' Guide: https://www.debian.org/doc/manuals/maint-guide/
