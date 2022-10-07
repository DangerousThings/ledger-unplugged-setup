import os, argparse, getpass


def parse():
    parser = argparse.ArgumentParser(description = 'Manage Ledger Unplugged')

    parser.add_argument('-hd', '--help-documentation', action='store_true', dest='documentation', 
        help='Print the complete help documentation')
    parser.add_argument('-l', '--list-readers', action='store_true', dest='listreaders', 
        help='list available PC/SC readers')

    actions = parser.add_subparsers(help='desired action to perform', dest='action') 

    # Interfacing options
    parser_handle_load = argparse.ArgumentParser(add_help=False)
    parser_handle_load.add_argument('-r', '--reader', nargs='?', dest='reader', type=int, 
        const=0, default=0, 
        required=False, help='index of the PC/SC reader to use (default: 0)')

    # SETUP action
    parser_setup = actions.add_parser('setup', help='setup ledger unplugged device',
        parents=[parser_handle_load])
    parser_setup.add_argument('-k', '--keycard-size', nargs='?', dest='keycardsize', type=int, 
        const=4, default=4, 
        help='amount of random destination address characters the user has to provide (default: 4)')
    parser_setup.add_argument('-s', '--keycard-seed', 
        nargs='?', dest='keycardseed', type=str,
        help='keycard seed (16 bytes = 32 hexadecimal characters)')
    parser_setup.add_argument('-sf', '--keycard-seed-file', 
        nargs='?', dest='keycardseedfile', type=str, const='keycard.pass', default='keycard.pass', 
        help='file that contains the keycard seed (default: keycard.pass)')
    parser_setup.add_argument('-p', '--pin', 
        nargs='?', dest='pin', type=str,
        help='PIN (4 numbers from 0 to 9)')
    parser_setup.add_argument('-pf', '--pin-file', 
        nargs='?', dest='pinfile', type=str, const='pin.pass', default='pin.pass', 
        help='file that contains the pin (default: pin.pass)')
    parser_setup.add_argument('-m', '--mnemonic', 
        nargs='?', dest='mnemonic', type=str,
        help='recover using BIP39 encoded mnemonic phrase (24 english words)')
    parser_setup.add_argument('-mf', '--mnemonic-file', 
        nargs='?', dest='mnemonicfile', type=str, const='mnemonic.pass', default='mnemonic.pass', 
        help='file that contains the BIP39 encoded mnemonic phrase (default: mnemonic.pass)')
    parser_setup.add_argument('-lo', '--log--apdus-only', dest='apduonly', type=bool, 
        default=False, action = argparse.BooleanOptionalAction,
        help='only display APDUs without sending')

    args = parser.parse_args()
    return (parser, args)


def validate(parser, args):
    if(args.documentation):
        print(parser.format_help())
        subparsers_actions = [
            action for action in parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for _, action in subparsers_action.choices.items():
                print(action.format_help())
        exit(0)

    if(args.listreaders):
        return

    if(args.action is None):
        parser.print_help()
        exit(1)

    # Print action to be performed
    if(args.action == 'setup'):
        print('info: Setting up Ledger Unplugged')
   
    # Validate and query any needed secrets
    if(args.action == 'setup'):
        if(os.path.isfile(args.keycardseedfile)):
            with open(args.keycardseedfile, 'r') as f:
                args.keycardseed = f.read()
        if(args.keycardseed is None):
            pw1 = getpass.getpass('prompt: No keycard seed specified, please create one: ')
            pw2 = getpass.getpass('prompt: Re-type keycard seed for confirmation: ')
            if(pw1 == pw2):
                args.keycardseed = pw1
            else:
                print('error: Keycard seeds do not match.')
                exit(1)
        try:
            args.keycardseed = bytes.fromhex(args.keycardseed)
            if(len(args.keycardseed) != 16):
                print('error: Keycard seed size is not 16 bytes (32 hexadecimal characters).')
                exit(1)
        except:
            print('error: Cannot parse keycard seed as hexadecimal number.')
            exit(1)
        if(args.keycardsize < 0 or args.keycardsize > 10):
            print('error: Keycard size must be larger than 0 and smaller or equal to 10.')
            exit(1)
        
        if(os.path.isfile(args.pinfile)):
            with open(args.pinfile, 'r') as f:
                args.pin = f.read()
        if(args.pin is None):
            pw1 = getpass.getpass('prompt: No PIN specified, please create one: ')
            pw2 = getpass.getpass('prompt: Re-type PIN for confirmation: ')
            if(pw1 == pw2):
                args.pin = pw1
            else:
                print('error: PINs do not match.')
                exit(1)
        if(not args.pin.isdecimal()):
            print('error: Pin must only contain number from 0 to 9.')
            exit(1)
        if(len(args.pin) != 4):
            print('error: PIN size is not 4 characters.')
            exit(1)
        args.pin = args.pin.encode('ascii')

        if(os.path.isfile(args.mnemonicfile)):
            with open(args.mnemonicfile, 'r') as f:
                args.mnemonic = f.read()
