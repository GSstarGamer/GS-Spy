import discord
class User():
    def __init__(self, discordUser: discord.User) -> None:
        self.name = discordUser.name
        self.pfp = discordUser.avatar
