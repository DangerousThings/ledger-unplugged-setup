#!/usr/bin/env python3

import ledger.argparser as arg
import ledger.loader as load
import ledger.setup as setup

if __name__ == '__main__':
    parser, args = arg.parse()
    arg.validate(parser, args)

    if(args.listreaders):
        load.list_readers()
        exit(1)

    if(args.action == 'setup'):
        setup.setup(args)
