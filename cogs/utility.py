import discord
from discord import app_commands
from discord.ext import commands
import json


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Ativar/Desativar auto-move
    @app_commands.command(name="automove",
                        description="Ativa/Desativa a função de mover os membros automaticamente")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Ligar", value="ligar"),
        app_commands.Choice(name="Desligar", value="desligar")
    ])
    async def _automove(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        
        with open("cogs/ServerSettings.json", "r") as f:
            auto_move = json.load(f)
        current_guild = str(interaction.guild_id)
        
        choices.value = choices.value.lower()
        if choices.value == "ligar":
            if not auto_move["automove"]:
                auto_move[current_guild]["automove"] = True
                with open("cogs/ServerSettings.json", "w") as f:
                    json.dump(auto_move, f, indent=4)
                await interaction.response.send_message(f"Automove foi ligado")
            else:
                await interaction.response.send_message(f"Automove já está ligado")
        
        if choices.value == "desligar":
            if auto_move[current_guild]["automove"]:
                auto_move[current_guild]["automove"] = False
                with open("cogs/ServerSettings.json", "w") as f:
                    json.dump(auto_move, f, indent=4)
                await interaction.response.send_message(f"Automove foi desligado")
            else:
                await interaction.response.send_message(f"Automove já está desligado")
                    


    # Add someone to black list
    @app_commands.command(name="blacklist-add",
                          description="Adiciona um usuário no blacklist para não ser movido pelo bot")
    async def _blacklistadd(self, interaction: discord.Interaction, user: discord.Member):
        with open("cogs/ServerSettings.json", "r") as f:
            excluded_list = json.load(f)
        current_guild = str(interaction.guild_id)
        
        if user not in excluded_list[current_guild]["ignored ids"]:
            excluded_list[current_guild]["ignored ids"].append(int(user.id))
            with open("cogs/ServerSettings.json", "w") as ids:
                json.dump(excluded_list, ids, indent=4)
            await interaction.response.send_message(f':white_check_mark: {user.display_name} será ignorado.')
        else:
            await interaction.response.send_message(f"{user.display_name} já está excluído... :neutral_face:")


    # Remove from blacklist
    @app_commands.command(name="blacklist-remove",
                          description="Remove um usuário da Lista Negra")
    async def _blacklistremove(self, interaction: discord.Interaction, user: discord.Member):
        with open("cogs/ServerSettings.json", "r") as f:
            excluded_list = json.load(f)
        current_guild = str(interaction.guild_id)
        
        if user.id in excluded_list[current_guild]["ignored ids"]:
            excluded_list[current_guild]["ignored ids"].remove(user.id)
            with open("cogs/ServerSettings.json", "w") as ids:
                json.dump(excluded_list, ids, indent=4)
            await interaction.response.send_message(f':white_check_mark: {user.display_name} não será mais ignorado')
        else:
            await interaction.response.send_message(f":x: {user.display_name} já está incluso")


    # List of blacklisted people
    @app_commands.command(name="blacklist-list",
                         description="Lista de pessoas na Lista Negra")
    async def _blacklistlist(self, interaction: discord.Interaction):
        with open("cogs/ServerSettings.json", "r") as f:
            excluded_list = json.load(f)
        current_guild = str(interaction.guild_id)
        print("-" * 24)
        print("Listing excluded people")
        excluded = []
        for excluded_people in excluded_list[current_guild]["ignored ids"]:
            excluded.append(self.client.get_user(int(excluded_people)).display_name)
        excluded = '\n'.join(excluded)

        embed = discord.Embed(title="LISTA NEGRA")
        embed.add_field(name="Usuários na lista negra", value=excluded)
        await interaction.response.send_message(embed=embed)
        print("Done")
        print("-" * 24)

    #-------------------------------------------------------------------------------------------------------------------
    # PREFIX COMMANDS
    @commands.command(name="automove", aliases=["am"])
    async def automove(self, ctx):
        
        with open("cogs/ServerSettings.json", "r") as f:
            auto_move = json.load(f)
        current_guild = str(ctx.author.guild.id)
        
        if not auto_move[current_guild]["automove"]:
            auto_move[current_guild]["automove"] = True
            with open("cogs/ServerSettings.json", "w") as f:
                json.dump(auto_move, f, indent=4)
                
            print(f"{ctx.author.display_name} has turned on AUTOMOVE")
            print("-" * 24)
            await ctx.send(":white_check_mark: Auto-move está ativado")
        else:
            auto_move[current_guild]["automove"] = False
            with open("cogs/ServerSettings.json", "w") as f:
                json.dump(auto_move, f, indent=4)
            print(f"{ctx.author.display_name} has turned on AUTOMOVE")
            print("-"*24)
            await ctx.send(":x: Auto-move está desligado")


    # Listar pessoas excluídas
    @commands.command(aliases=["bl"])
    async def blacklist(self, ctx):
        with open("cogs/ServerSettings.json", "r") as f:
            excluded_list = json.load(f)
        current_guild = str(ctx.author.guild.id)
        
        print("Listing excluded people")
        excluded = []
        for excluded_people in excluded_list[current_guild]["ignored ids"]:
            excluded.append(self.client.get_user(int(excluded_people)).display_name)
        excluded = '\n'.join(excluded)

        embed = discord.Embed(title="LISTA NEGRA")
        embed.add_field(name="Usuários na lista negra", value=excluded)
        await ctx.send(embed=embed)
        print(excluded)
        print("Done")
        print("-" * 24)


    # Este usuário será ignorado na hora de trocar os times
    @commands.command(aliases=["bladd", "bla"])
    async def blacklistadd(self, ctx, user: discord.Member):
        with open("cogs/ServerSettings.json", "r") as f:
            excluded_list = json.load(f)
        current_guild = str(ctx.author.guild.id)
        
        if user not in excluded_list[current_guild]["ignored ids"]:
            excluded_list[current_guild]["ignored ids"].append(int(user.id))
            with open("cogs/ServerSettings.json", "w") as ids:
                json.dump(excluded_list, ids, indent=4)
            print(f"{ctx.author.display_name} has added {user.display_name} to the BLACK LIST")
            print("-"*24)
            await ctx.send(f':white_check_mark: {user.display_name} será ignorado.')
        else:
            await ctx.send(f"{user.display_name} já está excluído")

    # Volta a incluir o jogador
    @commands.command(aliases=["blremove", "blr"])
    async def blacklistremove(self, ctx, user: discord.Member):
        with open("cogs/ServerSettings.json", "r") as f:
            excluded_list = json.load(f)
        current_guild = str(ctx.author.guild.id)
        
        if user.id in excluded_list[current_guild]["ignored ids"]:
            excluded_list[current_guild]["ignored ids"].remove(user.id)
            
            with open("cogs/ServerSettings.json", "w") as ids:
                json.dump(excluded_list, ids, indent=4)
            print(f"{ctx.author.display_name} has removed {user.display_name} from the BLACK LIST")
            print("-" * 24)
            await ctx.send(f':white_check_mark: {user.display_name} não será mais ignorado')
        else:
            await ctx.send(f":x: {user.display_name} não está na lista negra")


async def setup(client: commands.Bot):
    await client.add_cog(Utility(client))