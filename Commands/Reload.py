from Plugin import Plugin
import irclib

def run(bot, serv, ev) :
	bot.log('Reloading plugins')
	bot.reloadModules(bot.plugins)
	bot.log('Reloading commands')
	bot.reloadModules(bot.commands)

regex = 'reload'

command = Plugin(regex, run)
