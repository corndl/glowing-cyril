from Command import Command

def run(bot, serv, ev) :
	message = ev.arguments()[0]
	module = message.split(' ')[1]
	bot.log('Importing %s' % module)
	try :
		bot.importModule(module)
	except ImportError as e :
		bot.log('Couldn\'t import %s : %s, line %s, col %s' % (module, 
				e.args[0][0], e.args[0][1][1], e.args[0][1][2]), 1)
		

regex = 'import (Commands|Plugins)\.\w+'

command = Command(regex, run)
