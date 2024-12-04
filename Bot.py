#Spellz ~ by ~ Gytis#9668

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
db = 'D:/Bot Clients/Spellz/db.json'

#Get list for words
with open(words, "r+") as f:
    allwords = []
    for el in f:
        if '\n' in el:
            el = el.rstrip('\n')
        allwords.append(el)

#Def
def me(ctx):
    return ctx.author.id == 301014178703998987

#Events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='!spell'))
    print("Spellz now online!")

@client.event
async def on_message(msg):
    if msg.content.lower() == '!spell':
        with open(db, 'r+') as f:
            data = json.load(f)
            userid = str(msg.author.id)
            if userid not in data:
                data[userid] = {
                    "total": 0,
                    "correct": 0,
                    "incorrect": 0,
                    "ffa": 0
                }
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            else:
                pass
        wordchoice = random.choice(allwords)
        os.rename('{}.mp3'.format(wordchoice), 'Spellz.mp3')
        await msg.reply(file=discord.File('D:/Bot Clients/Spellz/Audio/Spellz.mp3'.format(wordchoice)))
        os.rename('Spellz.mp3', '{}.mp3'.format(wordchoice))
        def check(m):
            return m.author.id == msg.author.id
        userresponse = await client.wait_for('message', timeout=10, check=check)
        with open(db, 'r+') as f:
            data = json.load(f)
            data[str(msg.author.id)]['total'] = data[str(msg.author.id)]['total'] + 1
            if userresponse.content.lower() == wordchoice.lower():
                await userresponse.reply("Correct!")
                data[str(msg.author.id)]['correct'] = data[str(msg.author.id)]['correct'] + 1
            else:
                await userresponse.reply("Incorrect")
                data[str(msg.author.id)]['incorrect'] = data[str(msg.author.id)]['incorrect'] + 1
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
    elif msg.content in ['<@966386674382807040>', '<@!966386674382807040>']:
        await msg.reply("My prefix is `!`")
    else:
        pass
    await client.process_commands(msg)

#Loops
@tasks.loop(seconds=60)
async def ffa():
    await client.wait_until_ready()
    ffachannel = client.get_channel(967108141785419786)
    wordchoice = random.choice(allwords)
    os.rename('{}.mp3'.format(wordchoice), 'Spellz.mp3')
    await ffachannel.send(file=discord.File('D:/Bot Clients/Spellz/Audio/Spellz.mp3'.format(wordchoice)))
    os.rename('Spellz.mp3', '{}.mp3'.format(wordchoice))
    userresponse = await client.wait_for('message', timeout=60)
    with open(db, 'r+') as f:
        data = json.load(f)
        if userresponse.content.lower() == wordchoice.lower():
            await userresponse.reply("Correct!")
            data[str(userresponse.author.id)]['ffa'] = data[str(userresponse.author.id)]['ffa'] + 1
        else:
            pass
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

#Commands
@client.command(aliases=['stats', 'total'])
async def score(ctx, member : discord.Member=None):
    with open(db, 'r+') as f:
        data = json.load(f)
        userid = str(ctx.author.id)
        if userid not in data:
            data[userid] = {
                "total": 0,
                "correct": 0,
                "incorrect": 0,
                "ffa": 0
            }
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
        else:
            pass
        embed = discord.Embed(
            title="Score",
            colour=0xFFF261,
            description=f"**Total:** {data[userid]['total']}\n**Correct:** {data[userid]['correct']}\n**Incorrect:** {data[userid]['incorrect']}\n**Ratio:** {round(((data[userid]['correct'] / data[userid]['total']) * 100), 2)}%\n**FFA:** {data[userid]['ffa']}"
        )
        await ctx.reply(embed=embed)

#Make Work
async def main():
    async with client:
        ffa.start()
        await client.start('OTY2Mzg2Njc0MzgyODA3MDQw.YmA_uQ.OXXAuF6SGAWtMh4aMPNLQ8QJ7YY')

asyncio.run(main())