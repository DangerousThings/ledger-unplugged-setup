# Ledger Unplugged Setup

Tool to setup the [Ledger Unplugged applet](https://github.com/VivoKey/apex-ledger-unplugged). To generate and install attestation certificates, please use [fido-attestation-loader](https://github.com/DangerousThings/fido-attestation-loader) in `ledger` mode.
## Setup

Install [Python 3](https://www.python.org/downloads/) and Pip (usually packaged with Python), both are probably available via your package manager. Use Pip in the terminal to install the requirements: 

```
pip install -r requirements.txt
``` 

Required modules are `cryptography`, `asn1`, and `pyscard`. The executable might also be called `pip3`. If you use NixOS, Flake and EnvRC files are provided.

### Providing Secrets

To setup the Ledger Unplugged, several secrets have to be specified. This can be done in one of three ways for various commands:

1. Interactively during script runtime, by entering it when the script asks for input.
2. As a commandline parameter, by using the `-s` and `-p` parameters.
3. Inside a text file, by optionally specifying the file path using the `-sf` and `-pf` parameters. The default file names are `keycard_seed.pass` and `pin.pass`.

Option one requires an interactive terminal, which might be a problem if you want to pipe the script output to another program. When using option two, the passphrase might be logged into your terminal history file in clear text. Option three requires you to protect the passphrase file yourself however you see fit, e.g. by bind-mounting it and restricting access.

## Complete Commandline Reference

Use `./setup.py -hd` to print this information.

```

```
