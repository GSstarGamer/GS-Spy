import discord
from discord.ext import commands, tasks
import dotenv
import os
from configL import config
import PyUtls as logger
import asyncio
from functions import *
import requests

config()
dotenv.load_dotenv()
__TOKEN = os.getenv('TOKEN')


bot = commands.Bot(command_prefix=';',
                   help_command=None)
bot.lastsong = None
bot.laststatus = None
bot.laststatustext = None
bot.lastgame = None



@bot.listen()
async def on_ready():
    logger.success(f'Bot is logging {bot.user.name}. with Prefix: {config().prefix}')
    targets = [bot.get_user(user).name for user in config().targets]
    logger.log(f'Targets are [{", ".join(targets)}]')
    res = requests.get(config().webhookURL).json()
    channel = bot.get_channel(int(res['channel_id']))
    guild = bot.get_guild(int(res['guild_id']))

    channelname = ''
    guildname = ''

    if not channel:
        channelname = res['channel_id']
    else:
        channelname = '#'+channel.name
    
    if not guild:
        guildname = res['guild_id']
    else:
        guildname = guild.name
    

    logger.log(f'Webhooks will be sent in {guildname} -> {channelname}')

@bot.listen()
async def on_message_delete(message: discord.Message):
    if message.author.id in config().targets:
        if isenabled():     
            gLog('message delete', message.content, message.author, channelID=message.channel.id, jump_url=message.jump_url)
    await bot.process_commands(message)

@bot.listen() #spotify
async def on_presence_update(before: discord.Relationship, after: discord.Relationship):
    if before.id in config().targets:
        if isenabled():
            if not isinstance(after, discord.member.Member) and len(after.activities)>0:
                for activity in after.activities:
                    if isinstance(activity, discord.activity.Spotify):
                        if activity.title != bot.lastsong:
                            gLog('spotify', activity.title,
                                after.user, spotify=activity)
                                
                            bot.lastsong = activity.title
                            break

@bot.listen()  # status
async def on_presence_update(before: discord.Relationship, after: discord.Relationship):
    if before.id in config().targets:
        if isenabled():
            if not isinstance(after, discord.member.Member) and after.status != bot.laststatus and before.status != after.status:
                gLog('status', f'{before.status} -> {after.status}', before.user)
                bot.laststatus = after.status


@bot.listen()  # statustext
async def on_presence_update(before: discord.Relationship, after: discord.Relationship):
    if before.id in config().targets:
        if isenabled():
            if not isinstance(after, discord.member.Member) and after.activity.name != bot.laststatustext and before.activity.name != after.activity.name:
                beforeact = None
                afteract = None
                if isinstance(before.activity, discord.activity.CustomActivity):
                    beforeact = before.activity.name

                if isinstance(after.activity, discord.activity.CustomActivity):
                    afteract = after.activity.name
                if beforeact or afteract:
                    gLog('status text',
                        f'{beforeact} -> {afteract}', before.user)
                    bot.laststatustext = after.activity.name


@bot.listen()  # game
async def on_presence_update(before: discord.Relationship, after: discord.Relationship):
    if before.id in config().targets:
        if isenabled():
            if not isinstance(after, discord.member.Member) and len(after.activities) > 0:
                bgames = []
                agames = []
                for beforeG in before.activities:
                    if isinstance(beforeG, discord.activity.Game):
                        bgames.append(beforeG.name)
                        break
                for afterG in after.activities:
                    if isinstance(afterG, discord.activity.Game):
                        agames.append(afterG.name)
                        break
                bgames = ', '.join(bgames)
                agames = ', '.join(agames)
                if bgames or agames:
                    gLog('game', f'Before: [{bgames}] - After: [{agames}]', before.user)
            

@bot.listen()
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.id in config().targets:
        if isenabled():
            gLog('message edit', f'{before.content} -> {after.content}', before.author, before.channel.id, before.jump_url)
    await bot.process_commands(after)


@bot.listen()
async def on_typing(channel:discord.abc.Messageable, user:discord.User, when:datetime):
    if user.id in config().targets:
        if isenabled():
            name = ''
            if isinstance(channel, discord.DMChannel):
                name = 'your DM'
            else:
                try:
                    name = f'{channel.guild.name} -> #{channel.name}'
                except:
                    name = '#'+str(channel.name)
            gLog('typing', f'In {name}', user, channel.id)


@bot.listen() #bot.commands went working cuz package gay
async def on_message(ctx:discord.Message):
    if ctx.author == bot.user and ctx.content.startswith(config().prefix):
        command = ctx.content.replace(config().prefix, '')
        if command == 'toggle':
            isenabled(True)
            x = await ctx.reply(f'Spy is set too {isenabled()}. (DELETING IN 3 SECONDS)')
            await asyncio.sleep(3)
            await ctx.delete()
            await x.delete()
            logger.log(f'Spy is set to {isenabled()}')
    await bot.process_commands(ctx)


bot.run(__TOKEN)