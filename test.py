import socket
import json
import sys

#TCP_IP = '178.32.217.139'
#TCP_PORT = 3002
TCP_IP = '127.0.0.1'
TCP_PORT = 1337
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.recv(BUFFER_SIZE)

#[<puzzle name>. <puzzle as list>]
#puzzle_data = ["Tokyo Hotel", ['ABCDB EBFCG', 'AGHHD EEBAD', 'IIAFH EDJIB', 'AJFEH EDHFG', 'AJIIH EIFFJ', 'ABHJA EEAII']]
puzzle_data = ["Tokyo Hotel", ['XXXXX XXXXX', 'XXXXX XXXXX', 'IIAFH EDJIB', 'AJFEH EDHFG', 'AJIIH EIFFJ', 'ABHJA EEAII']]

old_solution = ["17037 47609", "19553 44713", "22165 43827", "18645 43569", "18225 42668", "17581 44122"]

request = json.dumps([puzzle_data])

print("Sending: " + request)
s.send(request)

print("Solution: " + s.recv(1024))
s.close()