from smartcard.System import readers


def list_readers():
    redlist = readers()
    if(len(redlist) == 0):
        print('warning: No PC/SC readers found')
        return
    redlist.sort(key=str)
    print('info: Available PC/SC readers (' + str(len(redlist)) + '):')
    for i, reader in enumerate(redlist):
        print(str(i) + ': ' + str(reader))


def upload_apdus(args, apdus):
    if(args.apduonly):
        print('info: Generated ' + str(len(apdus)) + ' APDUs:')
        for i, apdu in enumerate(apdus):
            print('info: Index: ' + str(i) + ', Length: ' + str(len(apdu)) + ', Data: ' + bytes(apdu).hex())
        exit(0)

    redlist = readers()
    if(len(redlist) == 0):
        print('error: No PC/SC readers found')
        exit(1)
    if(args.reader < 0 or args.reader >= len(redlist)):
        print('error: Specified reader index is out of range')
        exit(1)
    redlist.sort(key=str)
    red = redlist[args.reader]
    print('info: Using reader ' + str(args.reader) + ': ' + str(red))

    connection = red.createConnection()
    connection.connect()
    for i, apdu in enumerate(apdus):
        data, sw1, sw2 = connection.transmit(apdu)
        if(sw1 == 0x90 and sw2 == 0x00):
            print('success: APDU ' + str(i + 1) + '/' + str(len(apdus)) +
                ' (' + str(len(apdu)) + ' bytes) transferred, card response is ok')
        else:
            print('error: Card response: ' + f'{sw1:02x}' + ' ' + f'{sw2:02x}, aborting upload')
            connection.disconnect()
            exit(1)
    connection.disconnect()
