from random import randrange


maps = {
    "cerco": [
        "Pico da Ascenção",
        "Bazaar",
        "Ilha dos Sapos",
        "Cachoeira das Onças",
        "Praia da Serpente",
        "Mercadão de Peixes",
        "Serraria da Solidão"
    ],
    "koth": [
        "Snowfall Junction",
        "Magistrate's Archives",
        "Trade District",
        "Marauder's Port"
    ],
    "chacina": [
        "Primal Court",
        "Foreman's Rise",
        "Magistrate's Archives",
        "Marauder's Port"
    ],
    "tdm": [
        "Snowfall Junction",
        "Trade District",
        "Abyss",
        "Throne",
        "Dragon Arena"
    ],
    "teste": [
        "(WIP) Bog District",
        "(WIP) Dark Crossing",
        "(WIP) Eastwatch",
        "(WIP) Moss Garden",
        "(WIP) Salty Springs",
        "(WIP) Sand Bridge",
        "(WIP) Sierra",
        "(WIP) Undercity",
        "(WIP) Waterway"
    ]
}

def choose_map(modo: str):
    modo = modo.lower()
    mapas = maps.copy()
    return mapas[modo][randrange(0, len(mapas[modo]))]