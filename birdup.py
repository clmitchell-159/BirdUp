import discord
import csv
import re
import subprocess
import time as time
import datetime as datetime

global BIRDUP
global hcs
global timeSummon
global kittyCount

client = discord.Client()
BIRDUP = {}

def saveguilds():
	global BIRDUP
	with open("guildToggles.csv", 'w') as f:
		for key in BIRDUP:
			f.write('%s,%s,%s\n' % (key.id, BIRDUP[key][0], BIRDUP[key][1]))
			
			
def logAddReaction(text1, message):
	with open('log.txt', 'a') as f:
		f.write("%s for user '%s' in guild '%s' in channel '%s' at '%s'\n" % (text1, message.author.name, message.guild.name, message.channel, message.created_at.strftime("%m-%d-%Y %H:%M:%S")))
	print("%s for user '%s' in guild '%s' in channel '%s' at '%s'" % (text1, message.author.name, message.guild.name, message.channel, message.created_at.strftime("%m-%d-%Y %H:%M:%S")))


def common_data(list1, list2): 
    result = False
    # traverse in the 1st list 
    for x in list1: 
        # traverse in the 2nd list 
        for y in list2: 
            # if one common 
            if x == y: 
                result = True
                return result  
                  
    return result 


@client.event
async def on_message(message):
	#vars
	global BIRDUP
	global hcs
	tbcAllowedRoles = ["Fam", "Cool Kids"]
	tbcBlacklist = ["Green Cat"]
	usrRoles =[]
	for roll in message.author.roles:
		usrRoles.append(roll.name)
                
	#add known guild if necessary
	if message.guild not in BIRDUP:
		BIRDUP[message.guild] = [True, False]

        #do nothing if message is the bot's
	if message.author == client.user:
		if "RAID" in message.content and "SotP" in message.content and "SoS" in message.content:
			await message.add_reaction("🎊")#SotP
			await message.add_reaction("🐠")#LW
			await message.add_reaction("🌎")#EoW
			await message.add_reaction("🐋")#Levi
			await message.add_reaction("💩")#SoS
			await message.add_reaction("👑")#CoS
			await message.add_reaction("💮")#GoS
		if "Now:" in message.content and "Later Today:" in message.content:
			await message.add_reaction(discord.utils.get(hcs.emojis, name='birdup'))
			await message.add_reaction(discord.utils.get(hcs.emojis, name='one_one'))
			await message.add_reaction(discord.utils.get(hcs.emojis, name='two_two'))
			await message.add_reaction(discord.utils.get(hcs.emojis, name='four_four'))
			await message.add_reaction("⏰")
			await message.add_reaction("🤙")

		return
	
	#greenCount
	if (message.author.id == idRemoved and "kitty" in message.content.lower()) or (message.author.id == idRemoved or message.author.guild_permissions.administrator):
		global kittyCount
		global timeSummon
		if message.author.id == idRemoved:
			kittyCount = kittyCount + 1
		if (kittyCount % 10 == 0 and message.author.id == idRemoved) or message.content.lower().startswith("!birdkitty"):
			delta = datetime.datetime.now() - timeSummon
			await message.channel.send("Greeny Has Mentioned His Kitty " + str(kittyCount) + " times since the bot has restarted. (" + str(delta) + ")")

	


	#turn bot off in guild
	if message.content.startswith('!birdoff'):
		logAddReaction("BirdOff!", message)
		BIRDUP[message.guild] = [False, False]
		await message.channel.send( ':(')
	
	#turn selective mode on
	elif message.content.startswith('!birdup'):
		logAddReaction("BirdOn!", message)
		BIRDUP[message.guild][0] = True
		await message.channel.send( 'BIRDUP!')
	
	#turn all on
	elif (message.content.startswith('!birdall')):
		emoji = discord.utils.get(hcs.emojis, name='birdup')
		if message.guild.id == idRemoved:
			if ((message.author.name not in tbcBlacklist) and (('Fractal' in message.author.name) or ("Cool Kids" in usrRoles or "fam" in usrRoles)) and ("green" not in usrRoles)):
				logAddReaction("BirdAll!", message)
				BIRDUP[message.guild][1] = not BIRDUP[message.guild][1];
				await message.channel.send( 'BIRDALL!')
				await message.add_reaction(emoji)
		elif ('Fractal' in message.author.name):
			logAddReaction("BirdAll!", message)
			BIRDUP[message.guild][1] = not BIRDUP[message.guild][1];
			await message.channel.send( 'BIRDALL!')
			await message.add_reaction(emoji)
		
	#if all is on, add emoji reaction
	elif BIRDUP[message.guild][1] == True:
		logAddReaction("BirdUp!", message)
		emoji = discord.utils.get(hcs.emojis, name='birdup')
		await message.add_reaction(emoji)
	
	#if selective mode, add if condition is met
	elif ((BIRDUP[message.guild][0]) or (BIRDUP[message.guild][1])):
		if ((':birdup:' not in message.content.lower()) and (';birdup;' not in message.content.lower())) and (('birdup' in message.content.lower()) or ('bird up' in message.content.lower())):
			logAddReaction("BirdUp!", message)
			emoji = discord.utils.get(hcs.emojis, name='birdup')
			await message.add_reaction(emoji)
		if (message.content.lower() == "f" or message.content.lower().startswith('f ')):
			logAddReaction("F", message)
			emoji = discord.utils.get(hcs.emojis, name='ff')
			await message.add_reaction(emoji)
	
	#shutdown
	if (message.content.startswith('!birdshutdown') and (('Fractal' in message.author.name) or ('Bots' in message.author.roles))):
		saveguilds() 
		logAddReaction("Shutdown", message)
		await message.channel.send( 'Good Bye')
		raise SystemExit('Stopped by user: %s' % message.author.name)
	
	#update guild file
	if message.content.startswith('!birdsave'):
		saveguilds()
		logAddReaction("Update", message)
		await message.channel.send( 'Done')
	
	#send status
	if message.content.startswith('!birdstatus'):
		logAddReaction("Status", message)
		await message.channel.send( "Status of BirdUp in '%s':\nSelective: %s\nAll: %s" % (message.guild.name, BIRDUP[message.guild][0], BIRDUP[message.guild][1]))

    #send help
	if message.content.startswith('!birdhelp'):
		logAddReaction("Help", message)
		await message.channel.send( "Status of BirdUp in '%s':\nSelective: %s\nAll: %s" % (message.guild.name, BIRDUP[message.guild][0], BIRDUP[message.guild][1]))
		await message.channel.send( "Commands:\n!birdoff: Turn Bot Off (ish)\n!birdup: Turn Selective Mode On\n!birdall: Turn All Mode On (Restricted)\n!birdstatus: Get Status of the Bot\n!birdroles: view your roles\n!birdjail [name]: toggle Baby Jail role for user who's discord name (not nickname) begins with [name] (Restricted)\n!birdraid: summons the bird raid\n\nOther:\nFigure it out (WIP)")
	
	#view roles
	if message.content.startswith("!birdroles"):
		logAddReaction("Roles", message)
		listOfRoles = ""
		for roleAb in message.author.roles:
			role = roleAb.name
			if "@everyone" not in role:
				#+ ":" + str(roleAb.id) + 
				listOfRoles = listOfRoles + role + "\n"
		await message.channel.send("Roles for "+message.author.name+":\n"+listOfRoles)

	#destiny raid
	if re.search("r+a+i+d+\?", message.content.lower()) or message.content.startswith("!birdraid") or message.guild.id == idRemoved:
		destMentioned = False
		if message.content.startswith("!birdraid"):
			destMentioned = True
		for role in message.role_mentions:
			if "destin" in role.name.lower() or "raids" in role.name.lower():
				destMentioned = True
		if destMentioned:
			logAddReaction("Raid", message)
			await message.channel.send("\n╔══════════════╗\n║                 RAID                 ║\n╚══════════════╝\nSotP:     :confetti_ball:\nLW:      :tropical_fish: \nEoW:   :earth_americas: \nLevi:     :whale2:\nSoS:     :poop:\nCoS:	:crown:\nGoS:	:white_flower:")
			await message.channel.send("\n╔══════════════╗\n║                 TIME                 ║\n╚══════════════╝\nNow: <:birdup:562306087823474689>\n1 hr: :one:\n2 hr: :two:\n4 hr: :four:\nLater Today: :alarm_clock:\nAnytime Today: :call_me:")
			await message.channel.send("\n╔══════════════╗\n║                   <:birdup:562306087823474689>                  ║\n╚══════════════╝")

	#ipaddress
	if message.content.startswith("!birdip") and 'Fractal' in message.author.name:
		arg='ip route list'
		p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
		data=p.communicate()
		data=str(data[0])[1:]
		split_data=data.split(' ')
		ipaddr=split_data[split_data.index('src')+1]
		my_ip='Good day human overlord. This is your humble pi. My ip today is %s' % ipaddr
		await message.channel.send(my_ip)

	#gayBaby
	if message.content.startswith("!birdjail"):
		canJail = message.author.guild_permissions.administrator or 'Fractal' in message.author.name
		lessCool = message.guild.get_role(idRemoved)
		for role in message.author.roles:
			if (role == lessCool):
				canJail = True
		if canJail:
			usrs = []
			for usr in message.guild.members:
				if usr.name.lower().startswith(message.content.split(" ")[1].lower()):
					usrs.append(usr)
			if len(usrs) > 1:
				msg = "Found more than one user:\n"
				for usr in usrs:
					msg = msg + usr.name + "\n"
				msg = msg + "Please be more specific."
				await message.channel.send(msg)
			elif len(usrs) == 0:
				await message.channel.send("No Users Whose Name Begins with " + message.content.split(" ")[1] + " Found")
			else:
				for role in usrs[0].roles:
					if "baby jail" in role.name.lower():
						await usrs[0].remove_roles(role)
						logAddReaction("Remove Baby Jail From " + usrs[0].name, message)
						await message.channel.send("Removed " + usrs[0].name + " From Baby Jail")
						return
				await usrs[0].add_roles(message.guild.get_role(idRemoved))
				logAddReaction("Put " + usrs[0].name + " In Baby Jail", message)
				await message.channel.send("Put " + usrs[0].name + " In Baby Jail")
				return
		else:
			await message.channel.send("You Cannot Jail People")
	
	#DAVE
	if message.content.startswith("!birdclown"):
		canClown = message.author.guild_permissions.administrator or 'Fractal' in message.author.name
		lessCool = message.guild.get_role(idRemoved)
		for role in message.author.roles:
			if (role == lessCool):
				canClown = True
		if canClown:
			usrs = []
			for usr in message.guild.members:
				if usr.name.lower().startswith(message.content.split(" ")[1].lower()):
					usrs.append(usr)
			if len(usrs) > 1:
				msg = "Found more than one user:\n"
				for usr in usrs:
					msg = msg + usr.name + "\n"
				msg = msg + "Please be more specific."
				await message.channel.send(msg)
			elif len(usrs) == 0:
				await message.channel.send("No Users Whose Name Begins with " + message.content.split(" ")[1] + " Found")
			else:
				for role in usrs[0].roles:
					if "clown of" in role.name.lower():
						await usrs[0].remove_roles(role)
						logAddReaction("Declowned " + usrs[0].name, message)
						await message.channel.send(usrs[0].name + " is no longer a clown")
						return
				await usrs[0].add_roles(message.guild.get_role(idRemoved))
				logAddReaction("Clowned " +usrs[0].name, message)
				await message.channel.send(usrs[0].name + " is now a clown")
				return
		else:
			await message.channel.send("You Cannot Clown People")

	#if ":sex" in message.content.lower() and (message.guild.id == idRemoved or message.guild.id == idRemoved):
	#	await message.channel.send("You cannot say that - rule 9")
	#	await message.delete()

	#image size checker
	if (len(message.attachments) > 0 and message.channel.id == idRemoved and message.content.lower().startswith("hey alfred, emote add")):
		msg = "It looks like you are trying to add an emoji! However:\n"
		send = False
		if (message.attachments[0].size > 256000):
			msg = msg + "The max file size is 256kb, and your image is " + str(message.attachments[0].size/1000) + "kb\n"
			send = True
		pattern = re.compile("\W")
		matched = pattern.search(message.content[22:])
		if (matched):
			msg = msg + "Only alphanumeric & undersocre characters allowed in emoji names."
			send = True
		if send:
			await message.channel.send(msg)


				
		
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	await client.change_presence(activity=discord.Game('BirdUp!'))
	global hcs
	hcs = client.get_guild(idRemoved)
	global BIRDUP
	with open("guildToggles.csv", 'r') as f:
		for k,v,x in csv.reader(f):
			BIRDUP[client.get_guild(int(k))]=[v,x]
	print('-------------')
	global timeSummon
	global kittyCount
	kittyCount = 0
	timeSummon = datetime.datetime.now()
	
	
try:
	token = ''
	with open("token.txt", 'r') as f:
		token = f.readline()
	client.run(token)
except (KeyboardInterrupt, SystemExit, AttributeError, ValueError):
	print('exiting...')
finally:
	saveguilds()
	client.logout()
	
