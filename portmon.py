#!/usr/bin/env python3

import socket
import sys
import locale
from datetime import datetime
from time import sleep
import argparse
parser = argparse.ArgumentParser(description='Monitors the specified host and port, when the state changes prints out a log entry to STDOUT. This log entry contains current date and time in default locale format.')
parser.add_argument('ip_addr', type=str, default=None, help='ip address or hostname to connect, default value is \'localhost\'')
parser.add_argument('port', type=int, help='port number to check')
parser.add_argument('-t', type=float, default='3', help='time interval between checks in seconds)')
args = parser.parse_args()

dt_format = locale.nl_langinfo(locale.D_T_FMT)  # so it deps on locale of the system where executed

last_state = 'third state'   #is it okay?
ex = None

if args.port not in range(0,65535) or not args.ip_addr:
    parser.print_help()
    sys.exit(f"{args.port} is invalid port value")   #it even returns the correct code!
    raise


while(True):


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((str(args.ip_addr),int(str(args.port))))
        new_state = True

    except Exception as e:
        new_state = False
        ex = e
    finally:
        if last_state == 'first iteration':
            print('first')
        if new_state != last_state:
            last_state = new_state
            if new_state:
                print(f"{datetime.now().strftime(dt_format)}: port {args.port} is listening at {args.ip_addr}")
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            else:
                print(f"{datetime.now().strftime(dt_format)} exception: {repr(ex)}")

        sleep(args.t)
