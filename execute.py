from server import P2P
import msvcrt
import time
import sys

a = P2P(1234, 1)

te = ''
a.create_session("26.155.142.220")


def timed_input(caption, timeout=3):
    def echo(c):
        sys.stdout.write(c)
        sys.stdout.flush()

    echo(caption)

    _input = []
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if msvcrt.kbhit():
            c = msvcrt.getwch()
            if ord(c) == 13:
                echo('\r\n')
                break
            _input.append(c)
            echo(c)

    if _input:
        return ''.join(_input)


while True:
    te = (str(timed_input("")))
    print(te)
    a.send("26.155.142.220", bytes(te, "utf-8"))
    if te == 'stop':
        a.kill_server()
    b = a.client_sockets[0].recv(1024)
    print(b.decode("utf-8"))
    print(a.client_sockets[0])
