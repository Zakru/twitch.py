# -*- coding: utf-8 -*-

import twitch

bot = twitch.Bot()

@bot.command
def muni_muna():
	bot.send_message("Munin kananmunan!!!")

bot.run("bigbotter", "oauth:uvjquibld98048bldlc3zryzum1dm6", "redlight01")
