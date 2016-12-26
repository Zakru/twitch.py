import twitch

bot = twitch.Bot()

@bot.event
def on_ready():
	bot.send_message("Running EgBot v6.9")

@bot.event
def on_message():
	bot.send_message("Why would you say that?")

@bot.command
def egg():
	bot.send_message("I laid an egg!!!")

bot.run("username", "oauth:passwordjnvbpuiehnafdaiuhvnurs", "channel")
