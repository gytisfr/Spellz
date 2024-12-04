#Spellz Event ~ by ~ Gytis#9668

#Imports
import discord
import asyncio
import random
import json
import os
from discord.ext import commands, tasks
from discord.utils import get

#Vars
client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
client.remove_command('help')
os.chdir('D:/Bot Clients/Spellz/Audio')
words = 'D:/Bot Clients/Spellz/Words.txt'
db = 'D:/Bot Clients/Spellz/Event Bot/EventDB.json'

#Get list for words
with open(words, "r+") as f:
    allwords = []
    for el in f:
        if '\n' in el:
            el = el.rstrip('\n')
        allwords.append(el)

#Def
def admins(ctx):
    return ctx.author.id == 301014178703998987, 667029055727599627
    #Me, Epic

#Events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='!spell'))
    print("Spellz Event now online!")

@client.event
async def on_message(msg):
    if msg.content.lower() == '!word':
        if msg.author.id in [301014178703998987, 667029055727599627]:
            wordchoice = random.choice(allwords)
            os.rename('{}.mp3'.format(wordchoice), 'Spellz.mp3')
            await msg.channel.send("<@&977194890456870913>", file=discord.File('D:/Bot Clients/Spellz/Audio/Spellz.mp3'.format(wordchoice)))
            os.rename('Spellz.mp3', '{}.mp3'.format(wordchoice))
            userresponse = await client.wait_for('message')
            while userresponse.content.lower() != wordchoice.lower():
                if userresponse.author.id != 972087738037846036:
                    with open(db, 'r+') as f:
                        data = json.load(f)
                        if str(userresponse.author.id) not in data:
                            userid = str(userresponse.author.id)
                            data[userid] = {
                                "correct": 0,
                                "incorrect": 0,
                                "score": 0
                            }
                            f.seek(0)
                            f.truncate()
                            json.dump(data, f, indent=4)
                        await userresponse.reply("Incorrect")
                        data[str(userresponse.author.id)]['incorrect'] = data[str(userresponse.author.id)]['incorrect'] + 1
                        data[str(userresponse.author.id)]['score'] = data[str(userresponse.author.id)]['score'] - 1
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f, indent=4)
                userresponse = await client.wait_for('message')
            with open(db, 'r+') as f:
                data = json.load(f)
                if str(userresponse.author.id) not in data:
                    userid = str(userresponse.author.id)
                    data[userid] = {
                        "correct": 0,
                        "incorrect": 0,
                        "score": 0
                    }
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
                await userresponse.reply("Correct!")
                data[str(userresponse.author.id)]['correct'] = data[str(userresponse.author.id)]['correct'] + 1
                data[str(userresponse.author.id)]['score'] = data[str(userresponse.author.id)]['score'] + 1
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
    await client.process_commands(msg)

#Commands
@client.command(aliases=["return"])
@commands.check(admins)
async def owa(ctx, member : discord.Member=None):
    with open(db, "r+") as f:
        data = json.load(f)
        if member:
            personid = str(member.id)
            embed = discord.Embed(
                title=member.name,
                colour=0xFFF261,
                description=f"Correct:{data[personid]['correct']}\nIncorrect:{data[personid]['incorrect']}\nScore:{data[personid]['score']}"
            )
        else:
            embed = discord.Embed(
                title="Leaderboard",
                colour=0xFFF261,
                description=""
            )
            for el in data:
                theperson = client.get_user(int(el))
                embed.add_field(name=f"{theperson.name}", value=f"Correct:{data[el]['correct']}\nIncorrect:{data[el]['incorrect']}\nScore:{data[el]['score']}", inline=True)
        await ctx.author.send(embed=embed)

@client.command()
@commands.check(admins)
async def top(ctx):
    with open(db, "r+") as f:
        data = json.load(f)
        allscores = []
        for el in data:
            allscores.append(data[el]["score"])
        topscore = max(allscores)
        def _getscore(k):
            return data[k]['score']
        print(max(data, key=_getscore))
        thetopperson = client.get_user(int(max(data, key=_getscore)))
        print(thetopperson)
        embed = discord.Embed(
            title="Top",
            colour=0xFFF261,
            description=f"{thetopperson.mention} / {thetopperson.id} with {topscore} Points"
        )
        await ctx.author.send(embed=embed)

@client.command()
@commands.check(admins)
async def say(ctx, *, msg):
    await ctx.send(msg)

client.run('OTcyMDg3NzM4MDM3ODQ2MDM2.YnT9QQ.DvJ0aZFFV6FFn4I5beuUphATou0')