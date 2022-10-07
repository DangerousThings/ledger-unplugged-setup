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
        nargs='?', dest='keycardseedfile', type=str, const='keycard_seed.pass', default='keycard_seed.pass', 
        help='file that contains the keycard seed (default: keycard_seed.pass)')
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
