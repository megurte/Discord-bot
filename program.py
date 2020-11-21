import discord
from discord import utils
 
import config
 
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
 
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == POST_ID:
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=ROLES[emoji]) # объект выбранной роли (если есть)
            
            if(len([i for i in member.roles if i.id not in EXCROLES]) <= MAX_ROLES_PER_USER):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
 
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == POST_ID:
        	channel = self.get_channel(payload.channel_id) # получаем объект канала
        	message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        	member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=ROLES[emoji]) # объект выбранной роли (если есть)
 
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

TOKEN = 'Nzc5NDUzOTEyMzE0OTM3Mzg0.X7gxBg.bJgS45rEljUU_GXGXKnjpctoKR8'

POST_ID = 779621202242306058

ROLES = {
	'🥐': 276393911771987968, #Чебурек
	'🚶‍♂️': 276394311136837633, #no-name-role
	#'😀': 361495636480098306, #naci
	'🏳️‍🌈': 364081386715480077, #homo
}

EXCROLES = ()

MAX_ROLES_PER_USER = 6 

client = MyClient()
client.run(TOKEN)

