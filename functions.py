from discord_webhook import DiscordWebhook, DiscordEmbed
from configL import config
import PyUtls
import os
from datetime import datetime
import discord
import json


def gLog(type: str, message: str, user: discord.User, channelID: int = None, jump_url: str = None, spotify: discord.Spotify=None):
    print(
        f'{PyUtls.current_time()} [{user.name}] {type.upper()}: {message}')

    fMessage = f'{datetime.now().strftime("%H:%M:%S")} [{user.name}]: {message}'
    filePath = './logs/'+type+'.txt'
    if type+'.txt' not in os.listdir('./logs'):
        with open(filePath, 'w') as f:
            f.write(fMessage+'\n')
    else:
        with open(filePath, 'a') as f:
            f.write(fMessage+'\n')
    
    webhook = DiscordWebhook(url=config().webhookURL,
                             content="# GS-Spy caught something")
    
    embed = DiscordEmbed(title=type.capitalize(),
                         description=message, rate_limit_retry=True, color="8000FF")
    
    embed.set_author(name=user.name, url=f'https://discord.com/users/{user.id}',
                     icon_url=user.avatar.url)

    if channelID:
        embed.add_embed_field(name="Channel", value=f"<#{channelID}>")
    if jump_url:
        embed.add_embed_field(name="Jump url", value=jump_url)
    if spotify:
        embed.add_embed_field(name="Album", value=spotify.album)
        embed.add_embed_field(name="Track URL", value=spotify.track_url)
        totalSec = spotify.duration.total_seconds()
        minutes = totalSec // 60
        seconds = totalSec % 60
        embed.add_embed_field(name="Duration", value=f'{round(minutes)}:{round(seconds)}')
        embed.set_image(url=spotify.album_cover_url)

    embed.set_timestamp()
    webhook.add_embed(embed)

    response = webhook.execute()


def isenabled(toggle:bool=None):
    with open('config.json', 'r') as f:
        data = json.load(f)
    enabled = data['enabled']
    if toggle:
        if enabled:
            data['enabled'] = False
        else:
            data['enabled'] = True
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4)
    else:
        return enabled
