import datetime

import disnake
from disnake.ext import commands


bot = commands.Bot(command_prefix=".", help_command=None, intents=disnake.Intents.all(), test_guilds=[id_вашего сервера])

bot.remove_command("help")

CENSORED_WORDS = ["...", "..."] #Сюда добавляем бан ворды

#Выводит в консоль готовность бота

@bot.event
async def on_ready():
	print(f"Бот {bot.user} готов к работе!")

#Бан ворды

@bot.event
async def on_message(message):
	await bot.process_commands(message)

	for content in message.content.split():
		for censored_word in CENSORED_WORDS:
			if content.lower() == censored_word:
				await message.delete()
				await message.channel.send(f"{message.author.mention} _Не используй недопустимые слова_")

#Кик

@bot.slash_command(description='Кикает участника')
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake. Member, *, reason="Нарушение правил."):
	await ctx.send(f"**Администратоp** {ctx.author.mention} **иcключил пользователя** {member.mention}", delete_after=1440)
	await member.kick(reason=reason)
	await ctx.message.delete()

#Калькулятор

@bot.slash_command()
async def calc(inter, a: int, oper: str, b: int):
	if oper == "+":
		result = a + b
	elif oper == "-":
		result = a - b
	else:
		result = "**Неверный оператор**"
	await inter.send(str(result))

#Команда блокировки

@bot.slash_command(description='Банит участника')
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake. Member, *, reason="Нарушение правил."):
	await ctx.send(f"**Администратоp** {ctx.author.mention} **забанил пользователя** {member.mention}", delete_after=1440)
	await member.ban(reason=reason)
	await ctx.message.delete()

#Выводит онформацию о сервере 

@bot.slash_command(description='Информация о сервере')
async def server(inter):
	await inter.response.send_message(
        f"**Название сервера**: {inter.guild.name}\n**Всего участников**: {inter.guild.member_count}"
    )

#Мут участника через таймаут

@bot.slash_command(description='Мутит участника')
@commands.has_permissions(mute_members=True, administrator=True)
async def mute(self, interaction, member: disnake.Member, time: str, reason: str):
	time = datetime.datetime.now() + datetime.timedelta (minutes=int (time))
	await member.timeout(reason=reason, until=time)
	await interaction.response.send_message(f"**Пользователь** {member.mention} **был замьючен, по причине:** {reason}", ephemeral=True)

#Команда разбана

@bot.slash_command(description='Разбанивает участника')
async def unban(self, interaction, user: disnake. User):
	await interaction.guild.unban(user)
	await interaction.response. send_message(f"**С пользователя** {user.mention} **снят бан** ", ephemeral=True)

#Команда Clear

@bot.slash_command(description='Удаляет сообщения')
@commands.has_permissions(administrator=True)
async def clear(interaction, amount: int):
	await interaction.response.send_message(f"**Удалено** {amount} **сообщения**")
	await interaction.channel.purge(limit=amount + 1)

#Приветствие с новыми участниками 


@bot.event
async def on_member_join(member):
	role = disnake.utils.get(member.guild.roles, name='Название роли')  #При заходе участник автоматически будет получать роль
	channel = member.guild.system_channel #Сообщение о приветствии отправится в системный канал 
	embed = disnake. Embed(
		title=f"**Залетел на сервер!**",
		description=f"{member.mention} **Привестую на нашем сервере, для начала прочти правила📜**",
		color=0xF0C43F,
	)
	embed.set_author(
    name="",
    url="",
    icon_url="",
	)
	embed.set_footer(
    text="",
    icon_url="",
	)
	embed.add_field(name="**Желаю приятного времяпровождения!🍀**", value="", inline=False)
	embed.set_image("")

	await channel.send(embed=embed)
	await member.add_roles(role)

#Прощание с участниками

@bot.event
async def on_member_remove(member): 
	channel = bot.get_channel(id)
	embed = disnake. Embed(
		title="**Покинул нашу тусовку**",
		description=f"{member.mention} **ждём твоего возвращения🌟**",
		color=0xF0C43F,
	)
	embed.set_author(
    	name="",
    	url="",
    	icon_url="",
	)
	embed.set_image(url="")

	await channel.send(embed=embed)

#Команда Help

@bot.slash_command(description='Получить список всех команд')
async def help(ctx):
		embed = disnake. Embed(
 		title="Список всех команд бота:",
 		description=f"_/ban_ - **Команда банит участников**\n _/clear_ - **Очищает чат от сообщений**\n _/kick_ - **Кикает участников** \n _/mute_ - **Мутит участников**\n _/server_ - **Выдает информацию о сервере** \n_/unban_ - **Разбанивает участников** ",
 		color=0xF0C43F,
		)

		embed.set_author(
		name="",
		url="",
		icon_url="",
	)

		await ctx.send(embed=embed)

#Удаление приглашений 

@bot.event
async def on_message(message):
	if 'https://discord.gg' in message.content.lower():
		await message.delete()
		await message.channel.send(f"**{message.author.mention} Не нарушай правила сервера**")


bot.run("TOKEN") 
