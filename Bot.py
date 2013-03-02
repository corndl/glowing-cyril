# -*- coding: utf8 -*-

import irclib, ircbot, time, json, argparse, os
import sys

class Bot(ircbot.SingleServerIRCBot) :
	def __init__ (self) :
		self._default_path_to_config_file = 'config.json'
		self._path_to_config_file = ''
		self._log_file = ''
		self.plugins = []
		self.commands = []
		self.verbosity = False
		self.logging = False
		self.getArgs()
		self.getConfig()
		self.getModules('plugins')
		self.getModules('commands')
		ircbot.SingleServerIRCBot.__init__(self, [(self._config['server'], 
			self._config['port'])], self._config['nick'], self._config['name'])
		self.log('Running')

	def getConfig (self) :
		"""Reads values such as nick or pw from a json file. If no config file
		is specified, or if it is an incorrect one, values will be read from a
		default config file."""
		try :
			self._config = json.load(open(self._path_to_config_file))
			self.log('Getting config, opening %s' % self._path_to_config_file)
		except (AttributeError, IOError) :
			self._config = json.load(open(self._default_path_to_config_file))
			if self._path_to_config_file : 
				self.log('Failed to open config file %s, resorting to default.'
						% self._path_to_config_file)
		self.nick = self._config['nick']
		self.password = self._config['password']
		self.name = self._config['name']
		self.port = self._config['port']
		self.server = self._config['server']
		self.channels = self._config['channels']

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
			self._path_to_config_file = args.c 

	def importModule(self, name) :
		"""Loads a module from a package. """
		mod = __import__(name)
		components = name.split('.')
		for comp in components[1:] :
			mod = getattr(mod, comp)
		return mod

	def getModules(self, package) :
		"""Loads a list of modules (plugins or commands) read from the config 
		file. They must be located in the Plugins and Commands packages."""
		for module in self._config[package] :
			try :
				if package == "plugins" :
					m = self.importModule('Plugins.' + module)
					self.plugins.append(m)
				if package == "commands" :
					m = self.importModule('Commands.' + module)
					self.commands.append(m)
			except (ImportError) :
				self.log('Couldn\'t import %s' % module)

	def reloadModules(self) :
		for m in self.plugins :
			self.log(m)
			reload(m)
		for m in self.commands :
			self.log(m)
			reload(m)
		self.log('Reloaded')

	def log(self, message) :
		"""Prints log messages to stdout if verbosity is on, and to a log file 
		if logging is on."""
		dt = list(time.localtime())
		if dt[3] < 10 :
			dt[3] = '0%s' % dt[3]
		if dt[4] < 10 :
			dt[4] = '0%s' % dt[4]
		if dt[5] < 10 :
			dt[5] = '0%s' % dt[5]
		message = '%s:%s:%s, %s/%s/%s : %s' % (dt[3], dt[4], dt[5], dt[2], dt[1], dt[0], message)
		
		if self.verbosity :
			print message

		if self.logging :
			directory = 'logs'
			if not os.path.exists(directory) :
				os.makedirs(directory)
			if not self._log_file :
				self._log_file = '%s-%s-%s_%s:%s:%s' % (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
			path_to_log_file = os.path.join(directory, self._log_file)
			f = open(path_to_log_file, 'w')
			f.write(message)
			f.close()

	def identify(self, serv) :
		serv.privmsg('NickServ', 'identify ' + self.password)

	def on_welcome(self, serv, ev) :
		self.log('Connected')
		self.identify(serv)
		for channel in self._config['channels'] :
			serv.join(channel)
			if self._config['join_message'] :
				serv.privmsg(channel, self._config['join_message'])
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
			p.plugin.run(self, serv, ev) 

	def on_privmsg(self, serv, ev) :
		source = irclib.nm_to_n(ev.source())
		message = ev.arguments()[0]
		user = irclib.nm_to_h(ev.source())
		self.log(user)
		if user in self._config['admins'] :
			for c in self.commands :
				c.command.run(self, serv, ev)

	def join(self, serv, chan, source) :
		serv.join(chan)
		source_nick = irclib.nm_to_n(source)
		self.log('Joined %s - command used by %s (%s)' % (chan, source_nick, source))

	def part(self, serv, chan, source) :
		serv.part(chan)
		source_nick = irclib.nm_to_n(source)
		self.log('Left %s - command used by %s (%s)' % (chan, source_nick, source))

if __name__ == "__main__" :
	try :
		Bot().start()
	except KeyboardInterrupt :
		dt = list(time.localtime())
		message = '%s:%s:%s, %s/%s/%s : %s' % (dt[3], dt[4], dt[5], dt[2], dt[1], 
				dt[0], 'User aborted the program.')
		print message
