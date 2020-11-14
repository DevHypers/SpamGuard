import asyncio, discord, os, time
from itertools import product
from string import ascii_uppercase

import openpyxl
import threading

from AI import CheckSpam

client = discord.Client()

token = str(open("token.txt", "r", encoding="utf-8").readline())

prefix = "!"
AtoZ = []


async def bt(games):
    await client.wait_until_ready()
    while not client.is_closed():
        for g in games:
            await client.change_presence(status=discord.Status.online, activity=discord.Game(g))

            await asyncio.sleep(5)

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

    for x in range(1, 4):
        for combo in product(ascii_uppercase, repeat=x):
            AtoZ.append("".join(combo))

    ch = 0
    for g in client.guilds:
        ch += 1
    await client.change_presence(status=discord.Status.online, activity=await bt(['오늘도 스팸과 난투를 ', f'{ch}개의 서버에서 사용', ]))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    file = openpyxl.load_workbook("Config_DB.xlsx")
    sheet = file.active

    chguild = False
    for i in range(1, 101):
        if sheet["A" + str(i)].value == str(message.guild.id):
            for j in AtoZ:
                if sheet[str(j) + str(i)].value == str(message.channel.id):
                    chguild = True
                    break
            break

    if not chguild and not message:
        spampre = int(CheckSpam(message.content))
        if spampre >= 70:
            await message.delete()

    if message.content.startswith(prefix + 'clear'):
        if not message.author.guild_permissions.manage_messages:
            await message.channel.send("<@" + str(message.author.id) + ">" + ", 이 명령어는 `메세지 관리` 권한을 필요로 합니다!")
            return

        await message.delete()
        await message.channel.purge(limit=int(message.content.split(" ")[1]))

    if message.content.startswith(prefix + 'addexception'):
        if not message.author.guild_permissions.manage_messages:
            await message.channel.send("<@" + str(message.author.id) + ">" + ", 이 명령어는 `메세지 관리` 권한을 필요로 합니다!")
            return

        file = openpyxl.load_workbook("Config_DB.xlsx")
        sheet = file.active

        chguild = False
        for i in range(1, 101):
            if sheet["A" + str(i)].value == str(message.guild.id):
                chguild = True

                for j in AtoZ:
                    if not sheet[str(j) + str(i)].value:
                        sheet[str(j) + str(i)].value = str(message.channel.id)
                        message.channel.send("예외 채널 등록 성공!")
                        file.save("Config_DB.xlsx")
                        return
                break

        if not chguild:
            for i in range(1, 101):
                if not sheet["A" + str(i)].value:
                    sheet["A" + str(i)].value = str(message.guild.id)
                    break

            for i in range(1, 101):
                if sheet["A" + str(i)].value == str(message.guild.id):
                    for j in AtoZ:
                        if not sheet[str(j) + str(i)].value:
                            sheet[str(j) + str(i)].value = str(message.channel.id)
                            message.channel.send("예외 채널 등록 성공!")
                            file.save("Config_DB.xlsx")
                            return
                    break

        file.save("Config_DB.xlsx")


client.run(token)
