#!/usr/bin/env python3
""" Vote for my ID
"""
from sys import argv, exit as sysexit, stderr
from time import sleep
from requests import exceptions, request


def confirm(prompt="[Y/n] "):
    """ Get a yes/no response on stdin
    """
    while True:
        try:
            return {
                'Y': True,
                'N': False
            }[input(prompt).lstrip()[0].upper()]
        except (IndexError, KeyError):
            pass


if __name__ == '__main__':

    url = 'http://158.69.76.135/level0.php'

    headers = {
        'Host': '158.69.76.135',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://158.69.76.135/level0.php',
    }

    data = {
        'id': '801',
        'holdthedoor': 'Submit',
    }

    usage = f"{argv[0].split('/')[-1]} count"

    if len(argv) != 2:
        print(f"usage: {usage}", file=stderr)
        sysexit(2)

    try:
        count = int(argv[1])
    except ValueError:
        print(f"invalid count: {argv[1]}", file=stderr)
        print(f"usage: {usage}", file=stderr)
        sysexit(1)

    try:
        if not confirm(f"Submit {count} vote{'s' * (count != 1)}? [Y/n] "):
            print("Aborting.")
            sysexit(0)

        try:
            request("GET", url=url)
        except exceptions.ConnectionError:
            print("\nUnable to connect.")
            sysexit(1)

        for vote in range(1, count + 1):
            try:
                print(f"Submitting vote #{vote}...", end="")
                request("POST", url=url, headers=headers, data=data)
                print()
            except exceptions.ConnectionError:
                print("\nConnecting...", end="")
                for reconnect in range(6):
                    sleep(10)
                    try:
                        request("GET", url=url)
                    except exceptions.ConnectionError:
                        if reconnect == 6:
                            print("\nUnable to connect.")
                            sysexit(1)
                    else:
                        print()
                        break
    except KeyboardInterrupt:
        print("\nReceived interrupt.")
        sysexit(130)

    print("Done.")
    sysexit(0)
