import random
import uuid
import os
from ast import literal_eval


def load_cmd_sets():
    global cmd_sets
    global cmd_sets_name
    global available_cmd
    available_cmd = []
    # list of currently available commands
    cmd_sets = []
    # List of lists containing all available commands for any given situation
    cmd_sets_name = []
    # names to remember list by
    cmd_sets_file = open("Assets/cmd_sets.txt", "r")
    cmd_sets_lines = cmd_sets_file.read().split("\n")
    for line in cmd_sets_lines:
        if len(line.strip(", ")) > 0:
            cmd_sets_full_str = line.split(":")
            cmd_sets_name.append(cmd_sets_full_str[0])
            cmd_sets.append(cmd_sets_full_str[1].split(","))
    cmd_sets_file.close()


def set_avail_cmd(cmd_set_name):
    # sets all commands that are currently available to player
    global available_cmd
    found = False
    index = 0
    # match and stop search for command set
    while not found and index < len(cmd_sets_name):
        if cmd_set_name == cmd_sets_name[index]:
            found = True
            available_cmd = cmd_sets[index]
        index += 1
    if not found:
        return False
    else:
        return True


def cmd_interpreter():
    global all_cmd
    global quit_interpreter
    while not quit_interpreter:
        print("")
        current_cmd_string = input(">: ")
        print("")
        if not current_cmd_string.strip() == "":
            current_cmd = current_cmd_string.lower().rstrip().split(" ", 1)
            # Checks if command is a valid command and if the command is valid for current context
            if current_cmd[0] in all_cmd and current_cmd[0] in available_cmd:
                # print("Understood Command:", current_cmd[0])
                if len(current_cmd) > 1:
                    all_cmd[current_cmd[0]](current_cmd[1])
                else:
                    all_cmd[current_cmd[0]]()
            elif current_cmd[0] in all_cmd:
                print(dialogue["cmd.unavailable"])
            else:
                print(dialogue["cmd.unknown"])
    return


def load_dialogue(lang="en_us"):
    # Language support
    # Use dictionary to store all of game dialogue
    # access using dialogue["KEY NAME"]
    # https://www.w3schools.com/python/python_dictionaries.asp
    global dialogue
    dialogue = {}
    dialogue_file = open("Assets/dialogue/" + lang + ".txt", "r")
    dialogue_lines = dialogue_file.read().split("\n")
    for line in dialogue_lines:
        if len(line.strip(", ")) > 0:
            dialogue_str = line.split(":")
            dialogue[dialogue_str[0]] = str(dialogue_str[1])
    dialogue_file.close()
    return


def get_items():
    global all_weapons
    global weapon_type
    global item_lookup  # dictionary with translated names as key. used to find internal name
    global item_effect
    global item_strength
    global item_name
    global item_rarity
    global item_gen
    items_file = open("Assets/items.csv", "r")
    items_str = items_file.read().split("\n")
    for line in items_str:
        if len(line.strip(", ")) > 0:
            item_list = line.split(",")
            item_name.append(item_list[0])
            item_effect.append(item_list[1])
            item_strength.append(item_list[2])
            item_rarity.append(item_list[3])
            item_lookup[dialogue[item_list[0]].lower()] = item_list[0]
            if item_list[1] == 'weapon':
                weapon_type[item_list[0]] = item_list[4]
                if item_list[0] not in all_weapons:
                    all_weapons.add(item_list[0])
            if item_list[3] not in item_gen:
                item_gen[item_list[3]] = []
            item_gen[item_list[3]].append(item_list[0])
    return


def get_enemies():
    global game_enemies
    global enemy_gen
    enemies_file = open("Assets/enemies.csv", "r")
    enemies_str = enemies_file.read().split("\n")
    for line in enemies_str:
        if len(line.strip(", ")) > 0:
            enemy_list = line.split(",")
            game_enemies[enemy_list[0]] = list()
            game_enemies[enemy_list[0]].append(int(enemy_list[1]))  # Health
            game_enemies[enemy_list[0]].append(int(enemy_list[2]))  # Strength
            game_enemies[enemy_list[0]].append(enemy_list[3])  # rarity
            game_enemies[enemy_list[0]].append(enemy_list[4])  # resistance
            game_enemies[enemy_list[0]].append(enemy_list[5])  # vulnerability
            if enemy_list[3] not in enemy_gen:
                enemy_gen[enemy_list[3]] = []
            enemy_gen[enemy_list[3]].append(enemy_list[0])

    return


def load_save(save_name=''):  # load items to correct locations in game
    global save_file_name
    save_file_name = os.path.join("Saves", save_name, "")
    global x_pos
    global y_pos
    global visited_rooms
    global rooms
    global world_items
    global world_enemies
    global char_inventory
    global char_health
    global char_defense
    global boss_spawned
    save_data = {}
    save_file_path = os.path.join("Saves", save_name, "main.txt")
    save_file = open(save_file_path, "r")
    save_lines = save_file.read().split("\n")
    for line in save_lines:
        if len(line.strip(", ")) > 0:
            save_str = line.split(":", 1)
            save_data[save_str[0]] = save_str[1]
    try:
        x_pos = int(save_data['x_pos'])
        y_pos = int(save_data['y_pos'])
        visited_rooms = int(save_data['visited_rooms'])
        boss_spawned = literal_eval(save_data['boss_spawned'])
        char_health = int(save_data['char_health'])
        char_defense = int(save_data['char_defense'])
        rooms = literal_eval(save_data['rooms'])
        world_items = literal_eval(save_data['world_items'])
        world_enemies = literal_eval(save_data['world_enemies'])
        char_inventory = literal_eval(save_data['char_inventory'])
        save_file.close()
    except KeyError:
        print(dialogue['menu.loadFailed'])
        load_menu()

    return


def create_save(save="save1"):
    global x_pos
    global y_pos
    global visited_rooms
    global rooms
    global world_items
    global world_enemies
    global char_inventory
    global char_health
    global char_defense
    global boss_spawned
    # sets initial variable values
    x_pos = 0
    y_pos = 0
    visited_rooms = 0
    rooms = {0: {0: [0, '']}}
    world_enemies = {}
    world_items = {}
    char_inventory = {'item.axe': 1}  # internal item name, quantity
    char_health = 20
    char_defense = 1
    print(dialogue['start.createSave'])
    if not os.path.exists(os.path.join("Saves", save)):
        os.mkdir(os.path.join("Saves", save))
    save_file_path = os.path.join("Saves", save, "main.txt")
    save_file = open(save_file_path, "w")
    save_file.write("x_pos:" + str(x_pos) + "\n")
    save_file.write("y_pos:" + str(y_pos) + "\n")
    save_file.write("visited_rooms:" + str(visited_rooms) + "\n")
    save_file.write("boss_spawned:" + str(boss_spawned) + "\n")
    save_file.write("char_health:" + str(char_health) + "\n")
    save_file.write("char_defense:" + str(char_defense) + "\n")
    save_file.write("rooms:" + str(rooms) + "\n")
    save_file.write("world_enemies:" + str(world_enemies) + "\n")
    save_file.write("world_items:" + str(world_items) + "\n")
    save_file.write("char_inventory:" + str(char_inventory) + "\n")
    save_file.close()
    return


def save_file_search():
    all_saves = set()
    for directory in os.listdir(os.path.join(os.getcwd(), "Saves")):
        all_saves.add(directory)
    if ".DS_Store" in all_saves:
        all_saves.discard(".DS_Store")
    return all_saves


def load_menu():
    # loads and prints menu art
    menu_art_file = open("Assets/Art/Menu/logo.txt", "r")
    menu_art = menu_art_file.read()
    menu_art_file.close()
    print(menu_art)
    set_avail_cmd("menu.main")
    print(dialogue['menu.selections'])
    return


def create_room(x, y):
    global world_enemies
    global visited_rooms
    global boss_spawned
    visited_rooms += 1
    if debug_text:
        print("%d" % visited_rooms)
    spawning_chance = random.randint(0, 100)
    if debug_text:
        print(dialogue['debug.createRoom'])
    if visited_rooms > difficulty and not boss_spawned:
        spawning_chance = 101
    if spawning_chance == 101:  # Spawn Boss
        spawned_entity = 2
        enemy_type = random.choice(enemy_gen['boss'])
        entity_uuid = str(uuid.uuid4())
        health = game_enemies[enemy_type][0]
        enemy_attack = game_enemies[enemy_type][1]
        world_enemies[entity_uuid] = [enemy_type, health, enemy_attack]
        boss_spawned = True
    elif spawning_chance >= 75:  # Spawns item if chance over 75%
        spawned_entity = 1
        entity_uuid = str(uuid.uuid4())
        item_spawn_chance = random.randint(0, 100)
        if item_spawn_chance == 100:  # legendary
            item_type = random.choice(item_gen['legendary'])
        elif item_spawn_chance >= 99:  # rare
            item_type = random.choice(item_gen['rare'])
        elif item_spawn_chance >= 90:  # uncommon
            item_type = random.choice(item_gen['uncommon'])
        else:  # common
            item_type = random.choice(item_gen['common'])
        if debug_text:
            print(dialogue['debug.spawnedItem'] % dialogue[item_type])
        world_items[entity_uuid] = [item_type]
    elif spawning_chance >= 50:  # spawn enemy
        spawned_entity = 2
        entity_uuid = str(uuid.uuid4())
        enemy_spawn_chance = random.randint(0, 100)
        if enemy_spawn_chance >= 100:  # rare
            enemy_type = random.choice(enemy_gen['rare'])
        elif enemy_spawn_chance >= 90:  # uncommon
            enemy_type = random.choice(enemy_gen['uncommon'])
        else:  # common
            enemy_type = random.choice(enemy_gen['common'])
        if debug_text:
            print(dialogue['debug.spawnedEnemy'] % dialogue[enemy_type])
        health = game_enemies[enemy_type][0]
        enemy_attack = game_enemies[enemy_type][1]
        world_enemies[entity_uuid] = [enemy_type, health, enemy_attack]
    else:
        if debug_text:
            print(dialogue['debug.noSpawn'])
        spawned_entity = 0
        entity_uuid = ''
    if x not in rooms:
        rooms[x] = {}
    rooms[x][y] = [spawned_entity, entity_uuid]  # nothing = 0, item = 1, enemy = 2
    return


def load_room(x, y):
    room_exists = False
    if x in rooms:
        if y in rooms[x]:
            room_exists = True
    if not room_exists:
        create_room(x, y)
    if debug_text:
        print(dialogue['debug.loadRoom'])
    if rooms[x][y][0] == 0:
        print(dialogue['walk.empty'])
    else:
        entity_uuid = rooms[x][y][1]
        if rooms[x][y][0] == 2:
            entity_name = dialogue[world_enemies[entity_uuid][0]]  # Gets name of entity
            if game_enemies[world_enemies[entity_uuid][0]][2] = "boss": # Enemy is boss
                lock_doors = True

        else:
            entity_name = dialogue[world_items[entity_uuid][0]]
        print(dialogue['walk.occupied'] % entity_name)
    if visited_rooms == 14:
        print(dialogue['boss.nearby'])
    return


def game_exit():  # exit the game and finish the process
    global quit_interpreter
    quit_interpreter = True
    return


def walk(direction=''):
    global x_pos
    global y_pos
    moved = False
    if direction.lower() == dialogue['walk.north']:
        x_pos += 1
        moved = True
    elif direction.lower() == dialogue['walk.south']:
        x_pos += -1
        moved = True
    elif direction.lower() == dialogue['walk.east']:
        y_pos += 1
        moved = True
    elif direction.lower() == dialogue['walk.west']:
        y_pos += -1
        moved = True
    if moved:
        print(dialogue['walk.walking'] % direction.title())
        load_room(x_pos, y_pos)
        if debug_text:
            print("X: %d Y: %d" % (x_pos, y_pos))
    elif direction == '':
        print(dialogue['walk.noArgs'])
    else:
        print(dialogue['walk.unknown'])
    return


def game_quit():
    # save game
    global x_pos
    global y_pos
    global visited_rooms
    global rooms
    global world_items
    global world_enemies
    global char_inventory
    global char_health
    global char_defense
    save_file_path = os.path.join(save_file_name, "main.txt")
    # os.remove(save_file_path)
    save_file = open(save_file_path, "w")
    save_file.write("x_pos:" + str(x_pos) + "\n")
    save_file.write("y_pos:" + str(y_pos) + "\n")
    save_file.write("visited_rooms:" + str(visited_rooms) + "\n")
    save_file.write("boss_spawned:" + str(boss_spawned) + "\n")
    save_file.write("char_health:" + str(char_health) + "\n")
    save_file.write("char_defense:" + str(char_defense) + "\n")
    save_file.write("rooms:" + str(rooms) + "\n")
    save_file.write("world_enemies:" + str(world_enemies) + "\n")
    save_file.write("world_items:" + str(world_items) + "\n")
    save_file.write("char_inventory:" + str(char_inventory) + "\n")
    save_file.close()
    load_menu()
    return


def game_start():
    answered_load = False
    save_file = ""
    while not answered_load:
        print(dialogue['start.options'])
        response = input("(Y/N): ")
        if response.lower() == "y":
            avail_save_files = save_file_search()
            save_found = False
            while not save_found:
                print(dialogue['start.selectSave'], end=":\n")
                for save in avail_save_files:
                    print(save)
                save_file_input = input("?: ").lower().strip()
                if save_file_input in avail_save_files:
                    save_found = True
                    answered_load = True
                    save_file = save_file_input
                else:
                    print(dialogue['start.unknown'])
        elif response.lower() == "n":
            print(dialogue['start.nameSave'])
            save_file_input = input("?: ").lower().strip(" ,.:/\\")
            save_file = save_file_input
            create_save(save_file)
            answered_load = True
        else:
            print(dialogue['start.invalidResponse'])
    load_save(save_file)
    print("\n" * 20)
    if debug_immortal:
        print(dialogue['debug.optionsEnabled'])
    if debug_text:
        print(dialogue['debug.start'])
    set_avail_cmd("game.main")  # Sets available commands to those used during gameplay
    load_room(x_pos, y_pos)
    return


def options():
    print(dialogue['menu.options'])
    set_avail_cmd("menu.options")
    return


def menu_reset():
    print(dialogue['menu.resetConfirm'], end="\n\n")
    save_list = save_file_search()
    answered = False
    while not answered:
        response = input("(Y/N): ")
        print()  # line spacing
        if response.upper() == "Y":
            answered = True
            print(dialogue['menu.resetDeleted'])
            for saves in save_list:
                path_to_folder = os.path.join("Saves", saves)
                path_to_file = os.path.join(path_to_folder, "main.txt")
                os.remove(path_to_file)
                os.rmdir(path_to_folder)
        elif response.upper() == "N":
            answered = True
        else:
            print(dialogue['menu.resetUnknown'])
    options()
    return


def menu_back():
    load_menu()
    return


def inventory():
    global char_inventory
    print(dialogue['inventory.title'], end=':\n')
    for entry in char_inventory:
        print(dialogue[entry], "x%d" % char_inventory[entry])
    return


def pickup(item_input=''):
    global char_inventory
    global item_lookup
    if rooms[x_pos][y_pos][0] == 1:  # check if room has item
        item_uuid = rooms[x_pos][y_pos][1]
        room_item = world_items[item_uuid][0]
        if item_input in item_lookup or item_input == '':  # find internal name
            if item_input in item_lookup:
                pickup_item = item_lookup[item_input]
            else:  # assume item in room
                pickup_item = room_item
            if pickup_item == room_item:
                if pickup_item not in char_inventory:  # create entry for item if it doesn't exist
                    char_inventory[pickup_item] = 0
                print(dialogue['pickup.success'] % dialogue[pickup_item])
                char_inventory[pickup_item] += 1
                rooms[x_pos][y_pos] = [0, '']
            else:
                print(dialogue['pickup.noItemNearby'])
    else:
        print(dialogue['pickup.noNearby'])
    return


def consume(item_input=''):
    global item_name
    global item_strength
    global item_effect
    global char_health
    global char_inventory
    if item_input in item_lookup:
        item = item_lookup[item_input]
        if item in char_inventory:
            if debug_text:
                print(dialogue['debug.consume'])
            index = 0
            found = False
            while index < len(item_name) and not found:
                if item == item_name[index]:
                    found = True
                else:
                    index += 1
            if found and 'heal' == item_effect[index]:
                char_health += int(item_strength[index])
                print(dialogue['consume.success'] % (dialogue[item], int(item_strength[index])))
                print(dialogue['consume.hp'] % char_health)
                char_inventory[item] -= 1  # Remove one item from inventory on use
                if char_inventory[item] == 0:
                    char_inventory.pop(item)
            elif found:
                print(dialogue['consume.invalid'])  # found item but item can't be eaten
            # get effects
            # consume
        else:
            print(dialogue['consume.unavailable'])  # item not in inventory
    elif item_input == '':
        print(dialogue['consume.noArgs'])
    else:
        print(dialogue['consume.unknown'])
    return


def attack(weapon_input=''):
    global rooms
    global x_pos
    global y_pos
    global all_weapons
    global item_lookup
    global char_inventory
    global world_enemies
    global char_health
    global char_defense
    global debug_immortal
    global save_file_name
    if rooms[x_pos][y_pos][0] == 2:  # Check if enemy in room
        if weapon_input.lower() in item_lookup:  # search for internal name of weapon
            weapon = item_lookup[weapon_input.lower()]
        elif weapon_input == '':
            weapon = 'attack.hand'
        else:
            weapon = ''
        if (weapon in char_inventory and weapon in all_weapons) or weapon == 'attack.hand':
            weapon_name = weapon_input
            print("attacking with %s" % weapon_name)
            enemy_uuid = rooms[x_pos][y_pos][1]
            attack_enemy_name = dialogue[world_enemies[enemy_uuid][0]]
            attack_enemy_health = world_enemies[enemy_uuid][1]
            attack_enemy_strength = world_enemies[enemy_uuid][2]
            attack_enemy_resistance = game_enemies[world_enemies[enemy_uuid][0]][3]
            attack_enemy_vulnerability = game_enemies[world_enemies[enemy_uuid][0]][4]
            if weapon == 'attack.hand':  # Use hand
                weapon_strength = 1
                attack_weapon_type = ''
            else:  # Lookup weapon strength
                found = False
                index = 0
                while index < len(item_name) and not found:
                    if weapon == item_name[index]:
                        found = True
                    else:
                        index += 1
                weapon_strength = int(item_strength[index])
                attack_weapon_type = weapon_type[weapon]
            if attack_weapon_type == attack_enemy_resistance:
                attack_multiplier = .75  # Enemy Resistant to attack so it takes a %25 reduction in damage
            elif attack_weapon_type == attack_enemy_vulnerability:
                attack_multiplier = 1.25  # Enemy vulnerable to attack so it takes a %25 increase in damage
            else:
                attack_multiplier = 1.0  # Enemy neither vulnerable nor resistant to attack
            attack_enemy_health -= (weapon_strength*attack_multiplier)  # attacks enemy
            world_enemies[enemy_uuid][1] = attack_enemy_health  # stores enemy health in proper location
            print(dialogue['debug.attack'] % ((weapon_strength*attack_multiplier), attack_enemy_name, attack_enemy_health))
            if attack_enemy_health <= 0:  # remove Enemy
                print(dialogue['attack.kill'] % attack_enemy_name)
                world_enemies.pop(enemy_uuid)
                rooms[x_pos][y_pos] = [0, '']  # set room to contain nothing
            else:
                print(dialogue['debug.enemyAttack'] % (attack_enemy_name, attack_enemy_strength))
                if not debug_immortal:
                    char_health -= (attack_enemy_strength - char_defense)
                    print(dialogue['debug.health'] % char_health)
                    if char_health <= 0:
                        print(dialogue['attack.death'])
                        save_file_to_remove = os.path.join(save_file_name, "main.txt")
                        os.remove(save_file_to_remove)  # delete save file
                        os.rmdir(save_file_name)  # delete save file folder
                        load_menu()
                else:
                    print(dialogue['debug.immortal'])
        elif weapon_input in char_inventory:  # if item not a weapon but is a valid item in the player inventory
            print(dialogue['attack.invalidWeapon'])
        else:
            print(dialogue['attack.noWeapon'] % dialogue[weapon])
    else:
        print(dialogue['attack.noTarget'])
    return


# setup all available commands
all_cmd = {'walk': walk,
           'quit': game_quit,
           'start': game_start,
           'back': menu_back,
           'exit': game_exit,
           'reset': menu_reset,
           'options': options,
           'attack': attack,
           'inventory': inventory,
           'use': consume,
           'pickup': pickup}
# initialize
all_weapons = set()
weapon_type = dict()
item_lookup = dict()
item_effect = list()
item_strength = list()
item_name = list()
item_rarity = list()
item_gen = dict()
game_enemies = dict()
enemy_gen = dict()
difficulty = 15
boss_spawned = False
lock_doors = False
load_cmd_sets()
load_dialogue()
get_items()
get_enemies()
# Debug options
debug_immortal = False  # Debug option to prevent damage
debug_text = False  # show debug Text
quit_interpreter = False  # sets loop for command input
# ready to Load menu
load_menu()  # Loads main menu
cmd_interpreter()  # starts text input
