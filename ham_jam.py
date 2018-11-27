import random
import sys


class Entity:
    def __init__(self, health, max_health):
        self.health = health
        self.max_health = max_health


class Character(Entity):
    def __init__(self):
        super(Character, self).__init__()  # supposedly the proper way to declare a subclass
        self.inventory = []
        self.effects = []
        self.level = 1
        self.xp = 1


class Enemy(Entity):
    def __init__(self, strength):
        super(Enemy, self).__init__()
        self.strength = strength


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
    # TODO: implement command matching
    global all_cmd
    quit_interpreter = False
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
    item_name = []
    item_effect = []
    items_file = open("Assets/items.csv", "r")
    items_str = items_file.read().split("\n")
    for line in items_str:
        if len(line.strip(", ")) > 0:
            item_list = line.split(",")
            item_name.append(item_list[0])
            item_effect.append(item_list[1])

    # TODO: get items
    return


def load_save(save_num):  # load items to correct locations in game
    global save_data
    save_data = {}
    save_file = open("Saves/save" + save_num + ".txt", "r")
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
    spawning_chance = random.randint(0, 100)
    if spawning_chance >= 75:  # Spawns item if chance over 75%
        print("spawned item")
        item_spawn_chance = random.randint(0, 100)
        if item_spawn_chance <= 75:
            print("common")
        elif item_spawn_chance <= 90:
            print("uncommon")
        elif item_spawn_chance <= 99:
            print("rare")
        elif item_spawn_chance <= 100:
            print("legendary")
    elif spawning_chance >= 50:  # spawn enemy
        print("spawned enemy")
        enemy_spawn_chance = random.randint(0, 100)
        if enemy_spawn_chance <= 75:
            print("common")
        elif enemy_spawn_chance <= 90:
            print("uncommon")
        elif enemy_spawn_chance <= 99:
            print("rare")
        elif enemy_spawn_chance <= 100:
            print("legendary")
    else:
        print("nothing spawned")
    # TODO: save rooms to save file for later loading
    return


def load_room(x, y):
    room_exists = False
    if not room_exists:
        create_room(x, y)
    # TODO: check if room exists
    # TODO: If room does exist load it from file
    # TODO: If room does not exist create room
    return


def game_exit():  # exit the game and finish the process
    sys.exit()
    return


def walk(direction):
    global x_pos
    global y_pos
    moved = False
    if direction.lower() == dialogue['walk.north']:
        print("walking North")
        x_pos += 1
        moved = True
    elif direction.lower() == dialogue['walk.south']:
        print("walking Sorth")
        x_pos += -1
        moved = True
    elif direction.lower() == dialogue['walk.east']:
        print("walking East")
        y_pos += 1
        moved = True
    elif direction.lower() == dialogue['walk.west']:
        print("walking West")
        y_pos += -1
        moved = True
    if moved:
        load_room(x_pos, y_pos)
        print("X:", x_pos, "Y:", y_pos)
    else:
        print("invalid direction")
    return


def game_quit():
    # save game
    load_menu()

    return


def game_start():
    # TODO: start game
    global x_pos
    global y_pos
    x_pos = 0
    y_pos = 0

    print("starting game")
    set_avail_cmd("game.main")  # Sets available commands to those used during gameplay
    # load first room
    # load room
    return


def options():
    print(dialogue['menu.options'])
    return


all_cmd = {'walk': walk, 'quit': game_quit, 'start': game_start, 'exit': game_exit, 'options': options}
# initialize
load_cmd_sets()
load_dialogue()
# ready Load menu
load_menu()  # Loads main menu
cmd_interpreter()
