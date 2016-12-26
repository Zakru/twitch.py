# -*- coding: utf-8 -*-

import socket, string
import array

HOST = "irc.chat.twitch.tv"
PORT = 6667

class ReceivedData():
	
	data_type = "NORMAL"
	user = ""
	
	def __init__(self, data_type, user):
		self.data_type = data_type
		self.user = user

class MessageData():
	"""
	Class used to contain a message's text and sender's name
	"""
	content = ""
	user = ""
	
	def __init__(self, content, user):
		self.content = content
		self.user = user

class TwitchSocket():
	
	def __init__(self, host, port, debug=False):
		self.channel = ""
		self.debug = debug
		
		self._socket = socket.socket()
		self._socket.connect((host, port))
		self._ready = False
		self._events = {"on_ready":None,"on_receive":None,"on_message":None}
		self._prefix = "!"
		
		self._buffer = ""
	
	def read(self, size=1024, print_content=False):
		"""
		Read UTF-8 data from socket to buffer.
		"""
		self._buffer = self._buffer + str(self._socket.recv(size), 'utf-8')
		
		if (print_content):
			print (self._buffer)
	
	def next_line(self):
		self.read(print_content=self.debug)
		lines = self._buffer.split("\n")
		
		self._buffer = lines.pop()
		
		self.parse_in(lines)
	
	def parse_in(self, lines):
		for line in lines:
			if (line[:4] == "PING"):
				# Tell Twitch we're active
				
				self.send("PONG {0}\r\n".format(line[1]))
				print ("Sent 'PONG'")
			else:
				# Hey, we received info!
				
				parts = line.split(":")
				
				# But what kind of data is it?
				if ("QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]):
					# Yup, it's definitely a user message
					
					try:
						message = parts[2][:-1]
					except:
						message = ""
					
					usernamesplit = parts[1].split("!")
					username = usernamesplit[0]
					
					if self._ready:
						print (username + ": " + message)
						self.call_event("on_message", MessageData(message, username))
				elif ("JOIN" in parts[1]):
					# I think JOIN is for when someone joins the chat, but I've never seen it being sent.
					
					usernamesplit = parts[1].split("!")
					username = usernamesplit[0]
					self.call_event("on_recieve", ReceivedData("JOIN", username))
				
				for l in parts:
					if "End of /NAMES list" in l:
						# When received message above, tell everything the connection is open.
						
						self._ready = True
						self.call_event("on_ready")
	
	def send(self, message):
		"""
		Convert raw string data into a bytes and send it
		"""
		
		self._socket.send(bytes(message, 'utf-8'))
		print ("[SENT] " + message)
	
	def send_message(self, message):
		"""
		Convert message into raw data for Twitch to understand it
		"""
		
		self.send("PRIVMSG #" + self.channel + " :" + message + "\r\n")
	
	def login(self, name, password):
		"""
		Send Twitch login credentials
		"""
		
		self.send("PASS " + password + "\r\n")
		self.send("NICK " + name + "\r\n")
	
	def join(self, channel):
		"""
		Tell Twitch which channel you want to communicate with
		"""
		
		self.channel = channel
		self.send("JOIN #" + channel + "\r\n")
	
	def event(self, func):
		"""
		Decorator to add an event to the _events list
		"""
		
		if (func.__name__ in self._events):
			self._events[func.__name__] = func
		else:
			raise NameError("No event exists with the name '{0}'".format(func.__name__));
		return func
	
	def call_event(self, event, *args, **kwargs):
		if (event in self._events and self._events[event] != None):
			return self._events[event](*args, **kwargs)
