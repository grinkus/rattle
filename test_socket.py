#!/usr/bin/python

import sys
import socket
import string

HOST="irc.data.lt"
PORT=6667
NICK="rattleBotPy"
IDENT="rattlebot"
REALNAME="rattleBot"
CHAN="rattle"
readbuffer=""

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN #%s\r\n" % CHAN)

while 1:
	readbuffer=readbuffer+s.recv(1024)
	temp=string.split(readbuffer, "\n")
	readbuffer=temp.pop( )

	for line in temp:
		line=string.rstrip(line)
		line=string.split(line)

		if(line[0]=="PING"):
			s.send("PONG %s\r\n" % line[1])
# [':NeZinovaS!~darius@92111C5B.1EFA00A5.117F2273.IP', 'PRIVMSG', '#rattle', ':hi', 'again', 'rattleBotPy']

		if(line[2]=="#rattle" and line[3]==":task" and line[4]=="add"):
			s.send("PRIVMSG #%s %s\r\n" % (CHAN, line[5]) )

		print line

