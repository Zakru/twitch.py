# -*- coding: utf-8 -*-

import twitch

bot = twitch.Bot()

@bot.command
def egg():
	bot.send_message("I laid an egg!!!")

bot.run("username", "oauth:passwordjnvbpuiehnafdaiuhvnurs", "channel")
