# TODO:Everything


class Entity:
    def __init__(self, health, max_health):
        self.health = health
        self.max_health = max_health


class Character(Entity):
    def __init__(self):
        super(Character, self).__init__()
        self.inventory = []
        self.effects = []


def load_cmd_sets():
    global cmd_sets
    global cmd_sets_name
    global available_cmd
    global all_cmd
    all_cmd = []
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
            # add all new commands to all_cmd list
            for cmd in cmd_sets_full_str[1].split(","):
                if cmd not in all_cmd:
                    all_cmd.append(cmd)
    cmd_sets_file.close()
    print(cmd_sets)


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
    block_input = False
    while not block_input:
        current_cmd = input(">: ")
        if current_cmd.lower() in all_cmd and current_cmd.lower() in available_cmd:
            index = 0
            found = False
            while index <= len(all_cmd) and not found:
                if all_cmd[index].lower() == current_cmd.lower():
                    found = True
                    print("Understood:", current_cmd)
                    # TODO check if command is currently available
                    # TODO Command name resolution
                index += 1
            # match and stop search
        elif current_cmd in all_cmd:
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
            dialogue[dialogue_str[0]] = dialogue_str[1]
    dialogue_file.close()
    return


# functions
def get_rooms():
    # TODO: get rooms
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
    # TODO: load menu
    # loads and prints menu art
    menu_art_file = open("Assets/Art/Menu/logo.txt", "r")
    menu_art = menu_art_file.read()
    menu_art_file.close()
    print(menu_art)
    set_avail_cmd("menu.main")
    print(dialogue['menu.selections'])
    return


def load_room():
    # TODO: Load Room
    return


def load_assets():
    # TODO: Load assets
    return


# initialize
load_cmd_sets()
load_dialogue()
# ready Load menu
load_menu()  # Loads main menu
cmd_interpreter()
