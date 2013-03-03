import re

class Command :
	def __init__(self, regex, action) :
		self.regex = regex
		self.action = action
		
	def run(self, bot, serv, ev) :
		message = ev.arguments()[0]
		result = re.match(self.regex, message)
		if result :
			self.action(bot, serv, ev)
