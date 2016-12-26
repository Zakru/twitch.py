# -*- coding: utf-8 -*-

import asyncio
from .twitchsocket import TwitchSocket, HOST, PORT

class Bot:
	
	def __init__(self, command_prefix="!", loop=None, debug=False, *args, **kwargs):
		"""
		Initializes the bot
		"""
		self.loop = asyncio.get_event_loop() if loop is None else loop
		self.name = ""
		# Events are called through the call_event() method
		self._events = {"on_ready":None,"on_join":None,"on_message":None,"on_command":None}
		self.command_prefix = command_prefix
		self._commands = {}
		
		self._socket = TwitchSocket(HOST, PORT, debug=debug)
		
		@self._socket.event
		def on_ready():
			"""
			Called when socket receives "End of /NAMES list"
			"""
			self.call_event("on_ready")
		
		@self._socket.event
		def on_receive(received_data):
			"""
			The socket doesn't ever seem to receive a JOIN message,
			so this event is basically useless.
			"""
			if (received_data.data_type == "JOIN" and received_data.user == self.name):
				self.call_event("on_join")
		
		@self._socket.event
		def on_message(message):
			"""
			Called when socket receives a user message.
			If its first character is command_prefix,
			calls on_command event from _events. Otherwise
			calls on_message.
			"""
			if (message.content[0] == self.command_prefix):
				self.call_event("on_command", message)
			else:
				self.call_event("on_message", message)
		
		@self.event
		def on_command(message):
			"""
			Default on_command event. If overwritten,
			must include this line for normal command
			parsing to work.
			"""
			self.parse_commands(message)
	
	def login(self, name, password):
		"""
		Call socket's login function with the same
		arguments.
		"""
		self._socket.login(name, password)
	
	def join(self, channel):
		"""
		Call socket's join function with the same
		arguments.
		"""
		self._socket.join(channel)
	
	def run(self, name, password, channel):
		"""
		Combines login() and join() and starts running
		the main event loop.
		"""
		self.name = name
		self.login(name, password)
		self.join(channel)
		
		try:
			self.loop.run_until_complete(self.main_loop())
		except KeyboardInterrupt:
			pending = asyncio.Task.all_tasks()
			gathered = asyncio.gather(*pending)
			try:
				gathered.cancel()
				self.loop.run_until_complete(gathered)
				
				gathered.exception()
			except:
				pass
		finally:
			self.loop.close()
	
	def parse_commands(self, message):
		"""
		Checks if the first part (separated by spaces) of a
		message (command 'name') without command_prefix is in
		the _commands list. If a key of that name is present,
		runs the function under that key.
		"""
		command = message.content[1:].split('!')[0]
		parts = command.split(' ')
		name = parts[0]
		args = parts[1:]
		if (name in self._commands):
			try:
				self._commands[name](*args)
			except TypeError:
				self.send_message("Wrong number of arguments for command '{0}'".format(name))
	
	@asyncio.coroutine
	def main_loop(self):
		while True:
			self._socket.next_line()
	
	def event(self, func):
		"""
		Decorator for adding events to the _events list.
		"""
		if (func.__name__ in self._events):
			self._events[func.__name__] = func
		else:
			raise NameError("No event called '{0}'".format(func.__name__));
		return func
	
	def call_event(self, event, *args, **kwargs):
		"""
		Calls an event from the _events list.
		"""
		if (event in self._events and self._events[event] != None):
			return self._events[event](*args, **kwargs)
	
	def command(self, func):
		"""
		Decorator for adding commands to the _commands list
		"""
		self._commands[func.__name__] = func
	
	def send_message(self, message):
		"""
		Calls _socket.send_message()
		"""
		self._socket.send_message(message)
