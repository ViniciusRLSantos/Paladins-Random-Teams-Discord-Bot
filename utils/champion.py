import random as rd


def createRandomCrew(amount_of_people: int, only):
    print(f"{only} - {type(only)}")
    if only.lower() is None or only.lower() == "todos":
        role = ["Damage", "Tank", "Flank", "Support"]
    elif only.lower() == "dano":
        role = ["Damage"]
    elif only.lower() == "tanque":
        role = ["Tank"]
    elif only.lower() == "flanco":
        role = ["Flank"]
    elif only.lower() == "suporte":
        role = ["Support"]
    print(role)
    champs = {
        "Damage": [
            "Betty la Bomba",
            "Bomb King",
            "Cassie",
            "Dredge",
            "Drogoz",
            "Imani",
            "Kasumi",
            "Kinessa",
            "Lian",
            "Octavia",
            "Saati",
            "Sha lin",
            "Strix",
            "Tiberius",
            "Tyra",
            "Viktor",
            "Vivian",
            "Willo"
        ],
        "Tank": [
            "Ash",
            "Atlas",
            "Azaan",
            "Barik",
            "Fernando",
            "Inara",
            "Khan",
            "Makoa",
            "Raum",
            "Ruckus",
            "Terminus",
            "Torvald",
            "Yagorath",
            "Nyx"
        ],
        "Flank": [
            "Androxus",
            "Buck",
            "Caspian",
            "Evie",
            "Koga",
            "Lex",
            "Maeve",
            "Moji",
            "Skye",
            "Talus",
            "Vatu",
            "VII",
            "Vora",
            "Zhin"
        ],
        "Support": [
            "Corvus",
            "Furia",
            "Grohk",
            "Grover",
            "Io",
            "Jenos",
            "Lillith",
            "Mal'Damba",
            "Pip",
            "Rei",
            "Seris",
            "Ying"
        ]
    }
    
    team = []

    for i in range(amount_of_people):
        r = rd.choice(role)
        champ = rd.choice(champs[r])
        champs[r].remove(champ)
        team.append(champ)
    return team