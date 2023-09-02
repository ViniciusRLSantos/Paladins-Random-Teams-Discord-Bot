import discord
from discord import app_commands
from discord.ext import commands
import random as rd
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
from utils.champion import createRandomCrew
from typing import Optional, List


async def role_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> List[app_commands.Choice[str]]:
    roles = ["Todos", "Dano", "Suporte", "Flanco", "Tanque"]
    return [
        app_commands.Choice(name=classe, value=classe)
        for classe in roles if current.lower() in classe.lower()
    ]

class Scramble(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #-------------------------------------------------------------------------------------------------------------------
    # SLASH COMMANDS
    # Normal Scramble
    @app_commands.command(name="scramble",
                          description="Separa os times de modo aleatório")
    async def _scramble(self, interaction: discord.Interaction) -> None:
        
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
            
        voice_channel = interaction.user.voice.channel
        current_guild = interaction.guild_id
        time1 = self.client.get_channel(settings[str(current_guild)]["Time 1"])
        time2 = self.client.get_channel(settings[str(current_guild)]["Time 2"])
        troca_time = self.client.get_channel(settings[str(current_guild)]["Troca Time"])

        members = troca_time.members
        member_list = []
        team1 = []
        
        auto_move = settings[str(current_guild)]["automove"]
        excluded_list = settings[str(current_guild)]["ignored ids"]
        
        if settings[str(current_guild)]["Comando"] != -1:
            if settings[str(current_guild)]["Comando"] != interaction.channel_id:
                correct_channel = self.client.get_channel(settings[str(current_guild)]["Comando"])
                await interaction.response.send_message(f"Execute o comando no canal correto: {correct_channel.mention}")
                return

        if voice_channel == troca_time:
            # Separando os times e movendo para call
            print("\n-----------------------------------")
            print("Trocando times...")
            for member in members:
                if member.id not in excluded_list:
                    member_list.append(member)

            for i in range(round(len(member_list) / 2)):
                user = rd.choice(member_list)
                team1.append(user)
                member_list.remove(user)

            if auto_move:
                for mem in team1:
                    await mem.move_to(time1)

                for users in member_list:
                    await users.move_to(time2)

            print(f"Time 1 - {team1}\n\nTime 2 - {member_list}")
            print("\nTroca de times finalizado com êxito")
            print("-----------------------------------")

            # Criando a imagem dos times criados
            teams_image = Image.open("teams.png")
            #  Inserindo foto de perfil + nome dos membros do time 1
            for index, users_team1 in enumerate(team1):
                data = BytesIO(await users_team1.display_avatar.read())
                user_nick = users_team1.display_name
                pfp_size = 150
                font_size = 50

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 53
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                draw.text((xcord + pfp_size + 10, ycord + pfp_size / 2 - font_size), user_nick, font=font,
                        stroke_width=4, stroke_fill=(0, 0, 0, 255))

            #  Inserindo foto de perfil + nome dos membros do time 2
            for index, users_team2 in enumerate(member_list):
                data = BytesIO(await users_team2.display_avatar.read())
                user_nick = str(users_team2.display_name)
                pfp_size = 150
                font_size = 50

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 1717
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                draw.text((xcord - 10, ycord + pfp_size / 2 - font_size), user_nick, font=font, align="right", anchor="rt",
                        stroke_width=4, stroke_fill=(0, 0, 0, 255))

            with BytesIO() as a:
                teams_image.save(a, "PNG")
                a.seek(0)
                await interaction.response.send_message("Os times foram criados!", file=discord.File(a, "Times_Criados.png"))
        else:
            await interaction.response.send_message(f"Você precisa estar no {troca_time.mention} para executar o comando.")
    
    
    # Scramble teams and assign random champion to each player
    @app_commands.command(name="scramble-champion", description="Divide os times")
    @app_commands.autocomplete(classe=role_autocomplete)
    @app_commands.describe(classe="[Opcional] A classe que você quer que todos usem. Opções: Dano, Tanque, Suporte, Flanco")
    async def _scramblechampion(self, interaction: discord.Interaction, classe: Optional[str] = None):
        
        if classe is None:
            classe = "todos"
        
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
            
        voice_channel = interaction.user.voice.channel
        current_guild = interaction.guild_id
        time1 = self.client.get_channel(settings[str(current_guild)]["Time 1"])
        time2 = self.client.get_channel(settings[str(current_guild)]["Time 2"])
        troca_time = self.client.get_channel(settings[str(current_guild)]["Troca Time"])

        members = troca_time.members
        member_list = []
        team1 = []
        
        auto_move = settings[str(current_guild)]["automove"]
        excluded_list = settings[str(current_guild)]["ignored ids"]
        
        if settings[str(current_guild)]["Comando"] != -1:
            if settings[str(current_guild)]["Comando"] != interaction.channel_id:
                correct_channel = self.client.get_channel(settings[str(current_guild)]["Comando"])
                await interaction.response.send_message(f"Execute o comando no canal correto: {correct_channel.mention}")
                return

        if voice_channel == troca_time:
            # Separando os times e movendo para call
            print("\n-----------------------------------")
            print("Trocando times...")
            for member in members:
                if member.id not in excluded_list:
                    member_list.append(member)

            for i in range(round(len(member_list) / 2)):
                user = rd.choice(member_list)
                team1.append(user)
                member_list.remove(user)

            if auto_move:
                for mem in team1:
                    await mem.move_to(time1)

                for users in member_list:
                    await users.move_to(time2)


            # Assembling team compisitions
            team1_champions = createRandomCrew(len(team1), classe)
            team2_champions = createRandomCrew(len(member_list), classe)

            print(f"Time 1 - {team1}\n\nTime 2 - {member_list}")
            print("\nTroca de times finalizado com êxito")
            print("-----------------------------------")

            # Criando a imagem dos times criados
            teams_image = Image.open("teams.png")
            #  Inserindo foto de perfil + nome dos membros do time 1
            for index, users_team1 in enumerate(team1):
                data = BytesIO(await users_team1.display_avatar.read())
                user_nick = users_team1.display_name
                pfp_size = 150
                font_size = 50
                font_champ = 45

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 53
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                font_champion_name = ImageFont.truetype('Franklin-Gothic.TTF', size=font_champ)

                draw.text((xcord + pfp_size + 10, ycord + pfp_size / 2 - font_size), user_nick, font=font,
                        stroke_width=4, stroke_fill=(0, 0, 0, 255))
                draw.text((xcord + pfp_size + 10, ycord + pfp_size / 2 + font_champ/3), team1_champions[index],
                        font=font_champion_name, fill=(255, 246, 77, 255),
                        stroke_width=4, stroke_fill=(0, 0, 0, 255))

            #  Inserindo foto de perfil + nome dos membros do time 2
            for index, users_team2 in enumerate(member_list):
                data = BytesIO(await users_team2.display_avatar.read())
                user_nick = str(users_team2.display_name)
                pfp_size = 150
                font_size = 50
                font_champ = 45

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 1717
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                font_champion_name = ImageFont.truetype('Franklin-Gothic.TTF', size=font_champ)
                draw.text((xcord - 10, ycord + pfp_size / 2 - font_size), user_nick, font=font, align="right", anchor="rt",
                        stroke_width=4, stroke_fill=(0, 0, 0, 255))
                draw.text((xcord - 10, ycord + pfp_size / 2 + font_champ/3), team2_champions[index],
                        font=font_champion_name, align="right", anchor="rt",  fill=(255, 246, 77, 255),
                        stroke_width=4, stroke_fill=(0, 0, 0, 255))

            with BytesIO() as a:
                teams_image.save(a, "PNG")
                a.seek(0)
                await interaction.response.send_message("Os times foram criados!", file=discord.File(a, "Times_Criados.png"))
        else:
            await interaction.response.send_message(f"Você precisa estar no {troca_time.mention} para executar o comando.")
    
    #------------------------------------------------------------------------------------------------------------------
    # PREFIX COMMANDS
    # Scramble
    @commands.command(aliases=["s"])
    async def scramble(self, ctx):
        
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
            
        voice_channel = ctx.author.voice.channel
        current_guild = ctx.author.guild.id
        time1 = self.client.get_channel(settings[str(current_guild)]["Time 1"])
        time2 = self.client.get_channel(settings[str(current_guild)]["Time 2"])
        troca_time = self.client.get_channel(settings[str(current_guild)]["Troca Time"])
        
        members = troca_time.members
        member_list = []
        team1 = []
        
        auto_move = settings[str(current_guild)]["automove"]
        excluded_list = settings[str(current_guild)]["ignored ids"]
        
        if settings[str(current_guild)]["Comando"] != -1:
            if settings[str(current_guild)]["Comando"] != ctx.channel.id:
                correct_channel = self.client.get_channel(settings[str(current_guild)]["Comando"])
                await ctx.send(f"Execute o comando no canal correto: {correct_channel.mention}")
                return
        
        if voice_channel == troca_time:
            # Separando os times e movendo para call
            print("\n-----------------------------------")
            print("Trocando times...")
            for member in members:
                if member.id not in excluded_list:
                    member_list.append(member)

            for i in range(round(len(member_list) / 2)):
                user = rd.choice(member_list)
                team1.append(user)
                member_list.remove(user)

            if auto_move:
                print("AUTOMOVE IS ON")
                for mem in team1:
                    await mem.move_to(time1)

                for users in member_list:
                    await users.move_to(time2)
            else:
                print("AUTOMOVE IS OFF")

            print(f"Time 1 - {team1}\n\nTime 2 - {member_list}")
            print("\nTroca de times finalizado com êxito")
            print("-----------------------------------")

            # Criando a imagem dos times criados
            teams_image = Image.open("teams.png")
            #  Inserindo foto de perfil + nome dos membros do time 1
            for index, users_team1 in enumerate(team1):
                data = BytesIO(await users_team1.display_avatar.read())
                user_nick = users_team1.display_name
                pfp_size = 150
                font_size = 50

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 53
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                draw.text((xcord + pfp_size + 10, ycord + pfp_size / 2 - font_size), user_nick, font=font,
                          stroke_width=4, stroke_fill=(0, 0, 0, 255))

            #  Inserindo foto de perfil + nome dos membros do time 2
            for index, users_team2 in enumerate(member_list):
                data = BytesIO(await users_team2.display_avatar.read())
                user_nick = str(users_team2.display_name)
                pfp_size = 150
                font_size = 50

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 1717
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                draw.text((xcord - 10, ycord + pfp_size / 2 - font_size), user_nick, font=font, align="right",
                          anchor="rt",
                          stroke_width=4, stroke_fill=(0, 0, 0, 255))

            await ctx.send("Times foram criados!")
            with BytesIO() as a:
                teams_image.save(a, "PNG")
                a.seek(0)
                await ctx.send(file=discord.File(a, "Times_Criados.png"))
        else:
            await ctx.send(f"Você precisa estar no canal {troca_time.mention} para poder executar o comando")

    # Scramble teams and assign random champion to each player
    @commands.command(name="scramble-champion",
                    aliases=["sc", "scramblechamp", "scramblec", "scramblechampion"],
                    description="Divide os times e escolhe um champion para cada membro da equipe"
                    )
    async def scramblechampion(self, ctx, classe: str=""):
        with open("cogs/ServerSettings.json", "r") as f:
            settings = json.load(f)
        
        
        if classe == "":
            classe = "todos"
            
        voice_channel = ctx.author.voice.channel
        current_guild = ctx.author.guild.id
        time1 = self.client.get_channel(settings[str(current_guild)]["Time 1"])
        time2 = self.client.get_channel(settings[str(current_guild)]["Time 2"])
        troca_time = self.client.get_channel(settings[str(current_guild)]["Troca Time"])

        members = troca_time.members
        member_list = []
        team1 = []
        
        auto_move = settings[str(current_guild)]["automove"]
        excluded_list = settings[str(current_guild)]["ignored ids"]
        
        if settings[str(current_guild)]["Comando"] != -1:
            if settings[str(current_guild)]["Comando"] != ctx.channel.id:
                correct_channel = self.client.get_channel(settings[str(current_guild)]["Comando"])
                await ctx.send(f"Execute o comando no canal correto: {correct_channel.mention}")
                return

        if voice_channel == troca_time:
            # Separando os times e movendo para call
            print("\n-----------------------------------")
            print("Trocando times...")
            for member in members:
                if member.id not in excluded_list:
                    member_list.append(member)

            for i in range(round(len(member_list) / 2)):
                user = rd.choice(member_list)
                team1.append(user)
                member_list.remove(user)

            if auto_move:
                for mem in team1:
                    await mem.move_to(time1)

                for users in member_list:
                    await users.move_to(time2)

            # Assembling team compisitions
            team1_champions = createRandomCrew(len(team1), classe.lower())
            team2_champions = createRandomCrew(len(member_list), classe.lower())

            print(f"Time 1 - {team1}\n\nTime 2 - {member_list}")
            print("\nTroca de times finalizado com êxito")
            print("-----------------------------------")

            # Criando a imagem dos times criados
            teams_image = Image.open("teams.png")
            #  Inserindo foto de perfil + nome dos membros do time 1
            for index, users_team1 in enumerate(team1):
                data = BytesIO(await users_team1.display_avatar.read())
                user_nick = users_team1.display_name
                pfp_size = 150
                font_size = 50
                font_champ = 45

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 53
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                font_champion_name = ImageFont.truetype('Franklin-Gothic.TTF', size=font_champ)

                draw.text((xcord + pfp_size + 10, ycord + pfp_size / 2 - font_size), user_nick, font=font,
                          stroke_width=4, stroke_fill=(0, 0, 0, 255))
                draw.text((xcord + pfp_size + 10, ycord + pfp_size / 2 + font_champ / 3), team1_champions[index],
                          font=font_champion_name, fill=(255, 246, 77, 255),
                          stroke_width=4, stroke_fill=(0, 0, 0, 255))

            #  Inserindo foto de perfil + nome dos membros do time 2
            for index, users_team2 in enumerate(member_list):
                data = BytesIO(await users_team2.display_avatar.read())
                user_nick = str(users_team2.display_name)
                pfp_size = 150
                font_size = 50
                font_champ = 45

                pfp = Image.open(data)
                pfp = pfp.resize((pfp_size, pfp_size))
                user_nick = f"{user_nick[:32]}..." if len(user_nick) > 32 else user_nick
                xcord = 1717
                ycord = 179 + index * (26 + pfp_size)
                teams_image.paste(pfp, (xcord, ycord))

                draw = ImageDraw.Draw(teams_image)
                font = ImageFont.truetype('Franklin-Gothic.TTF', size=font_size)
                font_champion_name = ImageFont.truetype('Franklin-Gothic.TTF', size=font_champ)
                draw.text((xcord - 10, ycord + pfp_size / 2 - font_size), user_nick, font=font, align="right",
                          anchor="rt",
                          stroke_width=4, stroke_fill=(0, 0, 0, 255))
                draw.text((xcord - 10, ycord + pfp_size / 2 + font_champ / 3), team2_champions[index],
                          font=font_champion_name, align="right", anchor="rt", fill=(255, 246, 77, 255),
                          stroke_width=4, stroke_fill=(0, 0, 0, 255))

            with BytesIO() as a:
                teams_image.save(a, "PNG")
                a.seek(0)
                await ctx.send("Os times foram criados!", file=discord.File(a, "Times_Criados.png"))
        else:
            await ctx.send(f"Você precisa estar no {troca_time.mention} para executar o comando.")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Scramble(client))
