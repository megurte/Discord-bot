import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'Добро пожаловать, бот':
            await message.channel.send('Наконец я заработала')

        if message.content == 'Что ты умеешь?':
            await message.channel.send('Я пока ничего не умею')

        if message.content == 'Значит я тебя улучшу':
            await message.channel.send('Спасибо, создатель!')

        if message.content == 'test':
            await message.channel.send('test reply')

client = MyClient()
client.run('Nzc5NDUzOTEyMzE0OTM3Mzg0.X7gxBg.bJgS45rEljUU_GXGXKnjpctoKR8')