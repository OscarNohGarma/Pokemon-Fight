# > <
import pickle
from time import sleep

from requests_html import HTMLSession

pokemonBase = {
    "name": "",
    "currentHealth": 100,
    "baseHealth": 100,
    "level": 1,
    "type": None,
    "currentExp": 0,
    "attacks": None
}

URL_BASE = "https://pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="


def getPokemon(index):
    name = []
    url = "{}{}".format(URL_BASE, index)
    session = HTMLSession()

    newPokemon = pokemonBase.copy()
    pokemonPage = session.get(url)

    newPokemon["type"] = []

    for n in pokemonPage.html.find(".mini", first=True).text:
        if n == "\n":
            break
        name.append(n)
    newPokemon["name"] = ("".join(name))

    for img in pokemonPage.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        newPokemon["type"].append(img.attrs["alt"])

    newPokemon["attacks"] = []
    for atackItem in pokemonPage.html.find(".pkmain")[-1].find("tr .check3"):
        atack = {
            "name": atackItem.find("td", first=True).find("a", first=True).text,
            "type": atackItem.find("td")[1].find("img", first=True).attrs["alt"],
            "minLevel": atackItem.find("th")[1].text,
            "damage": int(atackItem.find("td")[3].text.replace("--", "0"))
        }
        newPokemon["attacks"].append(atack)

    return newPokemon


def getAllPokemons():
    try:
        print("Cargando el archivo de Pokémons...")
        sleep(3)
        with open("pokefile.pkl", "rb") as pokefile:
            allPokemons = pickle.load(pokefile)
    except FileNotFoundError:
        print("Archivo no encontrado. Descargando de internet...")
        allPokemons = []
        sleep(2)
        for index in range(150):
            allPokemons.append(getPokemon((index + 1)))
            print("{}/150".format(index + 1))
        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(allPokemons, pokefile)
            sleep(3)
        print("Todos los pokemons han sido descargados")
        sleep(2)
    print("Lista de Pokémons cargada con éxito")
    return allPokemons



