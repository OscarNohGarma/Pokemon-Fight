import os
import random
from pprint import pprint
from time import sleep


from pokeload import getAllPokemons

logo = "                                  ,'\ \n" \
       "    _.----.        ____         ,'  _\   ___    ___     ____\n" \
       "_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.\n" \
       "\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |\n" \
       " \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |\n" \
       "   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |\n" \
       "    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |\n" \
       "     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |\n" \
       "      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |\n" \
       "       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |\n" \
       "        \_.-'       |__|    `-._ |              '-.|     '-.| |   |\n" \
       "                                `'                            '-._|\n"


def get_player_profile(pokemon_list):
    return {
        "player_name": input("¿Cuál es tu nombre de entrenador? "),
        "pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 3
    }


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["currentHealth"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def choose_pokemon(player_profile):
    chosen = None
    print("ELIGE CON QUÉ POKÉMON LUCHARÁS\n")
    while not chosen:

        for index in range(len(player_profile["pokemon_inventory"])):
            print("{}- {}".format(index + 1, get_pokemon_info(player_profile["pokemon_inventory"][index])))
        try:
            pokemon = player_profile["pokemon_inventory"][int(input("\n¿CUÁL ELIGES? ")) - 1]
            if pokemon["currentHealth"] == 0:
                os.system("cls")
                print("\nEste Pokémon está debilitado... Selecciona otro\n")
            else:
                return pokemon
        except (ValueError, IndexError):
            print("\nELIGE UN POKÉMON VÁLIDO")


def get_pokemon_info(pokemon):
    return "{} | Tipo: {} | LV: {} | HP: {}/{}".format(pokemon["name"],
                                                       "/".join(pokemon["type"]),
                                                       pokemon["level"],
                                                       pokemon["currentHealth"],
                                                       pokemon["baseHealth"])


def get_attack_info(attack):
    return "{} | Tipo: {} | Daño: {} | RL: {}".format(attack["name"],
                                                      attack["type"],
                                                      attack["damage"],
                                                      attack["minLevel"])


def pokemon_attack(attack_chosen, rival_pokemon):
    attack_damage = attack_chosen["damage"]
    multiplier = 1.0
    if attack_chosen["type"] == "lucha":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["normal", "hielo", "roca", "siniestro", "acero"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "volador":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["lucha", "planta", "bicho"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "veneno":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["planta", "hada"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "tierra":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["fuego", "electrico", "veneno", "roca", "acero"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "roca":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["fuego", "hielo", "volador", "bicho"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "bicho":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["planta", "psiquico", "siniestro"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "fantasma":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["fantasma", "psiquico"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "acero":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["hielo", "roca", "hada"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "fuego":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["planta", "bicho", "hielo", "acero"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "agua":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["fuego", "tierra", "roca"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "planta":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["agua", "tierra", "roca"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "electrico":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["agua", "volador"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "psiquico":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["lucha", "veneno"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "hielo":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["planta", "tierra", "volador", "dragon"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "dragon":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["dragon"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "siniestro":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["psiquico", "fantasma"]:
                multiplier += 0.5
    elif attack_chosen["type"] == "hada":
        for pokemon_type in rival_pokemon["type"]:
            if pokemon_type in ["lucha", "dragon", "hada"]:
                multiplier += 0.5

    if multiplier == 1.5:
        print("¡El ataque es eficaz!")
    elif multiplier == 2.0:
        print("¡¡EL ATAQUE ES SUPEREFICAZ!!")

    return attack_damage * multiplier


def player_attack(player_pokemon, enemy_pokemon):
    if player_pokemon["currentHealth"] == 0:
        return
    acceded_attacks = []
    attack_chosen = None

    print("\n¿QUÉ ATAQUE DESEAS REALIZAR?")
    while not attack_chosen:
        for index in range(len(player_pokemon["attacks"])):
            try:
                if player_pokemon["level"] >= int(player_pokemon["attacks"][index]["minLevel"]):
                    print("{}- {}".format(index + 1, get_attack_info(player_pokemon["attacks"][index])))
                    acceded_attacks.append(player_pokemon["attacks"][index])
            except ValueError:
                pass
        try:
            attack_chosen = acceded_attacks[int(input("\n")) - 1]
        except (ValueError, IndexError):
            print("\nELIGE UN ATAQUE VÁLIDO")
    os.system("cls")
    print("\n{} ha utilizado {}".format(player_pokemon["name"], attack_chosen["name"]))
    total_damage = pokemon_attack(attack_chosen, enemy_pokemon)
    enemy_pokemon["currentHealth"] -= total_damage
    if enemy_pokemon["currentHealth"] < 0:
        enemy_pokemon["currentHealth"] = 0
    print("\n{}".format(get_pokemon_info(player_pokemon)))
    print("{}".format(get_pokemon_info(enemy_pokemon)))


def enemy_attack(enemy_pokemon, player_pokemon):
    os.system("cls")
    if enemy_pokemon["currentHealth"] == 0:
        return
    acceded_attacks = []
    attack_chosen = None
    for index in range(len(enemy_pokemon["attacks"])):
        try:
            if enemy_pokemon["level"] >= int(enemy_pokemon["attacks"][index]["minLevel"]):
                acceded_attacks.append(enemy_pokemon["attacks"][index])
        except ValueError:
            pass
    try:
        attack_chosen = acceded_attacks[random.randint(0, len(acceded_attacks) - 1)]
        while attack_chosen["damage"] == 0:
            attack_chosen = acceded_attacks[random.randint(0, len(acceded_attacks) - 1)]
    except (ValueError, IndexError):
        pass
    print("\n{} ha utilizado {}".format(enemy_pokemon["name"], attack_chosen["name"]))
    total_damage = pokemon_attack(attack_chosen, player_pokemon)
    player_pokemon["currentHealth"] -= total_damage
    if player_pokemon["currentHealth"] < 0:
        player_pokemon["currentHealth"] = 0
    print("\n{}".format(get_pokemon_info(player_pokemon)))
    print("{}".format(get_pokemon_info(enemy_pokemon)))


def assign_experience(attack_history):
    poke = None
    total_points = 0
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["currentExp"] += points
        total_points += points

        while pokemon["currentExp"] > 20:
            pokemon["currentExp"] -= 20
            pokemon["level"] += 1
            pokemon["baseHealth"] += 10
            pokemon["currentHealth"] = pokemon["baseHealth"]
            print("¡Tu Pokémon ha subido al nivel {}!".format(pokemon["level"]))
        poke = pokemon
    print("{} ha ganado {} de XP".format(poke["name"], total_points))
    print("\n{} | XP: {}/20".format(get_pokemon_info(poke), poke["currentExp"]))


def capture_with_pokeball(enemy_pokemon, player_profile):
    pass


def cure_pokemon(player_profile, player_pokemon):
    pass


def fight(player_profile, enemy_pokemon):
    os.system("cls")
    print("\n--- NUEVO COMBATE ---")
    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    os.system("cls")
    print("\nEnfrentamiento: {} VS {}".format(get_pokemon_info(player_pokemon),
                                              get_pokemon_info(enemy_pokemon)))
    input("PULSA ENTER PARA CONTINUAR")
    os.system("cls")

    print("\n¡{} entra en combate!".format(player_pokemon["name"]))
    print("¡{} entra en combate!".format(enemy_pokemon["name"]))

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["currentHealth"] > 0:
        print("\n{}".format(get_pokemon_info(player_pokemon)))
        print("{}".format(get_pokemon_info(enemy_pokemon)))
        action = None
        while action not in ["A", "P", "V", "C"]:
            action = input("\n¿Qué deseas hacer?: [A]tacar, [P]okéball, Poción de [V]ida, [C]ambiar Pokémon ")

        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            sleep(2)
            input("\nPulsa ENTER para continuar")
            attack_history.append(player_pokemon)
        elif action == "P":
            # Si el usuario tiene pokeballs en el inventario, se tira una,
            # hay una probabilidad de capturarlo relativa a la salud restante el pokémon
            # Cuando se captura pasa a estar en el inventario con la misma salud que tenía
            capture_with_pokeball(enemy_pokemon, player_profile)
        elif action == "V":
            # Si el usuario tiene curas en el inventario se aplica, cura 50 de vida hasta llegar a 100
            # Si el usuario no tiene se cura
            cure_pokemon(player_profile, player_pokemon)
        elif action == "C":
            player_pokemon = choose_pokemon(player_profile)

        enemy_attack(enemy_pokemon, player_pokemon)
        if enemy_pokemon["currentHealth"] > 0:
            sleep(2)
            input("\nPulsa ENTER para continuar")
        os.system("cls")
        if player_pokemon["currentHealth"] == 0 and any_player_pokemon_lives(player_profile):
            print("\nTu {} se ha debilitado\n".format(player_pokemon["name"]))
            player_pokemon = choose_pokemon(player_profile)
            os.system("cls")
            print("\n¡{} entra en combate!".format(player_pokemon["name"]))

    if enemy_pokemon["currentHealth"] == 0:
        print("\n{} ha sido debilitado".format(enemy_pokemon["name"]))
        sleep(1)
        print("¡HAZ GANADO!")
        player_profile["combats"] += 1
        sleep(1)
        assign_experience(attack_history)
        sleep(1)

    print("\n--- FIN DEL COMBATE ---")
    input("Presiona ENTER para continuar")


def item_lottery(player_profile):
    # segun un factor aleatorio, al jugador le puede tocar una pokeball o una cura
    pass


def main_screen():
    print(logo)
    input("                    PULSA ENTER PARA EMPEZAR")


def intro(player_profile):
    os.system("cls")
    print("\nINSTRUCCIONES\n\nSe te asignarán 3 Pokémon de la generación Kanto con los "
          "que tendrás que derrotar a todos los enemigos que te encuentres")
    sleep(3)
    print("¿{}, estás listo?".format(player_profile["player_name"]))
    sleep(2)
    input("\nPulsa ENTER para continuar")


def main():
    main_screen()
    os.system("cls")
    pokemon_list = getAllPokemons()
    sleep(2)
    player_profile = get_player_profile(pokemon_list)
    intro(player_profile)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        item_lottery(player_profile)

    print("Haz perdido en el combate número {}".format(player_profile["combats"]))


if __name__ == "__main__":
    main()
