import discord
import youtube_dl
import os
import shutil

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
VERSION = str ("1.1 ©Megurt")

play_emoji =str("▶️")
pause_emoji= str("⏸️")
resume_emoji = str("🔃")
stop_emoji = str("⏹")
skip_emoji = str("⏭️")
check_emoji = str("☑️")

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
@client.command(pass_context=True, aliases = ['pyou', 'py', 'playy'],name = 'playy, py, pyou', help = 'Запустить ютуб видео по ссылке')
async def playy(ctx, url: str):
	def check_queue():
		Queue_infile = os.path.isdir("./Queue")
		if Queue_infile is True:
			DIR = os.path.abspath(os.path.realpath("Queue"))
			length = len(os.listdir(DIR))
			still_q = length - 1
			try:
				first_file = os.listdir(DIR)[0]
			except:
				print("No more queued song(s)\n")
				queues.clear()
				return
			main_location = os.path.dirname(os.path.realpath(__file__))
			song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
			if length != 0:
				print("Song done, playing next queued\n")
				print(f"Songs still in queue: {still_q}")
				song_there = os.path.isfile("song.mp3")
				if song_there:
					os.remove("song.mp3")
				shutil.move(song_path, main_location)
				for file in os.listdir("./"):
					if file.endswith(".mp3"):
						os.rename(file, 'song.mp3')

				voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
				voice.source = discord.PCMVolumeTransformer(voice.source)
				voice.source.volume = 0.07

			else:
				queues.clear()
				return

		else:
			queues.clear()
			print("No songs were queued before the ending of the last song\n")

	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
			queues.clear()
			print("Removed old song file")
	except PermissionError:
		print("Trying to delete song file, but it's being played")
		await ctx.send("Ошибка, музыка уже играет")
		return

	Queue_infile = os.path.isdir("./Queue")
	try:
		Queue_folder = "./Queue"
		if Queue_infile is True:
			print("Removed old Queue Folder")
			shutil.rmtree(Queue_folder)
	except:
		print("No old Queue folder")

	await ctx.message.add_reaction(play_emoji)
	#await ctx.send("Getting everything ready now")

	voice = utils.get(client.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': True,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("Downloading audio now\n")
		ydl.download([url])

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			name = file
			print(f"Renamed File: {file}\n")
			os.rename(file, "song.mp3")

	voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	nname = name.rsplit("-", 2)
	await ctx.send(f"Играет: {nname[0]}")
	print("playing\n")




#	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#	voice = utils.get(client.voice_clients, guild=ctx.guild)

#	if not voice.is_playing():
#		with YoutubeDL(ydl_opts) as ydl:
#			info = ydl.extract_info(url, download=False)
#		URL = info['formats'][0]['url']
#		voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#		voice.is_playing()
#		await ctx.message.add_reaction(play_emoji)
#	else:
#		await ctx.send("Музыка уже играет")
#		return

#
queues = {}

@client.command(pass_context=True, aliases=['qy', 'quey'], help = "Добавить песню в очередь")
async def queuey(ctx, url: str):
	Queue_infile = os.path.isdir("./Queue")
	if Queue_infile is False:
		os.mkdir("Queue")
	DIR = os.path.abspath(os.path.realpath("Queue"))
	
	q_num = len(os.listdir(DIR))
	q_num += 1
	add_queue = True
	while add_queue:
		if q_num in queues:
			q_num += 1
		else:
			add_queue = False
			queues[q_num] = q_num

	queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': True,
		'outtmpl': queue_path,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			#'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("Downloading audio now\n")
		ydl.download([url])
	await ctx.message.add_reaction(check_emoji)
	await ctx.send("Добавлено " + str(q_num) + " в очередь")

	print("Song added to queue\n")




@client.command(name = 'pausey', help = 'Остановить проигрывание трека')
async def pausey(ctx):
	voice = utils.get(client.voice_clients,guild=ctx.guild)
	if voice and voice.is_playing():
		print("Bot is playing")
		voice.pause()
		#await ctx.("⏸️")
		await ctx.message.add_reaction(pause_emoji)
	else:
		print("Nothing is playing")
		await ctx.send("Ошибка, нет текущей песни")



@client.command(name = 'resumey', help = 'Возобновить проигрывание трека')
async def resumey(ctx):
	voice = utils.get(client.voice_clients,guild=ctx.guild)
	if voice and voice.is_paused():
		print("Resume music")
		voice.resume()
		await ctx.message.add_reaction(resume_emoji)
		#await ctx.send("🔃")
	else:
		print("Nothing is playing")
		await ctx.send("Ошибка, нет текущей песни")

#youtube music skip
@client.command(name = 'skipy', help = 'Пропустить текущий трек')
async def skipy(ctx):
	voice = utils.get(client.voice_clients,guild=ctx.guild)
	if voice and voice.is_playing():
		print("Skip music")
		voice.stop()
		#await ctx.send("⏹️")
		await ctx.message.add_reaction(skip_emoji)
	else:
		print("Nothing is playing")
		await ctx.send("Ошибка, нет текущей песни")




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








