import discord
from discord import utils
 
import config


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_raw_reaction_add(self, payload):
    	channel = self.get_channel(payload.channel_id)
    	message = await channel.fetch_message(payload.message_id)
    	member = utils.get(message.guild.members, id=payload.user_id)


    try:
    	emoli = str(payload.emoji)
    	role = utils.get(message.guild.roles, id= config.ROLES[emoji])

    	if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
    		await member.add_roles(role)
    		print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
    	else:
    		await message.remove_reaction(payload.emoji, member)
    		print('[ERROR] User {0.display_name} Too many roles for member {1.name}'.format(member, role))


    except KeyError as e:
    	print('[ERROR] KeyError, no role found for ' + emoji)
    	

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) 
        message = await channel.fetch_message(payload.message_id) 
        member = utils.get(message.guild.members, id=payload.user_id) 
 
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) 
 
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
    	

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'Что ты умеешь?':
            await message.channel.send('Я пока ничего не умею')

        if message.content == 'Значит я тебя улучшу':
            await message.channel.send('Спасибо, создатель!')

        if message.content == 'test':
            await message.channel.send('test reply')

client = MyClient()
client.run('config.TOKEN')