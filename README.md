# Ledger Unplugged Setup

Tool to setup the [Ledger Unplugged applet](https://github.com/VivoKey/apex-ledger-unplugged). To generate and install attestation certificates, please use [fido-attestation-loader](https://github.com/DangerousThings/fido-attestation-loader) in `ledger` mode.
## Setup

Install [Python 3](https://www.python.org/downloads/) and Pip (usually packaged with Python), both are probably available via your package manager. Use Pip in the terminal to install the requirements: 

```
pip install -r requirements.txt
``` 

Required modules are `cryptography`, `asn1`, and `pyscard`. The executable might also be called `pip3`. If you use NixOS, Flake and EnvRC files are provided.

## Complete Commandline Reference

Use `./setup.py -hd` to print this information.

```

```
