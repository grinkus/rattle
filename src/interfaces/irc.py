import logging
import socket
import string

from interfaces.base import Event

class Irc:
	"""
	IRC User Interface class
	"""
	#_host, _port, _nick, _chan, _ident, _realname
	_readbuffer = ""
	_events = []

	def __init__(self, host, port, nick, chan, ident="", realname=""):
		"""connect to specific IRC server and join the channel"""
		logging.debug("Irc.__init__()")
		self._host, self._port, self._nick, self._chan, self._ident, self._realname = host, port, nick, chan, ident, realname
		if ( len(self._ident) < 1 ):
			self._ident = self._nick.lower()
		if ( len(self._realname) < 1 ):
			self._realname = self._nick

		logging.debug(self)

		self._s = socket.socket( )
		self._s.connect(( self._host, self._port ))
		self.send("NICK %s" % self._nick)
		self.send("USER %s 0 * :%s" % (self._ident, self._realname))
		self.send("JOIN %s" % self._chan)


	def __del__(self):
		"""disconect or other destruction"""
		logging.debug("Irc.__del__()")

	def __repr__(self):
		"""object string to debug"""
		return "%s (%s:%d) %s@%s" % (__name__, self._host, self._port, self._nick, self._chan)

	def __str__(self):
		"""object string to show"""
		return "%s (%s:%d) %s@%s" % (__name__, self._host, self._port, self._nick, self._chan)


	def _processing(self):
		self._readbuffer = self._readbuffer + self._s.recv(1024)
		temp = string.split( self._readbuffer, "\n" )
		self._readbuffer = temp.pop()

		for line in temp:
			line = string.rstrip( line )
			line = string.split( line )

			if line[0] == "PING":
				self._s.send( "PONG %s\r\n" % line[1] )

			elif line[2] == self._chan and len( line ) >= 4 :
				user = line[0].split("!")[0][1:]
				msg = ' '.join( line[3:] )
				target = line[2]

				if line[1] == "PRIVMSG":
					event_type = "groupchat"
					self._events.append( Event( user, msg, target, event_type ) )

	def getLastEvent(self):
		self._processing();
		if self._events:
			return self._events.pop()
		else:
			return None

	def send(self, msg):
		logging.debug("Irc.send(): %s" % msg )
		self._s.send( msg + "\r\n" )

	def sendMsg(self, msg):
		self.send("PRIVMSG %s :%s\r\n" % (self._chan, msg) )