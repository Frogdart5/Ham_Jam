import random
import uuid


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
        current_cmd_string = input(">: ")
        if not current_cmd_string.strip() == "":
            current_cmd = current_cmd_string.lower().rstrip().split()
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
    global weapon_lookup  # dictionary with translated names as key. used to find internal name
    global item_name
    global item_effect
    global item_strength
    global item_display_key
    global item_rarity
    items_file = open("Assets/items.csv", "r")
    items_str = items_file.read().split("\n")
    for line in items_str:
        if len(line.strip(", ")) > 0:
            item_list = line.split(",")
            item_name.append(item_list[0])
            item_effect.append(item_list[1])
            item_strength.append(item_list[2])
            item_display_key.append(item_list[3])
            item_rarity.append(item_list[4])
            if item_list[1] == 'weapon' and item_list[3] not in all_weapons:
                all_weapons.append(item_list[3])
                weapon_lookup[dialogue[item_list[3]]] = item_list[3]
    return


def load_save(save_num=0):  # load items to correct locations in game
    global save_data
    save_data = {}
    save_file = open("Saves/save" + str(save_num) + ".txt", "r")
    save_lines = save_file.read().split("\n")
    for line in save_lines:
        if len(line.strip(", ")) > 0:
            save_str = line.split(":")
            save_data[save_str[0]] = save_str[1]
    # TODO: put saveFile items in proper memory
    save_file.close()
    return


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
    spawning_chance = random.randint(0, 100)
    print(dialogue['debug.createRoom'])
    if spawning_chance >= 75:  # Spawns item if chance over 75%
        print("spawned item:", end=' ')
        spawned_entity = 1
        entity_uuid = uuid.uuid4()
        item_spawn_chance = random.randint(0, 100)
        if item_spawn_chance == 100:
            print("legendary")
            item_type = 'legendary'
        elif item_spawn_chance >= 99:
            print("rare")
            item_type = 'rare'
        elif item_spawn_chance >= 90:
            print("uncommon")
            item_type = 'uncommon'
        else:
            print("common")
            item_type = 'common'
        world_items[entity_uuid] = [item_type]
    elif spawning_chance >= 50:  # spawn enemy
        spawned_entity = 2
        entity_uuid = uuid.uuid4()
        enemy_spawn_chance = random.randint(0, 100)
        if enemy_spawn_chance == 100:
            enemy_type = 'enemy.legendary'
            health = 10
            enemy_attack = 10
        elif enemy_spawn_chance >= 99:
            enemy_type = 'enemy.rare'
            health = 10
            enemy_attack = 5
        elif enemy_spawn_chance >= 90:
            enemy_type = 'enemy.uncommon'
            health = 10
            enemy_attack = 3
        else:
            enemy_type = 'enemy.common'
            health = 10
            enemy_attack = 2
        print(dialogue['debug.spawnedEnemy'] % dialogue[enemy_type])
        world_enemies[entity_uuid] = [enemy_type, health, enemy_attack]
    else:
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

    print(dialogue['debug.loadRoom'])
    if rooms[x][y][0] == 0:
        print(dialogue['walk.empty'])
    else:
        entity_uuid = rooms[x][y][1]
        if rooms[x][y][0] == 2:
            entity_name = dialogue[world_enemies[entity_uuid][0]]  # Gets name of entity
        else:
            entity_name = entity_uuid
        print(dialogue['walk.occupied'] % entity_name)
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
        print("X: %d Y: %d" % (x_pos, y_pos))
    elif direction == '':
        print(dialogue['walk.noArgs'])
    else:
        print(dialogue['walk.unknown'])
    return


def game_quit():
    # save game
    load_menu()
    return


def game_start():
    # TODO: Load save file for game
    if debug_immortal:
        print(dialogue['debug.optionsEnabled'])
    print(dialogue['debug.start'])
    set_avail_cmd("game.main")  # Sets available commands to those used during gameplay
    load_room(x_pos, y_pos)
    return


def options():
    print(dialogue['menu.options'])
    set_avail_cmd("menu.options")
    return


def inventory():
    global char_inventory
    print(dialogue['inventory.title'], end=':\n')
    for entry in char_inventory:
        print(dialogue[entry])
    return


def attack(weapon_input=''):
    global rooms
    global x_pos
    global y_pos
    global all_weapons
    global weapon_lookup
    global char_inventory
    global world_enemies
    global char_health
    global char_defense
    global debug_immortal
    if rooms[x_pos][y_pos][0] == 2:  # Check if enemy in room
        if weapon_input in weapon_lookup:  # search for internal name of weapon
            weapon = weapon_lookup[weapon_input]
        elif weapon_input == '':
            weapon = 'attack.hand'
        else:
            weapon = ''
        if (weapon in char_inventory and weapon in all_weapons) or weapon == 'attack.hand':
            weapon_name = weapon_input
            print("attacking with %s" % weapon_name)
            enemy_uuid = rooms[x_pos][y_pos][1]
            enemy_health = world_enemies[enemy_uuid][1]
            enemy_strength = world_enemies[enemy_uuid][2]
            enemy_name = dialogue[world_enemies[enemy_uuid][0]]
            if weapon == 'attack.hand':  # Use hand
                weapon_strength = 1
            else:  # Lookup weapon strength
                found = False
                index = 0
                while index < len(item_display_key) and not found:
                    if weapon == item_display_key[index]:
                        found = True
                    else:
                        index += 1
                weapon_strength = int(item_strength[index]) 
            enemy_health -= weapon_strength
            world_enemies[enemy_uuid][1] = enemy_health
            print(dialogue['debug.attack'] % (weapon_strength, enemy_name, enemy_health))
            if enemy_health <= 0:  # remove Enemy
                print(dialogue['attack.kill'] % enemy_name)
                world_enemies.pop(enemy_uuid)
                rooms[x_pos][y_pos] = [0, '']
            else:
                print(dialogue['debug.enemyAttack'] % (enemy_name, enemy_strength))
                if not debug_immortal:
                    char_health -= (enemy_strength - char_defense)
                    print(dialogue['debug.health'] % char_health)
                    if char_health <= 0:
                        print(dialogue['debug.death'])
                        # TODO: handle death situations
                else:
                    print(dialogue['debug.immortal'])
        elif weapon_input in char_inventory:  # if item not a weapon but is a valid item in the player inventory
            print(dialogue['attack.invalidWeapon'])
        else:
            print(dialogue['attack.noWeapon'] % weapon)
    else:
        print(dialogue['attack.noTarget'])
    return


all_cmd = {'walk': walk,
           'quit': game_quit,
           'start': game_start,
           'exit': game_exit,
           'options': options,
           'attack': attack,
           'inventory': inventory}
# initialize
all_weapons = []
weapon_lookup = {}
item_name = []
item_effect = []
item_strength = []
item_display_key = []
item_rarity = []
load_cmd_sets()
load_dialogue()
get_items()
# ready Load menu
load_menu()  # Loads main menu
# sets initial variable values
world_items = {}
x_pos = 0
y_pos = 0
rooms = {0: {0: [0, '']}}
world_enemies = {}
char_inventory = {'item.sword': 1}
char_health = 20
char_defense = 1
debug_immortal = True
quit_interpreter = False
cmd_interpreter()
