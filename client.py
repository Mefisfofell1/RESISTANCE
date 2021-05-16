import socket

s = socket.socket()
s.connect(("26.155.142.20", 1234))
send = ''
while True:
	send += str(input())
	if send == 'stop':
		break
	s.send(bytes(send, "utf-8"))
	msg = s.recv(1024)
	print(msg.decode("utf-8"))
