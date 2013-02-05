# -*- coding: utf8 -*-

import irclib, ircbot, time, json, argparse, os
from sys import argv

class Bot(ircbot.SingleServerIRCBot) :
	def __init__ (self) :
		self.default_path_to_config_file = 'config.json'
		self.path_to_config_file = ''
		self.log_file = ''
		self.plugins = []
		self.commands = []
		self.verbosity = False
		self.logging = False
		self.getArgs()
		self.getConfig()
		self.getPlugins()
		ircbot.SingleServerIRCBot.__init__(self, [(self.config['server'], 
			self.config['port'])], self.config['nick'], self.config['name'])
		self.log('Running')

	def getConfig (self) :
		"""Reads values such as nick or pw from a json file. If no config file
		is specified, or if it is an incorrect one, values will be read from a
		default config file."""
		try :
			self.config = json.load(open(self.path_to_config_file))
			self.log('Getting config, opening %s' % self.path_to_config_file)
		except (AttributeError, IOError) :
			self.config = json.load(open(self.default_path_to_config_file))
			if self.path_to_config_file : 
				self.log('Failed to open config file %s, resorting to default.'
						% self.path_to_config_file)
		self.nick = self.config['nick']
		self.password = self.config['password']
		self.name = self.config['name']
		self.port = self.config['port']
		self.server = self.config['server']
		self.channels = self.config['channels']

	def getArgs(self) :
		"""Parses arguments : logging, verbosity, custom config file"""
		parser = argparse.ArgumentParser()
		parser.add_argument('-log', help = 'save logs', action = 'store_true')
		parser.add_argument('-v', help = 'display logs', action = 'store_true')
		parser.add_argument('-c', help = 'specify custom path to config file')
		args = parser.parse_args()
		if args.log :
			print 'Logging on'
			self.logging = True
		if args.v :
			print 'Verbosity on'
			self.verbosity = True
		if args.c :
			self.path_to_config_file = args.c 

	def importModule(self, name) :
		"""Loads a module from a package. """
		mod = __import__(name)
		components = name.split('.')
		for comp in components[1:] :
			mod = getattr(mod, comp)
		return mod

	def getPlugins(self) :
		"""Loads a list of plugins read from the config file. They must be located
		in the Plugins packag."""
		for plugin in self.config['plugins'] :
			try :
				p = self.importModule('Plugins.' + plugin)
				self.plugins.append(p)
			except (ImportError) :
				self.log('Couldn\'t import %s' % plugin)

	def getCommands(self) :
		"""Loads a list of commands read from the config file. They must be located
		in the Commands package."""
		for command in self.config['command'] :
			try :
				c = self.importModule('Commands.' + command)
				self.command.append(c)
			except (ImportError) :
				self.log('Couldn\'t import %s' % command)

	def log(self, message) :
		"""Prints log messages to stdout if verbosity is on, and to a log file 
		if logging is on."""
		dt = list(time.localtime())
		if dt[3] < 10 :
			dt[3] = '0%s' % dt[3]
		if dt[4] < 10 :
			dt[4] = '0%s' % dt[4]
		if dt[5] < 10 :
			dt[5] = '0%s' % dt[4]
		message = '%s:%s:%s, %s/%s/%s : %s' % (dt[3], dt[4], dt[5], dt[2], dt[1], dt[0], message)
		
		if self.verbosity :
			print message

		if self.logging :
			directory = 'logs'
			if not os.path.exists(directory) :
				os.makedirs(directory)
			if not self.log_file :
				self.log_file = '%s-%s-%s_%s:%s:%s' % (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
			path_to_log_file = os.path.join(directory, self.log_file)
			f = open(path_to_log_file, 'w')
			f.write(message)
			f.close()

	def identify(self, serv) :
		serv.privmsg('NickServ', 'identify ' + self.password)

	def on_welcome(self, serv, ev) :
		self.log('Connected')
		self.identify(serv)
		for channel in self.config['channels'] :
			serv.join(channel)
			if self.config['join_message'] :
				serv.privmsg(channel, self.config['join_message'])
			self.log('Joined %s' % channel)

	def on_join(self, serv, ev) :
		newcomer = irclib.nm_to_n(ev.source())
		channel = ev.target()

	def on_privnotice(self, serv, ev) :
		source = irclib.nm_to_n(ev.source())
		message = ev.arguments()[0]

	def on_pubmsg(self, serv, ev) :
		source = irclib.nm_to_n(ev.source())
		channel = ev.target()
		message = ev.arguments()[0]
		for p in self.plugins :
			result = p.plugin.run(serv, ev) 

	def on_privmsg(self, serv, ev) :
		source = irclib.nm_to_n(ev.source())
		message = ev.arguments()[0]
		for command in self.priv_commands :
			command(source, message)

if __name__ == "__main__" :
	try :
		Bot().start()
	except KeyboardInterrupt :
		dt = list(time.localtime())
		message = '%s:%s:%s, %s/%s/%s : %s' % (dt[3], dt[4], dt[5], dt[2], dt[1], 
				dt[0], 'User aborted the program.')
		print message
