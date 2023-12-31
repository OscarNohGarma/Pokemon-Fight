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
        "pokeballs": 3,
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
            os.system("cls")
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
            os.system("cls")
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
    pokemon_list = []
    for pokemon in attack_history:
        total_points = 0
        if pokemon not in pokemon_list:
            pokemon_list.append(pokemon)
        points = random.randint(1, 10)
        pokemon["currentExp"] += points
        total_points += points

        while pokemon["currentExp"] >= 20:
            pokemon["currentExp"] -= 20
            pokemon["level"] += 1
            pokemon["baseHealth"] += 10
            pokemon["currentHealth"] = pokemon["baseHealth"]
            print("¡Tu {} ha subido al nivel {}!".format(pokemon["name"], pokemon["level"]))
        poke = pokemon
        print("{} ha ganado {} de XP".format(poke["name"], total_points))
    for pokemon in pokemon_list:
        print("\n{} | XP: {}/20".format(get_pokemon_info(pokemon), pokemon["currentExp"]))


def capture_with_pokeball(enemy_pokemon, player_profile):
    os.system("cls")
    capture = False

    probability = (1 - enemy_pokemon["currentHealth"] / enemy_pokemon["baseHealth"]) * 0.5
    ran_number = random.random()
    if probability == 0:
        probability = 0.1
    print("Probabilidad de captura {}%".format(probability))
    print(ran_number)
    print("1 giro...")
    sleep(1)
    print("2 giros...")
    sleep(2)
    if 0 < ran_number <= probability:
        print("\n¡{} ha sido capturado!".format(enemy_pokemon["name"]))
        enemy_pokemon["currentHealth"] = enemy_pokemon["baseHealth"]
        player_profile["pokemon_inventory"].append(enemy_pokemon)
        capture = True
    else:
        print("\nEl pokémon se ha escapado")
    sleep(1)
    player_profile["pokeballs"] -= 1
    print("\nPokéballs restantes: {}".format(player_profile["pokeballs"]))
    input("\nPulsa ENTER para continuar")
    return capture


def cure_pokemon(player_profile, player_pokemon):
    os.system("cls")
    if player_profile["health_potion"] == 0:
        print("\nNo tienes pociones de vida")
        sleep(1)
        input("\nPulsa ENTER para continuar")
        os.system("cls")
        return False
    else:
        if player_pokemon["currentHealth"] == player_pokemon["baseHealth"]:
            print("\nTu Pokémon ya tiene el máximo de salud")
            input("Pulsa ENTER para continuar")
            os.system("cls")
            return False
        print("\nPociones de vida restantes: {}".format(player_profile["health_potion"]))
        answer = ""
        while answer not in ["S", "N"]:
            answer = input("¿Deseas utilizar una poción de vida en {}? S/N ".format(player_pokemon["name"]))
            os.system("cls")
        if answer == "S":
            player_pokemon["currentHealth"] += 100
            if player_pokemon["currentHealth"] > player_pokemon["baseHealth"]:
                player_pokemon["currentHealth"] = player_pokemon["baseHealth"]
            player_profile["health_potion"] -= 1

            print("\n{}".format(get_pokemon_info(player_pokemon)))
            print("\nHaz utilizado una poción de curación")

            print("Pociones de vida restantes: {}".format(player_profile["health_potion"]))
            sleep(1)
            input("\nPulsa ENTER para continuar")
            return True
        elif answer == "N":
            pass
            os.system("cls")
            return False


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
    catch = False

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["currentHealth"] > 0 and not catch:
        print("\n{}".format(get_pokemon_info(player_pokemon)))
        print("{}".format(get_pokemon_info(enemy_pokemon)))
        action = None
        cure = True
        pokeballs_usable = True

        while action not in ["A", "P", "V", "C"]:
            action = input("\n¿Qué deseas hacer?: [A]tacar, [P]okéball, Poción de [V]ida, [C]ambiar Pokémon ")

        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            sleep(1)
            input("\nPulsa ENTER para continuar")
            attack_history.append(player_pokemon)
        elif action == "P":
            if player_profile["pokeballs"] == 0:
                os.system("cls")
                print("\nNo tienes pokéballs restantes")
                sleep(1)
                input("\nPulsa ENTER para continuar")
                os.system("cls")
                pokeballs_usable = False
            else:
                catch = capture_with_pokeball(enemy_pokemon, player_profile)
        elif action == "V":
            cure = cure_pokemon(player_profile, player_pokemon)
        elif action == "C":
            player_pokemon = choose_pokemon(player_profile)

        if cure and not catch and pokeballs_usable:
            enemy_attack(enemy_pokemon, player_pokemon)
            if enemy_pokemon["currentHealth"] > 0:
                sleep(1)
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
    elif catch:
        os.system("cls")
        print("\n{} ha sido añadido a tu inventario".format(enemy_pokemon["name"]))
        player_profile["combats"] += 1
        sleep(1)
        assign_experience(attack_history)
        sleep(1)

    print("\n--- FIN DEL COMBATE ---")
    input("Presiona ENTER para continuar")


def item_lottery(player_profile):
    random_number = random.randint(1, 100)
    if 0 < random_number <= 15:
        os.system("cls")
        print("\n¡Obtuviste una poción de vida!")
        player_profile["health_potion"] += 1
        print("\nPociones de vida restantes: {}".format(player_profile["health_potion"]))
        sleep(1)
        input("\nPulsa ENTER para continuar")
    elif 15 < random_number <= 30:
        os.system("cls")
        print("\n¡Obtuviste una Pokéball!")
        player_profile["pokeballs"] += 1
        print("\nPokéballs restantes: {}".format(player_profile["pokeballs"]))
        sleep(1)
        input("\nPulsa ENTER para continuar")
    else:
        pass


def main_screen():
    print(logo)
    input("                    PULSA ENTER PARA EMPEZAR")


def intro(player_profile):
    os.system("cls")
    print("\nINSTRUCCIONES\n\nSe te asignarán 3 Pokémon de la generación Kanto con los "
          "que tendrás que derrotar a todos los enemigos que te encuentres")
    sleep(1)
    print("¿{}, estás listo?".format(player_profile["player_name"]))
    sleep(1)
    input("\nPulsa ENTER para continuar")


def main():
    main_screen()
    os.system("cls")
    pokemon_list = getAllPokemons()
    sleep(1)
    player_profile = get_player_profile(pokemon_list)
    intro(player_profile)
    max_pokemon_level = 0

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        for index in range(len(player_profile["pokemon_inventory"])):
            if max_pokemon_level == 0:
                max_pokemon_level = player_profile["pokemon_inventory"][index]["level"]
            elif player_profile["pokemon_inventory"][index]["level"] > \
                    player_profile["pokemon_inventory"][index - 1]["level"]:
                max_pokemon_level = player_profile["pokemon_inventory"][index]["level"]
        input("\nPresiona ENTER para continuar")
        enemy_pokemon["level"] = max_pokemon_level
        enemy_pokemon["baseHealth"] += (max_pokemon_level - 1) * 10
        fight(player_profile, enemy_pokemon)
        item_lottery(player_profile)

    print("Haz perdido en el combate número {}".format(player_profile["combats"]))


if __name__ == "__main__":
    main()
