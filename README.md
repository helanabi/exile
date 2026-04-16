## Overview

A CLI tool that delays access to a secret to reduce impulsive behavior.

## Quick Start

```
$ exile --delay=360 abc123
$ exile
Secret will be available after 6 hours
```
After 6 hours:
```
$ exile
abc123
```

## Motivation

**Exile** was designed to enforce self-discipline and fight impulsive urges
by delaying access to a password protected material.  

For example it could be used to reduce addiction to various internet-related
activities such as doom-scrolling, online shopping, pornography, video games,
etc. by storing an account or locker password in `exile` and setting
an appropriate delay, which forces the user to wait for that amount of time
before regaining access, which in turn potentially absorbs the urge to
undertake the addressed activity immediately.

## Security Model

**Exile** uses symmetric encryption with a random 32-byte key
generated at build time and embedded into the binary.  

Serious attempts by competent individuals can extract the encryption key
and bypass **exile** by inspecting the binary, but the goal of **exile**
is not invincible protection, it's making bypassing harder than waiting.

## Installation

* [Download the latest version](https://github.com/helanabi/exile/archive/refs/tags/v0.1.0.zip)
* `unzip exile-0.1.0.zip`
* `cd exile-0.1.0`
* `pip install -r requirements.txt`
* `sh build.sh`
* Place binary in your `PATH`, e.g. `sudo cp dist/exile /usr/local/bin/`
* Use `exile -h` for usage help

## Usage

```
usage: exile [-h] [-c] [-d DELAY] [-f] [-r] [-v] [secret]

Delay access to a secret

positional arguments:
  secret

options:
  -h, --help         show this help message and exit
  -c, --cancel       cancel unlock request
  -d, --delay DELAY  delay duration in minutes
  -f, --force        overwrite existing secret
  -r, --remove
  -v, --version      show software version and copyright notice
```

## Examples

* Store a secret with a 10-hours delay:  
`$ exile --delay=600 mypassword`

* Start unlock timer:  
`$ exile`

* Cancel unlock request:  
`$ exile --cancel`

* Remove secret:  
`$ exile --remove`

## Storage

**Exile** stores encrypted data in:

`~/.cache/exile_data`

## License

This project is licensed under the GNU General Public License v3.0 or later.  
See the COPYING file for details.