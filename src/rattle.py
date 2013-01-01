#!/usr/bin/python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.info('Starting...')

import sys
import socket
import string

class UiIrc:
	"""
	IRC User Interface class
	"""
	#_host, _port, _nick, _chan, _ident, _realname, 
	_readbuffer = ""
	_commands = []

	def __init__(self, host, port, nick, chan, ident="", realname=""):
		"""connect to specific IRC server and join the channel"""
		logging.debug("UiIrc.__init__()")
		self._host, self._port, self._nick, self._chan, self._ident, self._realname = host, port, nick, chan, ident, realname
		if ( len(self._ident) < 1 ):
			self._ident = self._nick.lower()
		if ( len(self._realname) < 1 ):
			self._realname = self._nick

		logging.debug(self)

		self._s = socket.socket( )
		self._s.connect(( self._host, self._port ))
		self.send("NICK %s" % self._nick)
		self.send("USER %s %s bla :%s" % (self._ident, self._host, self._realname))
		self.send("JOIN %s" % self._chan)


	def __del__(self):
		"""disconect or other destruction"""
		logging.debug("UiBase.__del__()")

	def __repr__(self):
		"""object string to debug"""
		return "%s (%s:%d) %s@%s" % (__name__, self._host, self._port, self._nick, self._chan)

	def __str__(self):
		"""object string to show"""
		return "%s (%s:%d) %s@%s" % (__name__, self._host, self._port, self._nick, self._chan)


	def _processing(self):
		self._readbuffer = self._readbuffer + self._s.recv(1024)
		temp = string.split( self._readbuffer, "\n")
		self._readbuffer = temp.pop( )

		for line in temp:
			line = string.rstrip(line)
			line = string.split(line)

			if(line[0]=="PING"):
				self._s.send("PONG %s\r\n" % line[1])

			# [':NeZinovaS!~darius@92111C5B.1EFA00A5.117F2273.IP', 'PRIVMSG', '#rattle', ':hi', 'again', 'rattleBotPy']
			if( line[2]==self._chan and len(line) >= 5 ):
				user = line[0].split("!")[0].split(":")[1]
				command = line[3].split(":")[1]
				subcommand = line[4]
				msg = ' '.join( line[3:len(line)] )
				self._commands.append(Command(user,command,subcommand,msg))

	def getUserCommand(self):
		self._processing();
		if self._commands:
			return self._commands.pop()
		else:
			return Command()

	def send(self, msg):
		logging.debug("Irc.send(): %s" % msg )
		self._s.send( msg + "\r\n" )

	def sendMsg(self, msg):
		self.send("PRIVMSG %s %s\r\n" % (self._chan, msg) )


class Command():
	'''Command structure'''
	def __init__(self, user="", command="", subcommand="", msg=""):
		self.user = user
		self.command = command
		self.subcommand = subcommand
		self.msg = msg
		self.inited = ( len(self.user) > 0 )


if __name__ == '__main__':
	ui = UiIrc("irc.data.lt", 6667, "rattleBotPy", "#rattle")
	while 1:
		cmd = ui.getUserCommand();
		if ( not cmd.inited ):
			continue

		if (cmd.command == "task" and cmd.subcommand == "add"):
			ui.sendMsg('oh... now I understand you...')
		else:
			ui.sendMsg("I don't realy know what are you talking about (%s)" % (cmd.msg) );

