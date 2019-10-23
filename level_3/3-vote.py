#!/usr/bin/env python3
""" Vote for my ID
"""
from sys import argv, exit as sysexit, stderr
from time import sleep

from tempfile import TemporaryFile
from requests import sessions
try:
    import Image
except ModuleNotFoundError:
    from PIL import Image
from pytesseract import image_to_string


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


URL = 'http://158.69.76.135/level3.php'

HEADERS = {
    'Host': '158.69.76.135',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': URL,
    'User-Agent': ' '.join((
        'Mozilla/5.0',
        '(Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36',
        '(KHTML, like Gecko)',
        'Chrome/74.0.3729.169',
        'Safari/537.36',
    )),
}

DATA = {
    'id': '801',
    'holdthedoor': 'Submit',
}

USAGE = f"usage: {argv[0].split('/')[-1]} count"


if __name__ == '__main__':

    if len(argv) != 2:
        print(USAGE, file=stderr)
        sysexit(2)

    try:
        COUNT = int(argv[1])
    except ValueError:
        print(f"invalid count: {argv[1]}", file=stderr)
        print(USAGE, file=stderr)
        sysexit(1)

    if not confirm(f"Submit {COUNT} vote{'s'*(COUNT!=1)}? [Y/n] "):
        print("Aborting.")
        sysexit(0)

    try:
        with sessions.Session() as session:
            print("Initiating session...", end="")
            try:
                session.get(URL)
            except ConnectionError:
                print("\nUnable to connect.")
                sysexit(1)

            print(f"\nSession initiated ({session.cookies['HoldTheDoor']})")
            VOTE = 1
            while VOTE < COUNT + 1:
                try:
                    with TemporaryFile() as image:
                        RESP = session.get(
                            url=URL.replace('level3.php', 'captcha.php'),
                            headers={**HEADERS, 'Content-Type': 'image/*'},
                        )
                        image.write(RESP.content)
                        DATA['captcha'] = image_to_string(Image.open(image))
                        DATA['key'] = session.cookies['HoldTheDoor']

                    print(f"Submitting vote #{VOTE}...", end="")
                    RESP = session.post(url=URL, headers=HEADERS, data=DATA)
                    if int(RESP.HEADERS['Content-Length']) < 128:
                        print("\nIncorrect captcha.")
                    else:
                        print()
                        VOTE += 1

                except ConnectionError:
                    print("\nReconnecting...", end="")
                    for reconnect in range(6):
                        sleep(10)
                        try:
                            session.get(URL)
                        except ConnectionError:
                            if reconnect == 6:
                                print("\nUnable to reconnect.")
                                sysexit(1)
                        else:
                            DATA['key'] = session.cookies['HoldTheDoor']
                            print(f"\nSession continued ({DATA['key']})")
                            break
                finally:
                    session.cookies.clear_expired_cookies()

    except KeyboardInterrupt:
        print("\nReceived interrupt.")
        session.close()
        sysexit(130)

    print("Done.")
    sysexit(0)
