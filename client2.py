import socket
import sys
import time
import msvcrt


def timed_input(caption, timeout=10):
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


s = socket.socket()
s.connect(("26.155.142.20", 1234))
send = ''
while True:
	send = str(timed_input(""))
	if send == 'stop':
		continue
	s.send(bytes(send, "utf-8"))
	msg = s.recv(1024)
	print(msg.decode("utf-8"))
