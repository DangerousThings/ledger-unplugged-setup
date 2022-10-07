# Ledger Unplugged Setup

Tool to setup the [Ledger Unplugged applet](https://github.com/VivoKey/apex-ledger-unplugged). To generate and install attestation certificates, please use [fido-attestation-loader](https://github.com/DangerousThings/fido-attestation-loader) in `ledger` mode.
## Setup

Install [Python 3](https://www.python.org/downloads/) and Pip (usually packaged with Python), both are probably available via your package manager. Use Pip in the terminal to install the requirements: 

```
pip install -r requirements.txt
``` 

Required modules are `cryptography`, `asn1`, `pyscard`, and `bip-utils`. The executable might also be called `pip3`. If you use NixOS, Flake and EnvRC files are provided.

### Providing Secrets

To setup the Ledger Unplugged, several secrets have to be specified. This can be done in one of three ways for various commands:

1. Interactively during script runtime, by entering it when the script asks for input.
2. As a commandline parameter, by using the `-s`, `-p` and `-m` parameters.
3. Inside a text file, by optionally specifying the file path using the `-sf`, `-pf`, and `-mf` parameters. The default file names are `keycard.pass`, `pin.pass`, and `mnemonic.pass`.

Option one requires an interactive terminal, which might be a problem if you want to pipe the script output to another program. When using option two, the passphrase might be logged into your terminal history file in clear text. Option three requires you to protect the passphrase file yourself however you see fit, e.g. by bind-mounting it and restricting access.

### Air-Gapped Setup

If the token has been properly provisioned with an attestation certificate, the setup process can be encrypted. This is not yet implemented in this tool.

## Seeds

The applet expects two distinct seeds: A `16` byte keycard seed, and a `64` byte mnemonic seed (`BIP39`).

The keycard seed is usually unique per token, it may come as e.g. a QR code on a piece of paper together with the token from the manufacturer.

The mnemonic seed is randomly generated, and is intended to be backed up by the user in order to recover the token in the future if necessary.

## Initialize Using Random Mnemonic Seed

To initialize a fresh token using a random seed:

```
./ledger.py setup
```

You can also specify the PIN and keycard seed instead of being prompted:

```
./ledger.py setup -p 1234 -s 1234567890abcdef1234567890abcdef
```

You might have to specify the index of your PC/SC reader using the `-r` flag (use `./ledger.py -l` to list connected readers).

## Recover Using Mnemonic Seed Phrase

If you have a backup of your mnemonic seed phrase which was displayed when you initialized the token (as well as the keycard seed you chose), you can use that to recover:

```
./ledger.py setup -m "demand soup present horn child flat meat quality smoke flavor toe method govern winter spot west lock tell sunny spoil cage topic shoe card" ...
```

You can also put these words in a text file and use the `-mf` option.

## Complete Commandline Reference

Use `./setup.py -hd` to print this information.

```
usage: ledger.py [-h] [-hd] [-l] {setup} ...

Manage Ledger Unplugged

positional arguments:
  {setup}               desired action to perform
    setup               setup ledger unplugged device

options:
  -h, --help            show this help message and exit
  -hd, --help-documentation
                        Print the complete help documentation
  -l, --list-readers    list available PC/SC readers

usage: ledger.py setup [-h] [-r [READER]] [-k [KEYCARDSIZE]] [-s [KEYCARDSEED]] [-sf [KEYCARDSEEDFILE]] [-p [PIN]] [-pf [PINFILE]] [-m [MNEMONIC]] [-mf [MNEMONICFILE]]
                       [-lo | --log--apdus-only | --no-log--apdus-only]

options:
  -h, --help            show this help message and exit
  -r [READER], --reader [READER]
                        index of the PC/SC reader to use (default: 0)
  -k [KEYCARDSIZE], --keycard-size [KEYCARDSIZE]
                        amount of random destination address characters the user has to provide (default: 4)
  -s [KEYCARDSEED], --keycard-seed [KEYCARDSEED]
                        keycard seed (16 bytes = 32 hexadecimal characters)
  -sf [KEYCARDSEEDFILE], --keycard-seed-file [KEYCARDSEEDFILE]
                        file that contains the keycard seed (default: keycard.pass)
  -p [PIN], --pin [PIN]
                        PIN (4 numbers from 0 to 9)
  -pf [PINFILE], --pin-file [PINFILE]
                        file that contains the pin (default: pin.pass)
  -m [MNEMONIC], --mnemonic [MNEMONIC]
                        recover using BIP39 encoded mnemonic phrase (24 english words)
  -mf [MNEMONICFILE], --mnemonic-file [MNEMONICFILE]
                        file that contains the BIP39 encoded mnemonic phrase (default: mnemonic.pass)
  -lo, --log--apdus-only, --no-log--apdus-only
                        only display APDUs without sending (default: False)
```
