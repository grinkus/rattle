#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG)
logging.info('Starting...')

from interfaces.irc import Irc


if __name__ == '__main__':
	interfaces = [
		Irc("irc.server", 6667, "nickname", "#channel", "ident")
	]

	while 1:

		for ui in interfaces:
			event = ui.getLastEvent();

			if event is None:
				continue

			elif event.event_type == "groupchat":
				for interface in interfaces:
					if interface == ui:
						continue
					else:
						interface.sendMsg( "Respond. (%s)" % event.msg )
