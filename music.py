import discord
from discord import utils

from discord.ext import commands
from discord.voice_client import VoiceClient

from random import choice

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready(self):
	print('Logged on as {0}!'.format(self.user)) 

@client.command()
async def join(ctx):
	print("join")
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send('успешно подключился')

@client.command()
async def leave(ctx):
	print("leave")
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await connect.channel()
		await ctx.send('успешно отключился')
	

@client.command()
async def foo(ctx, arg):
	print("foo")
	await ctx.send(arg)

@client.command()
async def hello(ctx):
	responses = ['Привет, создатель!', 'Добро пожаловать', 'こんにちは～～', 'こんばんは、みんなさん', 'おかえりなさいご主人']
	print("hello")
	await message.channel.send(choice(responses))

@client.command()
async def ping(ctx):
	print(f'**Pong!** Latency: {round(client.latency * 1000)}ms')
	await message.channel.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')



@client.event
async def on_message( message):
		
	
	await client.process_commands(message)



client.run('Nzc5NDUzOTEyMzE0OTM3Mzg0.X7gxBg.bJgS45rEljUU_GXGXKnjpctoKR8')