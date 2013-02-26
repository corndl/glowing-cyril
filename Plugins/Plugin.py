import re
from random import randrange

class Plugin :
	def __init__(self, hash_regexes_actions) :
		self.regexes_actions = hash_regexes_actions
				
	def run(self, bot, serv, ev) :
		message = ev.arguments()[0]
		for regex in self.regexes_actions :
			result = re.match(regex, message)
			if result :
				self.regexes_actions[regex](bot, serv, ev)

	def test(self, message) :
		for regex in self.regexes_actions :
			result = re.match(regex, message)
			if result :
				self.regexes_actions[regex](None, Serv(), EvTest(message))

class EvTest :
	def __init__(self, message) :
		self.message = message
		self.chans = ['#corn']
		self.users = ['corn!defrance20@tic.iiens.net', 'Jojo!chapele20@tic.iiens.net']
	
	def arguments(self) :
		return [self.message]

	def source(self) :
		return self.users[randrange(len(self.users))]

	def target(self) :
		return self.chans[randrange(len(self.chans))]

class Serv() :
	def __init__(self) :
		pass

	def privmsg(self, chan, message) :
		self.prettyPrint(chan, message)

	def prettyPrint(self, chan, message) :
		print '%s : <Bot> %s' % (chan, message)
