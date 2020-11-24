import discord
import youtube_dl

from discord import utils
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
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

ydl_opts = {
    'format': 'bestaudio/best',
  	'outtmpl': 'c:/Songs_download/%(title)s.%(ext)s', # <--- pay attention here
    'download_archive': 'downloaded_songs.txt',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        #'preferredquality': '192',
        }],
    #'logger': MyLogger(),
    #'progress_hooks': [my_hook],

}

def my_hook(d):
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {}".format(file_tuple[1]))
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])

class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name="trying to do her best"))
	print('Logged on as {0}!'.format(client.user))



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
	

#youtube music commands
@client.command(aliases = ['pyou', 'py', 'playyoutube'],name = 'pyou, py, playyoutube', help = 'Запустить проигрывание ютуб видео по ссылке')
async def pyou(ctx, url):
	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
	voice = utils.get(client.voice_clients, guild=ctx.guild)

	if not voice.is_playing():
		with YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(url, download=False)
		URL = info['formats'][0]['url']
		voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
		voice.is_playing()
	else:
		await ctx.send("Already playing song")
		return

#youtube music pause
@client.command()
async def pausey(ctx):
	voice = utils.get(client.voice_clients,guild=ctx.guild)
	if voice and voice.is_playing():
		print("Bot is playing")
		voice.pause()
		await ctx.send("⏸️")
	else:
		print("Nothing is playing")
		await ctx.send("Ошибка, нет текущей песни")

@client.command()
async def resumey(ctx):
	voice = utils.get(client.voice_clients,guild=ctx.guild)
	if voice and voice.is_paused():
		print("Resume music")
		voice.resume()
		await ctx.send("🔃")
	else:
		print("Nothing is playing")
		await ctx.send("Ошибка, нет текущей песни")

#youtube music skip
@client.command()
async def skipy(ctx):
	voice = utils.get(client.voice_clients,guild=ctx.guild)
	if voice and voice.is_playing() or voice.is_paused():
		print("Skip music")
		#voice.resume
		await ctx.send("⏭️")
	else:
		print("Nothing is playing")
		await ctx.send("Ошибка, что-то пошло не так")


@client.command(aliases = ['adder', 'addition', 'summ'],name = 'sum, adder, summ', help = 'Сложить два числа X Y')
async def _summ(ctx, arg1, arg2):
	await ctx.send(int(arg1)+int(arg2))





@client.command(name='clear', help = 'Удалениет заданное число сообщений')
@has_permissions(administrator=True)
async def clear(ctx, amount = 2):	
	print('deleted ' + str(amount) + ' message(s)')
	await ctx.channel.purge(limit=amount)	
	

@clear.error
async def clear_error(error, ctx):
	if isinstance(error, MissingPermissions):
		print("error")
		await ctx.send("Извините, вы не можите использовать эту команду. Необходимо иметь права администратора")


#if ctx.message.author.server_permissions.administrator:
#else:
	#	await ctx.send("Извините, вы не можите использовать эту команду. Необходимо иметь права администратора")

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








