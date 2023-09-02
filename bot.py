import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
import json
import sys


cmd_prefix = "v!"
intents = discord.Intents().all()
client = commands.Bot(command_prefix=cmd_prefix.lower(), intents=intents)


print("User Current Version:-", sys.version)

class VScramble(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=cmd_prefix,
            intents=intents,
            application_id=1054757107473326090
        )
        # self.tree = app_commands.CommandTree(self)
        self.initial_extentions = [
            "cogs.scramble",
            "cogs.utility",
            "cogs.help",
            "cogs.admin"
        ]

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        print("-"*24)
    
    async def on_guild_join(self, joined_guild):
        print("hey")
        with open("cogs/ServerSettings.json") as f:
            guilds = json.load(f)
        
        for guild in self.guilds:
            if str(guild.id) not in guilds.keys():
                guilds[str(guild.id)] = {
                    "Time 1": -1,
                    "Time 2": -1,
                    "Troca Time": -1,
                    "Comando": -1,
                    "automove": False,
                    "ignored ids": []
                }
                print(f"ADDED NEW GUILD!\nName: {guild.name}\n ID: {guild.id}")
            with open("cogs/ServerSettings.json", "w") as f:
                json.dump(guilds, f, indent=4)

    async def setup_hook(self) -> None:
        for ext in self.initial_extentions:
            await self.load_extension(ext)
            print(f"|{ext}| has loaded")
            print("-"*24)
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)
        print("-"*24)
    
    
client = VScramble()
client.run('BOT TOKEN')