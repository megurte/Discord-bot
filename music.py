import discord
from discord import utils

from discord.ext import commands
from discord.voice_client import VoiceClient

from random import choice

client = commands.Bot(command_prefix='!')

status = ['Supporting!', 'Eating!', 'Sleeping!']


@client.event
async def on_ready():
	print('Logged on as Lulu-support#3215!') 


@client.command(name = 'hello', help = 'Поприветствовать бота')
async def hello(ctx):
	responses = ['Привет, создатель!', 'Добро пожаловать', 'こんにちは～～', 'こんばんは、みんなさん', 'おかえりなさいご主人']
	print("hello")
	await message.channel.send(choice(responses))


@client.command(name = 'ping', help = 'Пропинговать бота')
async def ping(ctx):
	print(f'**Pong!** Latency: {round(client.latency * 1000)}ms')
	await message.channel.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')


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
	
@client.command(name = 'summ', help = 'Сложить два числа X Y')
async def summ(ctx, arg1, arg2):
	await ctx.send(int(arg1)+int(arg2))




@client.event
async def on_message( message):
		
	if message.content == 'Бот - молодец':
			await message.channel.send('Спасибо! ❤️')
	await client.process_commands(message)



client.run('Nzc5NDUzOTEyMzE0OTM3Mzg0.X7gxBg.bJgS45rEljUU_GXGXKnjpctoKR8')