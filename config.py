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


if message.content == '!join':
			if not member.message.author.voice:
				await member.send("You are not connected to a voice channel")
				return
			else:
				channel = member.message.author.voice.channel
			print("connected")
			await channel.connect()

		if message.content == '!leave':
			voice_client = member.message.guild.voice_client
			print("leave")
			await voice_client.disconnect()	



class MyClient(discord.Client):

	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user)) 


	

	@client.command(name='ping', help='This command returns the latency')
	async def ping(ctx):
		print(f'**Pong!** Latency: {round(client.latency * 1000)}ms')
		await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')


	@client.command(name='hello', help='This command returns a random welcome message')
	async def hello(ctx):
		responses = ['Привет, создатель!', 'Добро пожаловать', 'こんにちは～～', 'こんばんは、みんなさん', 'おかえりなさいご主人']
		print("hello")
		await ctx.send(choice(responses))




	
			
		


	@client.event
	async def on_member_join(member):
		channel = utils.get(member.guild.channels, name='general')
		await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')





		
	client = commands.Bot(command_prefix='!')

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