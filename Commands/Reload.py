from Command import Command

def run(bot, serv, ev) :
	bot.log('Reloading plugins')
	bot.reloadModules(bot.plugins)
	bot.log('Reloading commands')
	bot.reloadModules(bot.commands)

regex = 'reload'

command = Command(regex, run)
