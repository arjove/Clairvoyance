import socket
import json
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 1337
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.recv(BUFFER_SIZE)

#[<puzzle name>. <puzzle as list>]
puzzle_data = ["Tokyo Hotel", ['ABCDB EBFCG', 'AGHHD EEBAD', 'IIAFH EDJIB', 'AJFEH EDHFG', 'AJIIH EIFFJ', 'ABHJA EEAII']]
puzzle_json = json.dumps(puzzle_data)

s.send(puzzle_json)
resp = ""
while resp != "[*] Goodbye!\n":
	resp = s.recv(BUFFER_SIZE)
	sys.stdout.write(resp)
	try:
		if resp[-1] == '>':
			s.send(raw_input())
	except:
		pass #I know error handling, I have the best error handling - Donald J. Trump


s.close()