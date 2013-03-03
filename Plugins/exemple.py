#!/usr/bin/python

from Plugin import Plugin

def run(bot, serv, ev) :
	pass

REGEX = '.'
REGEXES_RUN = { REGEX : run }
plugin = Plugin(REGEXES_RUN)

if __name__ == '__main'__ :
	plugin.test('test', None)
