from typing import NamedTuple
from enum import IntFlag, IntEnum
from bip_utils import Bip39EntropyBitLen, Bip39EntropyGenerator, Bip39WordsNum, Bip39Languages, Bip39MnemonicGenerator, Bip39MnemonicEncoder
from .loader import upload_apdus

class SetupModes(IntEnum):
    Wallet          = 0x01
    RelaxedWallet   = 0x02
    Server          = 0x04
    Developer       = 0x08

class SetupFeatures(IntFlag):
    UncompressedPublic  = 0x01
    DeterministicSig    = 0x02
    AuthAllSigHash      = 0x04
    Skip2FA             = 0x08

class SetupConfig(NamedTuple):
    mode: SetupModes
    features: SetupFeatures
    coinVersion: int
    p2shVersion: int


def setup(args):
    apdus = []
    # Select the applet
    apdus.append([0x00, 0xA4, 0x04, 0x00, 0x0C, 0xA0, 0x00, 0x00, 0x06, 0x17, 0x00, 0x54, 0xBF, 0x6A, 0xA9, 0x49, 0x01])
    # FACTORY INITIALIZE KEYCARD SEED
    apdus.append([0xD0, 0x26, 0x00, 0x00, 0x11, args.keycardsize] + list(args.keycardseed))
    # SETUP, regular
    config = SetupConfig(
        mode        = Wallet,
        features    = DeterministicSig | Skip2FA,
        coinVersion = 0x00, # Regular Addresses
        p2shVersion = 0x05  # Pay To Script Hash Addresses (BIP 16)
    )
    apdus.append([0xE0, 0x20, 0x00, 0x00])
    upload_apdus(args, apdus)
