from typing import NamedTuple
from enum import IntFlag, IntEnum
from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip39MnemonicGenerator, Bip39Languages, Bip39WordsNum
from .loader import upload_apdus


class SetupModes(IntEnum):
    Wallet          = 0x01
    RelaxedWallet   = 0x02
    Server          = 0x04
    Developer       = 0x08

class SetupFeatures(IntFlag):
    UncompressedPublic  = 0x01 # Use uncompressed public keys in addresses (otherwise compress them)
    DeterministicSig    = 0x02 # Enable RFC 6979 deterministic signatures (otherwise use a random K)
    AuthAllSigHash      = 0x04 # Authorize all signature hashtypes (otherwise only authorize SIGHASH_ALL)
    Skip2FA             = 0x08 # Skip second factor, allow relaxed inputs and arbitrary output scripts if consuming P2SH inputs in a transaction


def setup(args):
    apdus = []

    # Select the applet
    apdus.append([
        0x00, 0xA4, 0x04, 0x00, # Command
        0x0C, # AID length
        0xA0, 0x00, 0x00, 0x06, 0x17, 0x00, 0x54, 0xBF, 0x6A, 0xA9, 0x49, 0x01 # AID
    ])

    # Refer to https://raw.githubusercontent.com/LedgerHQ/btchip-doc/master/bitcoin-technical.asc

    # FACTORY INITIALIZE KEYCARD SEED
    apdus.append([
        0xD0, 0x26, 0x00, 0x00, # Command
        0x11, # Data length
        args.keycardsize # Number of random address characters to provide
        ] + list(args.keycardseed) # Keycard seed
    )

    # SETUP, regular (P1 = 0x00)
    seed = None
    if(args.mnemonic is not None):
        if(Bip39MnemonicValidator().IsValid(args.mnemonic)):
            seed = Bip39SeedGenerator(args.mnemonic).Generate()
            print('info: Recovering using existing mnemonic seed.')
        else:
            print('error: Cannot parse mnemonic seed as BIP39.')
            exit(1)
    if(seed is None):
        print('info: Generating random mnemonic seed, make sure to back it up:')
        mnemonic = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)
        print('      ' + str(mnemonic))
        seed = Bip39SeedGenerator(mnemonic).Generate()
    apdus.append([
        0xE0, 0x20, 0x00, 0x00, # Command
        0x4C, # Data length
        SetupModes.Wallet, # Mode
        SetupFeatures.DeterministicSig | SetupFeatures.Skip2FA, # Features
        0x00, # Version for Regular Addresses
        0x05, # Version for Pay To Script Hash Addresses (BIP 16), or 0x00 if disabled
        0x04  # PIN length
    ] + list(args.pin) + [ # PIN
        0x00, # Secondary PIN length (unused)
        0x40  # BIP32 seed length (64 bytes)
    ] + list(seed) + [ # BIP32 seed
        0x00  # 3DES-2 key wrapping key length only for developer mode (0x00 to generate a new key, 0x10 to set up a backup)
    ])

    upload_apdus(args, apdus)
