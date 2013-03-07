from Command import Command

def run(bot, serv, ev) :
	message = ev.arguments()[0]
	module = message.split(' ')[1]
	bot.log('Unloading %s' % module)
	for i in bot.plugins :
		if module in str(i) :
			bot.plugins.remove(i)
			bot.log('Unloaded %s' % i)
			return 
	for i in bot.commands :
		if module in str(i) :
			bot.commands.remove(i)
			bot.log('Unloaded %s' % i)
			return 
	bot.log('No such module (%s)' % module)

regex = 'unload (Commands|Plugins)\.\w+'

command = Command(regex, run)

