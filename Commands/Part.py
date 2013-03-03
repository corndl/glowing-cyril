from Command import Command
import irclib

def run(bot, serv, ev) :
	chan = ev.arguments()[0].split(' ')[1]
	source = irclib.nm_to_n(ev.source())
	bot.part(serv, chan, ev.source())

regex = 'part #.+'

command = Command(regex, run)
