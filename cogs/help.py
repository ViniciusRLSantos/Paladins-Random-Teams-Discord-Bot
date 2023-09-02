import discord
from discord import app_commands
from discord.ext import commands


class Helpme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def helpme(self, ctx):
        embed = discord.Embed(title="**LISTA DE COMANDOS**")
        embed.add_field(name="**scramble (s)**",
                        value="Separa os times de modo aleatório.",
                        inline=False)
        embed.add_field(name="**scramblechampion (sc, scramblec, scramblechamp)**",
                        value="Separa os times de modo aleatório e escolhe os champions de cada jogador. Pode também limitar para champions "
                              "de uma classe específica",
                        inline=False)
        embed.add_field(name="**blacklist (bl)**",
                        value="Mostra quem está na lista negra do bot.\n"
                            "Pessoas na lista negra não serão colocados em nenhum time"
                            " mesmo estando na call.",
                        inline=False)
        embed.add_field(name="**blacklistadd (bladd/bla)**",
                        value="Adiciona alguém na lista negra do bot",
                        inline=False)
        embed.add_field(name="**blacklistremove (blremove/blr)**",
                        value="Remove alguém na lista negra do bot",
                        inline=False)
        embed.add_field(name="**automove (am)**",
                        value="Ativa/desativa a função de mover os membros para a call "
                            "dos times automaticamente ao usar o comando *scramble*.",
                        inline=False)
        await ctx.send(embed=embed)
    
    # Slash Command version
    @app_commands.command(name="helpme", description="Lista de todos os comandos.")
    async def _helpme(self, interaction: discord.Interaction):
        embed = discord.Embed(title="**LISTA DE COMANDOS**")
        embed.add_field(name="**scramble (s)**",
                        value="Separa os times de modo aleatório.",
                        inline=False)
        embed.add_field(name="**scramblechampion (sc, scramblec, scramblechamp)**",
                        value="Separa os times de modo aleatório e escolhe os champions de cada jogador. Pode também limitar para champions "
                              "de uma classe específica",
                        inline=False)
        embed.add_field(name="**blacklist (bl)**",
                        value="Mostra quem está na lista negra do bot.\n"
                            "Pessoas na lista negra não serão colocados em nenhum time"
                            " mesmo estando na call.",
                        inline=False)
        embed.add_field(name="**blacklistadd (bladd/bla)**",
                        value="Adiciona alguém na lista negra do bot",
                        inline=False)
        embed.add_field(name="**blacklistremove (blremove/blr)**",
                        value="Remove alguém na lista negra do bot",
                        inline=False)
        embed.add_field(name="**automove (am)**",
                        value="Ativa/desativa a função de mover os membros para a call "
                            "dos times automaticamente ao usar o comando *scramble*.",
                        inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot):
    await client.add_cog(Helpme(client))