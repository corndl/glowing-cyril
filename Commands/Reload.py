from Plugin import Plugin
import irclib

def run(bot, serv, ev) :
	bot.log('Reloading')
	bot.reloadModules()

regex = 'reload'

command = Plugin(regex, run)
