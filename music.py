import discord
import youtube_dl
from discord import utils

from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
from discord.ext.commands import CheckFailure
from discord.voice_client import VoiceClient

from random import choice

client = commands.Bot(command_prefix='!')
POST_ID = 779692750941323264
ROLES = {
	'🥐': 276393911771987968, #Чебурек
	'🚶‍♂️': 276394311136837633, #no-name-role
	'🏳️‍🌈': 364081386715480077, #homo
}
EXCROLES = ()

players = {}

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name="trying to do her best"))
	print('Logged on as Lulu-support#3215!') 


@client.command(name = 'hello', help = 'Поприветствовать бота')
async def hello(ctx):
	author = ctx.message.author
	responses = [f'Привет, {author.mention}! ', f'Добро пожаловать, {author.mention}', 'Добра тебе!']
	print("hello")
	await ctx.send(choice(responses))


@client.command(name = 'ping', help = 'Пропинговать бота')
async def ping(ctx):
	print(f'**Pong!** Latency: {round(client.latency * 1000)}ms')
	await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')


@client.command(name = 'join', help = 'Подключить бота к голосовому каналу')
async def join(ctx):
	if not ctx.message.author.voice:
		await ctx.send("Вы не в войс канале")
		return
	else:
		channel = ctx.message.author.voice.channel
	await channel.connect()


@client.command(name = 'leave', help = 'Отключить бота из голосового канала')
async def leave(ctx):
	voice_client = ctx.message.guild.voice_client
	await voice_client.disconnect()
	

@client.command(aliases = ['py', 'playyoutube', 'play_youtube'],name = 'pyou', help = 'Запустить проигрывание ютуб видео')
async def pyou(ctx, url):
	#guild = ctx.message.guild
	#voice_client = client.voice_client_in(guild)
	voice_client = ctx.guild.voice_client
	player = await voice_client.create_ytdl_player(url)
	players[server.id] = player
	player.start()



@client.command(aliases = ['adder', 'addition', 'summ'],name = 'sum', help = 'Сложить два числа X Y')
async def _summ(ctx, arg1, arg2):
	await ctx.send(int(arg1)+int(arg2))





@client.command(name='clear')
@has_permissions(administrator=True)
async def clear(ctx, amount = 2):
	if ctx.message.author.guild_permissions.administrator:
		print('deleted ' + str(amount) + ' message(s)')
		await ctx.channel.purge(limit=amount)	
	else:
		await ctx.send("Извините, вы не можите использовать эту команду. Необходимо иметь права администратора")











#add role	
@client.event
async def on_raw_reaction_add(payload):
	if payload.message_id == POST_ID:
		channel = client.get_channel(payload.channel_id) 
		message = await channel.fetch_message(payload.message_id) 
		member = utils.get(message.guild.members, id=payload.user_id) 
 		
	try:
		emoji = str(payload.emoji) # эмоджик который выбрал юзер
		role = utils.get(message.guild.roles, id=ROLES[emoji]) # объект выбранной роли (если есть)

		await member.add_roles(role)
		print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
			
	except KeyError as e:
		print('[ERROR] KeyError, no role found for ' + emoji)
	except Exception as e:
		print(repr(e))
	

#remove role	
@client.event
async def on_raw_reaction_remove(payload):
	if payload.message_id == POST_ID:
		channel = client.get_channel(payload.channel_id) 
		message = await channel.fetch_message(payload.message_id) 
		member = utils.get(message.guild.members, id=payload.user_id) 

	try:
		emoji = str(payload.emoji) # эмоджик который выбрал юзер
		role = utils.get(message.guild.roles, id=ROLES[emoji]) # объект выбранной роли (если есть)

		await member.remove_roles(role)
		print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
	except KeyError as e:
		print('[ERROR] KeyError, no role found for ' + emoji)
	except Exception as e:
		print(repr(e))


@client.event
async def on_message(message):		
	if message.content == 'Бот - молодец':
		await message.channel.send('Спасибо! ❤️')
	if message.content == 'Бот, пока':
		await message.channel.send(f'До встречи, {message.author.mention}!')
	if message.content == 'Спокойной ночи, бот':
		await message.channel.send(f'Спокойной ночи, {message.author.mention}! Теплых снов ❤️')
	if message.content == 'Спасибо, бот':
		await message.channel.send(f'Всегда рада помочь!')
	await client.process_commands(message)



#@clear.error
#async def clear_error(error, ctx):
 #   if isinstance(error, CheckFailure):
 #       await ctx.send("Извините, вы не можите использовать эту команду. Необходимо иметь права администратора")

client.run('Nzc5NDUzOTEyMzE0OTM3Mzg0.X7gxBg.bJgS45rEljUU_GXGXKnjpctoKR8')








