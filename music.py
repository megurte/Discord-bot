import discord
from discord import utils

from discord.ext import commands
from discord.voice_client import VoiceClient

from random import choice

client = commands.Bot(command_prefix='!')

help_text = {
	'!hello - Поприветствовать бота \n'
	'!ping - Пропинговать бота \n'
	'!join - Подключить бота к голосовому каналу \n'
	'!leave - Отключить бота из голосового канала \n'
}


@client.event
async def on_ready():
	print('Logged on as Lulu-support#3215!') 


@client.command(name = join)
async def join(ctx):
	if not ctx.message.author.voice:
		await ctx.send("You are not connected to a voice channel")
		return

	else:
		channel = ctx.message.author.voice.channel

	await channel.connect()

@client.command()
async def leave(ctx):
	voice_client = ctx.message.guild.voice_client
	await voice_client.disconnect()
	
@client.command()
async def foo(ctx, arg1,arg2):
	print("foo")
	await ctx.send(arg1+arg2)

@client.command()
async def help(ctx):
	await 


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