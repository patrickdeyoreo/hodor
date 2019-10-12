#!/usr/bin/env python3
""" Vote for my ID
"""
from requests import exceptions, sessions
from sys import argv, exit, stderr
from time import sleep


if __name__ == '__main__':
    """ Vote an arbitrary number of times for my ID
    """
    name = argv[0].split('/')[-1]
    usage = f"usage: {name} count"

    if len(argv) != 2:
        print(f"{name}: {usage}", file=stderr)
        exit(2)

    try:
        count = int(argv[1])
    except ValueError:
        print(f"{name}: {argv[1]}: count must be a number", file=stderr)
        print(f"{name}: {usage}", file=stderr)
        exit(1)

    url = 'http://158.69.76.135/level1.php'

    headers = {
        'Host': '158.69.76.135',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://158.69.76.135',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'Referer': 'http://158.69.76.135/level1.php',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
            'id': '801',
            'holdthedoor': 'Submit',
            }

    with sessions.Session() as session:
        try:
            print("Initiating session...", end="")
            session.get(url)

            data['key'] = session.cookies['HoldTheDoor']
            headers['Cookie'] = f"HoldTheDoor={data['key']}"
            print(f"\nSession initiated (key: {data['key']})")

            print(f"Voting {count} times:")
            for vote in range(1, count + 1):
                try:
                    print(f"Submitting vote #{vote}...", end="")
                    session.post(url=url, headers=headers, data=data)
                    print()

                except exceptions.ConnectionError:
                    print("\nReconnecting...", end="")
                    for reconnect in range(10):
                        sleep(10)
                        try:
                            session.get(url)
                        except exceptions.ConnectionError:
                            if reconnect == 10:
                                print("\nUnable to reconnect.")
                                exit(1)
                        else:
                            data['key'] = session.cookies['HoldTheDoor']
                            headers['Cookie'] = f"HoldTheDoor={data['key']}"
                            break

        except KeyboardInterrupt:
            print("\nReceived interrupt.")
            exit(130)

    print("Done.")
    exit(0)
