import discord
from discord import app_commands
from discord.ext import commands
from utils.maps import *
import json


main_guild = 994469525464551474
test_guild = 1047605217350398062
selected_guild = discord.Object(id=main_guild)
  

class Map(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="map",
                        description="Escolhe um mapa aleatório")
    @app_commands.choices(modo=[
        app_commands.Choice(name="Mata-Mata", value="tdm"),
        app_commands.Choice(name="Cerco", value="cerco"),
        app_commands.Choice(name="Chacina", value="chacina"),
        app_commands.Choice(name="Rei do Pedaço", value="koth"),
        app_commands.Choice(name="Mapas de Teste", value="teste")
    ])
    async def choose_map(interaction: discord.Interaction, modo_de_jogo: app_commands.Choice[str]):
        interaction.send_response(f"Mapa: {choose_map(modo_de_jogo)}")

