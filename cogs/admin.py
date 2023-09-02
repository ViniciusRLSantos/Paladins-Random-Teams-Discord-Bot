import discord
import json
from discord import app_commands
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client       
    
    # PREFIX COMMANDS-------------------------------------------------------------------------------------------------------
    @commands.command(name="setcommandchannel",
                      aliases=["setcmd", "setcmdchannel"])
    @commands.has_permissions(administrator=True)
    async def set_command(self, ctx, channel: discord.TextChannel):
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
        current_guild = str(ctx.author.guild.id)
        try:
            settings[current_guild]["Comando"] = channel.id
            await ctx.send(f"Canal de comandos foi setado para: {channel.mention}")
            with open("cogs/ServerSettings.json", "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            await ctx.send(f":x: Insira um id válido de canal ou uma menção de canal existente \n Erro: {e} ")
    
    @commands.command(name="setteamonechannel",
                      aliases=["setteamone", "setteam1channel", "setteam1"])
    @commands.has_permissions(administrator=True)
    async def set_team_one(self, ctx, channel: discord.VoiceChannel):
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
        current_guild = str(ctx.author.guild.id)
        try:
            settings[current_guild]["Time 1"] = channel.id
            await ctx.send(f"Canal de Time 1 foi setado para: {channel.mention}")
            with open("cogs/ServerSettings.json", "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            await ctx.send(f":x: Insira um id válido de canal ou uma menção de canal existente \n Erro: {e} ")
    
    @commands.command(name="setteamtwochannel",
                      aliases=["setteamtwo", "setteam2channel", "setteam2"])
    @commands.has_permissions(administrator=True)
    async def set_team_two(self, ctx, channel: discord.VoiceChannel):
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
        current_guild = str(ctx.author.guild.id)
        try:
            settings[current_guild]["Time 2"] = channel.id
            await ctx.send(f"Canal de Time 2 foi setado para: {channel.mention}")
            with open("cogs/ServerSettings.json", "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            await ctx.send(f":x: Insira um id válido de canal ou uma menção de canal existente \n Erro: {e} ")
    
    @commands.command(name="setscramblechannel",
                      aliases=["setscramble"])
    @commands.has_permissions(administrator=True)
    async def set_scramble(self, ctx, channel: discord.VoiceChannel):
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
        current_guild = str(ctx.author.guild.id)
        try:
            settings[current_guild]["Troca Time"] = channel.id
            await ctx.send(f"Canal de Permutar Equipes foi setado para: {channel.mention}")
            with open("cogs/ServerSettings.json", "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            await ctx.send(f":x: Insira um id válido de canal ou uma menção de canal existente \n Erro: {e} ")
            

async def setup(client: commands.Bot):
    await client.add_cog(Admin(client))