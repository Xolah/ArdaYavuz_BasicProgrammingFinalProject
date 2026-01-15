# HAMNASİA
import random
import time
import sys

def printSlow(text, delay=0.03):
    for char in text:
        print(char, end="")
        time.sleep(delay)
    print()

def textSeperator():
    print("\n", "-" * 40, "\n")


def create_secret_file():
    filename = "SECRET_TOP_TIER_CAREFUL!!!!!!.txt"
    try:
        with open(filename, "w") as f:
            f.write("--- TOP SECRET RECIPE DATA ---\n")
            f.write("Encryption Level: HIGH\n")
            f.write("...\n")
            f.write("The password to the Dark Corridor is: KETCHUP\n")
            f.write("...\n")
            f.write("DO NOT SHARE WITH STUDENTS!")
        printSlow("[SYSTEM]: Check the game files to search for the password.")
    except:
        print("Error: Could not create the file. (Check permissions)")

rooms = {
    "ROOM1": {
        "name": "Main Hall",
        "description": "A grand hall with broken statues. The only way is forward to the KITCHEN.",
        "exits": {"forward": "ROOM2", "kitchen": "ROOM2"},
        "cleared": True,
        "locked": False
    },
    "ROOM2": {
        "name": "Kitchen",
        "description": "It smells like rotten tomatoes here. Shelves are filled with ingredients.",
        "exits": {"back": "ROOM1", "forward": "ROOM3", "dining": "ROOM3"},
        "cleared": False,
        "locked": False
    },
    "ROOM3": {
        "name": "Dining Hall",
        "description": "Tables are overturned. The door ahead is locked. Written on it: 'REA UOY NHUYRA'.",
        "exits": {"back": "ROOM2", "forward": "ROOM4", "lab": "ROOM4"},
        "cleared": False,
        "locked": True
    },
    "ROOM4": {
        "name": "Food Lab",
        "description": "Computers are buzzing... Looks like someone left a PC on.",
        "exits": {"back": "ROOM3"}, 
        "cleared": False,
        "locked": True
    },
    "ROOM5": {
        "name": "Dark Corridor",
        "description": "A heavy steel door blocks the way. It has a keypad asking: '1 + 1 = ?'.",
        "exits": {"back": "ROOM4", "forward": "ROOM6", "Selman's chamber": "ROOM6"},
        "cleared": False,
        "locked": True
    },
    "ROOM6": {
        "name": "Selman's Chamber",
        "description": "The center of chaos. Selman Hoca is chained. The smell of hamburger is overwhelming.",
        "exits": {"back": "ROOM5"},
        "cleared": False,
        "locked": False
    },
}

item_info = {
    "bread":   {"combat": "Heals 30 HP", "passive": "Max HP +10 (Permanent)"},
    "tomato":  {"combat": "ATK +5 (Temp)", "passive": "ATK +2 (Permanent)"},
    "meat":    {"combat": "ATK +10 (Temp)", "passive": "ATK +5 (Permanent)"},
    "lettuce": {"combat": "DEF +3 (Temp)", "passive": "DEF +1 (Permanent)"},
    "cheese":  {"combat": "DEF +5 (Temp)", "passive": "DEF +2 (Permanent)"},
    "patties": {"combat": "None (Ingredient)", "passive": "None"},
    "premium meat": {"combat": "Ingredient", "passive": "Ingredient"},
    "absolute burger": {"combat": "WIN GAME", "passive": "WIN GAME"}
}

class Player():
    def __init__(self):
        self.name = ""
        self.hp = 100
        self.max_hp = 100
        self.attack = 20
        self.defense = 0
        self.crit_rate = 10
        self.luck = 0
        self.inventory = {}    
        self.recipes = []      
        self.current_room = "GATE"

    def setName(self):
        textSeperator()
        printSlow("Enter your name, warrior (Press Enter for default name 'Anton Ego'): ")
        name_input = input(">> ")
        if name_input.strip() == "":
            self.name = "Anton Ego"
        else:
            self.name = name_input
        printSlow(f"Welcome, {self.name}!\n")

    def chooseKit(self):
        textSeperator()
        printSlow("Choose your fighting style:\n")
        print("1. The Vegetarian (Tanky - High HP, Solid Defense)")
        print("2. The Caligula (Aggressive - Good Dmg, Low Defense)")
        print("3. The Omnivore (Balanced - Good Luck)")
        
        while True:
            choice = input("\nSelect kit (1-3): ")
            if choice in ["1", "2", "3"]:
                self.applyKit(choice)
                break
            else:
                print("Invalid choice. Please type 1, 2, or 3.")

    def applyKit(self, choice):
        if choice == "1": # The Vegetarian (Tank)
            self.hp = 130
            self.max_hp = 130
            self.attack = 18
            self.defense = 4
            self.inventory["lettuce"] = 2
            time.sleep(0.5)
            printSlow("\nOh, so you have a big heart for choosing a tanky hero.\nAlright...")
            
        elif choice == "2": # The Caligula (Damage)
            self.hp = 90
            self.max_hp = 90
            self.attack = 25
            self.defense = 1
            self.crit_rate = 20  
            time.sleep(0.5)
            printSlow("\nOh, so you are brave enough to choose a slim hero.\nAlright...")
            
        elif choice == "3": # The Omnivore (Balanced)
            self.hp = 110
            self.max_hp = 110
            self.attack = 20
            self.defense = 2
            self.luck = 15
            self.inventory["bread"] = 1
            time.sleep(0.5)
            printSlow("\nOh, so you are a coward and chose a balanced hero.\nAlright...")
        
        printSlow(f"Hero kit {choice} applied successfully!")
        time.sleep(0.5)

    def printStats(self):
        textSeperator()
        print(f"--- {self.name}'s Stats ---")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"ATK: {self.attack} | DEF: {self.defense}")
        print(f"CRIT: {self.crit_rate}% | LUCK: {self.luck}")
        print("\n--- INVENTORY DETAILS ---")
        
        if not self.inventory:
            print("Your bag is empty.")
        else:
            for item, count in self.inventory.items():
                info = item_info.get(item, {"combat": "???", "passive": "???"})
                print(f"* {item.upper()} (x{count})")
                print(f"  > Combat Effect : {info['combat']}")
                print(f"  > Passive Effect: {info['passive']}")
        textSeperator()

class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.intent = "" 
        self.intent_value = 0
        self.temp_defense = 0

    def is_alive(self):
        return self.hp > 0

    def decide_action(self):
        self.temp_defense = 0
        roll = random.randint(1, 100)
        
        can_heal = self.hp < self.max_hp

        attack_threshold = 60
        if "Meat" in self.name: attack_threshold = 50
        elif "Lettuce" in self.name: attack_threshold = 80

        if roll > attack_threshold + 15 and not can_heal:
            roll = 1

        if roll <= attack_threshold:
            self.intent = "ATTACK"
            self.intent_value = self.damage
            return f"is preparing to ATTACK! ({self.damage} DMG)"
            
        elif roll <= attack_threshold + 15:
            self.intent = "DEFEND"
            self.intent_value = self.damage // 2
            return f"is raising a SHIELD! (+{self.intent_value} Def)"
            
        else:
            self.intent = "HEAL"
            self.intent_value = 15
            return f"is eating a snack to HEAL! (+{self.intent_value} HP)"

def combat_loop(player, enemies):
    textSeperator()
    printSlow(f"!!! BATTLE STARTED !!! Enemies: {len(enemies)}")
    
    bonus_atk = 0
    bonus_def = 0
    
    while player.hp > 0:
        
        active_enemies = []
        for e in enemies:
            if e.is_alive():
                active_enemies.append(e)
        
        if len(active_enemies) == 0:
            break

        print("\n--- ENEMY INTENTS ---")
        total_enemy_damage = 0
        for i, enemy in enumerate(active_enemies):
            action_text = enemy.decide_action()
            print(f"#{i+1}: {enemy.name} [{enemy.hp}/{enemy.max_hp} HP] -> {action_text}")
            if enemy.intent == "ATTACK":
                total_enemy_damage += enemy.intent_value

        player_turn_over = False
        isDefending = False
        
        while not player_turn_over:
            curr_atk = player.attack + bonus_atk
            curr_def = player.defense + bonus_def
            
            print(f"\n--- YOUR TURN (HP: {player.hp}/{player.max_hp}) ---")
            print(f"Stats with Buffs -> ATK: {curr_atk} | DEF: {curr_def}")
            print("1. attack [id]")
            print("2. defend (Block x3)")
            print("3. +use [item] (Temporary Battle Buffs)")
            
            action = input(">> ").strip().lower()
            parts = action.split(" ")
            cmd = parts[0]
            
            if cmd == "+stats":
                player.printStats()
                continue
            
            elif cmd == "+use":
                if len(parts) > 1:
                    item_name = parts[1]
                    if item_name in player.inventory and player.inventory[item_name] > 0:
                        
                        if "bread" in item_name:
                            heal = 30
                            player.hp = min(player.max_hp, player.hp + heal)
                            printSlow(f"Used Bread. Healed {heal} HP!")
                        
                        elif "tomato" in item_name:
                            bonus_atk += 5
                            printSlow(f"Used Tomato. Temporary Attack +5!")
                        
                        elif "meat" in item_name:
                            bonus_atk += 10
                            printSlow(f"Used Meat. Temporary Attack +10!")
                        
                        elif "lettuce" in item_name:
                            bonus_def += 3
                            printSlow(f"Used Lettuce. Temporary Defense +3!")
                        
                        elif "cheese" in item_name:
                            bonus_def += 5
                            printSlow(f"Used Cheese. Temporary Defense +5!")
                        
                        player.inventory[item_name] -= 1
                        if player.inventory[item_name] == 0: del player.inventory[item_name]
                        
                        player_turn_over = True
                    else:
                        print("You don't have that item.")
                else:
                    print("Use what?")

            elif cmd == "attack":
                target_index = 0
                if len(parts) > 1 and parts[1].isdigit():
                    target_index = int(parts[1]) - 1
                
                if 0 <= target_index < len(active_enemies):
                    target = active_enemies[target_index]
                    
                    is_crit = random.randint(1, 100) <= player.crit_rate
                    total_atk = player.attack + bonus_atk
                    dmg = total_atk * 2 if is_crit else total_atk
                    
                    trueDamage = max(0, dmg - target.temp_defense)
                    target.hp -= trueDamage
                    
                    if is_crit:
                        printSlow(f"CRITICAL! You dealt {trueDamage} damage to {target.name}!")
                    else:
                        printSlow(f"You hit {target.name} for {trueDamage} damage.")
                    
                    if not target.is_alive():
                        printSlow(f"-> {target.name} is defeated!")
                        
                        drop_item = ""
                        if "Tomato" in target.name: drop_item = "tomato"
                        elif "Bread" in target.name: drop_item = "bread"
                        elif "Lettuce" in target.name: drop_item = "lettuce"
                        elif "Cheese" in target.name: drop_item = "cheese"
                        elif "Meat" in target.name: drop_item = "meat"
                        
                        if drop_item:
                            drop_count = 2
                            if random.randint(1, 100) <= (player.luck * 3):
                                drop_count += 1
                                print("(Luck Bonus! Found extra loot!)")
                                
                            if drop_item in player.inventory: player.inventory[drop_item] += drop_count
                            else: player.inventory[drop_item] = drop_count
                            printSlow(f"-> Enemy dropped: {drop_count} {drop_item.upper()}")

                    player_turn_over = True
                else:
                    print("Invalid target!")
                    
            elif cmd == "defend":
                total_def = player.defense + bonus_def
                block_amount = total_def * 3
                printSlow(f"Guard UP! Blocking {block_amount} damage.")
                player_turn_over = True
            else:
                print("Invalid command.")

        if len(active_enemies) > 0:
            print("\n--- ENEMY TURN ---")
            damage_taken = 0
            
            for enemy in active_enemies:
                if not enemy.is_alive(): continue
                
                if enemy.intent == "ATTACK":
                    total_def = player.defense + bonus_def
                    block_val = total_def * 3 if isDefending else total_def
                    
                    dmg = max(0, enemy.intent_value - block_val)
                    damage_taken += dmg
                    
                elif enemy.intent == "HEAL":
                    old_hp = enemy.hp
                    enemy.hp = min(enemy.max_hp, enemy.hp + enemy.intent_value)
                    print(f"{enemy.name} healed. (HP: {old_hp} -> {enemy.hp})")
            
            if damage_taken > 0:
                player.hp -= damage_taken
                printSlow(f"OUCH! Took {damage_taken} damage! (HP: {player.hp})")
            elif total_enemy_damage > 0:
                printSlow("BLOCKED! You took 0 damage.")
            
            time.sleep(1)

    if player.hp <= 0:
        printSlow("YOU DIED... Game Over.")
        sys.exit()
    else:
        printSlow("\nVICTORY! All enemies are defeated.")
        return "WON"

game_running = True 

def mainGameLoop():
    global game_running
    
    player = Player()
    
    textSeperator()
    printSlow("----HAMNESİA----\n\n\n\n\n")
    printSlow("NARRATOR: The world has lost its flavor...")
    printSlow("NARRATOR: Many years have passed since the Great Chef Selman lost the 'Absolute Hamburger Recipe'.")
    printSlow("NARRATOR: Food tyrants took over the school. Students are starving.")
    printSlow("NARRATOR: But a hero was born from the ashes of a burnt toast...")
    time.sleep(1)
    
    player.setName()
    player.chooseKit()
    
    printSlow(f"\nNARRATOR: {player.name}, you gathered all your courage and stood before the Gastronomy Consulate.")
    printSlow("NARRATOR: Your mission: Find the recipe, feed Selman Hoca, and restore peace.")
    printSlow("NARRATOR: But wait! A Cheese Guard is blocking the entrance.")
    textSeperator()
    
    printSlow("TUTORIAL: Before you enter place, you must learn the basics:")
    printSlow("1. COMMANDS: Type '+help' anytime to see what you can do.")
    printSlow("2. COMBAT: Enemies' intentions will be shown. Use 'defend' if necessary.")
    printSlow("3. ITEMS: You can use items by typing '+use [item_name]'")
    printSlow("- BUT, be careful about when to use those items!\n- Because the boost that consumables gave is temproary within fight and permanent else.")
    printSlow("4. NAVIGATION: Use '+go [place]' to move between rooms.")
    print("\n(Press Enter to confront the guard and start your journey...)")
    input()
    
    
    printSlow(f"Cheese Guard: 'HEY! Humans are forbidden!'")
    print("\n--- TUTORIAL FIGHT ---")
    print(f"1. Cheese Guard (HP: 10/10) -> is shouting at you!")
    
    while True:
        print(f"\nYour Turn! Type 'attack 1' to shut him up.")
        tut_cmd = input(">> ").strip().lower()
        if tut_cmd == "attack 1":
            printSlow("CRITICAL HIT! 999 Damage! The Cheese Guard is dead.")
            break
        else:
            print("Just type 'attack 1'.")
            
    printSlow("\nNow the real challenge begins.")
    player.current_room = "ROOM1"
    rooms["ROOM1"]["visited"] = True
    
    textSeperator()
    printSlow(f"--- {rooms['ROOM1']['name']} ---")
    printSlow(rooms['ROOM1']['description'])
    textSeperator()

    while game_running:
        print("\nWhat will you do? (+help, +map, +inv, +go [place])")
        user_input = input(">> ").strip().lower()
        parts = user_input.split(" ", 1)
        command = parts[0]
        argument = parts[1] if len(parts) > 1 else None

        if command == "+quit":
            printSlow("Exiting... Goodbye!")
            game_running = False
            
        elif command == "+help":
            textSeperator()
            print("COMMAND LIST:")
            print("+stats        : Show character stats")
            print("+inv          : Open inventory")
            print("+map          : Show current location")
            print("+go [place]   : Move to a room")
            print("+use [item]   : Eat food (permanently buffs stats)")
            print("+craft        : Combine ingredients")
            print("+answer [text]: Solve puzzles")
            print("+quit         : Exit game")
            if player.current_room == "ROOM4":
                print("\nROOM SPECIFIC:")
                print("+search       : Investigate room")
                print("+use computer : Hack terminal")
                print("+enter [code] : Unlock door")
            textSeperator()
        
        elif command == "+stats":
            player.printStats()
            
        elif command == "+inv":
            player.printStats()
            
        elif command == "+map":
            print(f"Current Location: {rooms[player.current_room]['name']}")
            print("Paths:")
            for direction, room_id in rooms[player.current_room]["exits"].items():
                print(f"- {rooms[room_id]['name']} (Type: '+go {direction}')")

        elif command == "+go":
            if not argument:
                print("Go where? (Ex: '+go kitchen')")
            else:
                current_room_data = rooms[player.current_room]
                
                is_forward = argument in ["forward", "dining", "lab", "chamber", "food lab", "dining hall", "efe's chamber"]
                
                if is_forward and current_room_data["locked"]:
                    printSlow("THE DOOR IS LOCKED! You must solve the puzzle first.")
                    if player.current_room == "ROOM3": 
                        print("Hint: Solve the anagram on the door (+answer [text]).")
                    if player.current_room == "ROOM5": 
                        print("Hint: Think about Dennis Villenevue and Incendies please (+answer [number]).")
                    continue

                if argument in current_room_data["name"].lower():
                    print("You are already there!")
                
                elif argument in current_room_data["exits"]:
                    target_id = current_room_data["exits"][argument]
                    player.current_room = target_id
                    target_room = rooms[target_id]
                    
                    textSeperator()
                    printSlow(f"--- {target_room['name']} ---")
                    printSlow(target_room["description"])
                    
                    if not target_room["cleared"]:
                        if target_id == "ROOM6":
                            enemies = [Enemy("THE PRIME RIB", 200, 15)] 
                            printSlow("\nROAAAAAR! The Beast of Gluttony appears!")
                        else:
                            num_enemies = random.randint(1, 2)
                            enemy_types = [
                                {"name": "Rotten Tomato", "hp": 50, "dmg": 8},   
                                {"name": "Stale Bread", "hp": 60, "dmg": 10},   
                                {"name": "Lettuce Shooter", "hp": 40, "dmg": 12}, 
                                {"name": "Moldy Cheese", "hp": 60, "dmg": 7},    
                                {"name": "Raw Meat Slab", "hp": 80, "dmg": 9}   
                            ]
                            enemies = []
                            enemy_names = []
                            for i in range(num_enemies):
                                etype = random.choice(enemy_types)
                                enemies.append(Enemy(etype["name"], etype["hp"], etype["dmg"]))
                                enemy_names.append(etype["name"])
                            printSlow(f"\nEnemies appeared: {', '.join(enemy_names)}!")
                        
                        printSlow("Get ready for battle!")
                        time.sleep(1)
                        
                        combat_loop(player, enemies)
                        
                        printSlow(f"\nBattle ended. Status: HP {player.hp}/{player.max_hp}")
                        target_room["cleared"] = True 
                        
                        if target_id == "ROOM2":
                            textSeperator()
                            printSlow("With the kitchen safe, you notice a recipe pinned to the wall!")
                            printSlow(">> RECIPE UNLOCKED: Meat + Bread = Patties")
                            textSeperator()
                            
                        elif target_id == "ROOM4":
                            textSeperator()
                            printSlow("The enemies damaged the computer, but the screensaver is still visible!")
                            printSlow(">> RECIPE UNLOCKED: Patties + Lettuce + Tomato = ABSOLUTE BURGER")
                            textSeperator()
     
                        if target_id == "ROOM6":
                            textSeperator()
                            printSlow("With a final roar, The Prime Rib explodes into ingredients!")
                            printSlow("LOOT RAIN! You gathered everything needed for the final recipe:")
                            
                            final_ingredients = ["meat", "bread", "lettuce", "tomato"]
                            
                            for ing in final_ingredients:
                                if ing in player.inventory:
                                    player.inventory[ing] += 99
                                else:
                                    player.inventory[ing] = 99
                                printSlow(f"-> Acquired: {ing.upper()}")
                            
                            printSlow("\nNow you have everything!")
                            printSlow("1. Type '+craft' to make Patties (Meat+Bread)")
                            printSlow("2. Type '+craft' again to make ABSOLUTE BURGER (Patties+Lettuce+Tomato)")
                            textSeperator()

                    textSeperator()
                else:
                    print("You can't go that way.")
        
        elif command == "+search":
            if player.current_room == "ROOM4":
                printSlow("You see a mysterious computer terminal on the desk.")
                printSlow("Maybe you should try to '+use computer'?")
            else:
                print("You found nothing of interest.")
        
        elif command == "+use":
            if argument == "computer" and player.current_room == "ROOM4":
                printSlow("You start hacking the terminal...")
                time.sleep(1)
                create_secret_file()
                printSlow(">> SYSTEM ALERT: A secret file has been downloaded to your game folder!")
                printSlow(">> HINT: Check your game files to find the password.")
            
            elif argument and argument in player.inventory:
                player.inventory[argument] -= 1
                if player.inventory[argument] == 0: 
                    del player.inventory[argument]
                
                if "bread" in argument:
                    player.max_hp += 10
                    player.hp = player.max_hp
                    printSlow(f"Ate Bread. Max HP increased to {player.max_hp} (Permanent).")
                
                elif "tomato" in argument:
                    player.attack += 2
                    printSlow(f"Ate Tomato. Attack increased to {player.attack} (Permanent).")
                
                elif "meat" in argument:
                    player.attack += 5
                    printSlow(f"Ate Meat. You feel strong! Attack increased to {player.attack} (Permanent).")
                
                elif "lettuce" in argument:
                    player.defense += 1
                    printSlow(f"Ate Lettuce. Defense increased to {player.defense} (Permanent).")
                
                elif "cheese" in argument:
                    player.defense += 2
                    printSlow(f"Ate Cheese. Defense increased to {player.defense} (Permanent).")
                
                else:
                    print("You ate it, but nothing happened.")
            else:
                print("You don't have that item or can't use it here.")

        elif command == "+answer":
            if player.current_room == "ROOM3":
                if argument == "are you hungry":
                    printSlow("CORRECT! The lock clicks open.")
                    rooms["ROOM3"]["locked"] = False
                else:
                    print("Wrong answer. The door remains locked.")
            
            elif player.current_room == "ROOM5":
                if argument == "1":
                    printSlow("ACCESS GRANTED! The steel door slides open.")
                    rooms["ROOM5"]["locked"] = False
                else:
                    print("BEEP! Incorrect answer. Try again.")

        elif command == "+recipes":
            textSeperator()
            print("--- COOKBOOK ---")
            
            print("1. HAMBURGER PATTIES")
            print("   Ingredients: Meat + Bread")
            print("   Effect: Essential ingredient for the final burger.")
            print("-" * 20)
            
            print("2. THE ABSOLUTE BURGER")
            print("   Ingredients: Patties + Lettuce + Tomato")
            print("   Effect: The only way to save Selman Hoca (WIN GAME).")
            print("-" * 20)
            
            print("Type '+craft' when you have enough ingredients.")
            textSeperator()
        
        elif command == "+craft":
            if "meat" in player.inventory and "bread" in player.inventory:
                player.inventory["meat"] -= 1
                player.inventory["bread"] -= 1
                if player.inventory["meat"] <= 0: del player.inventory["meat"]
                if player.inventory["bread"] <= 0: del player.inventory["bread"]
                
                if "patties" in player.inventory: player.inventory["patties"] += 1
                else: player.inventory["patties"] = 1
                
                printSlow("You crafted: HAMBURGER PATTIES!")
            
            elif "patties" in player.inventory and "lettuce" in player.inventory and "tomato" in player.inventory:
                printSlow("Mixing ingredients...")
                time.sleep(1)
                printSlow("You crafted: THE ABSOLUTE BURGER!")
                player.inventory["absolute burger"] = 1
                
                if player.current_room == "ROOM6":
                    textSeperator()
                    printSlow("Selman Hoca sees the burger. Use '+feed' to save him or '+eat' to betray him.")
            else:
                print("You don't have enough ingredients. (Need Meat+Bread -> Patties, then Patties+Lettuce+Tomato)")

        elif command == "+feed":
            if "absolute burger" in player.inventory and player.current_room == "ROOM6":
                textSeperator()
                printSlow("You feed Selman Hoca. He takes a bite...")
                printSlow("His eyes widen. 'This... this is the taste of Freedom!'")
                printSlow("The tyranny ends. Everyone gets 'AA'.")
                printSlow("\n--- GOOD ENDING: THE SAVIOR ---")
                break
            else:
                print("You can't do that yet.")

        elif command == "+eat":
            if "absolute burger" in player.inventory and player.current_room == "ROOM6":
                textSeperator()
                printSlow("You look at the burger. You are hungry too...")
                printSlow("You eat it in one bite. Selman Hoca screams in despair.")
                printSlow("You become the new Food Lord. The dark age continues for humanity...")
                printSlow("\n--- BAD ENDING: THE GLUTTON ---")
                break
            else:
                print("You can't do that yet.")
        
        elif command == "+enter":
            if player.current_room == "ROOM4":
                if not argument:
                    print("Enter what? (Ex: '+enter 1234')")
                elif argument == "ketchup":
                    printSlow("ACCESS GRANTED! The door to the Dark Corridor opens.")
                    rooms["ROOM4"]["exits"]["forward"] = "ROOM5"
                    rooms["ROOM4"]["exits"]["corridor"] = "ROOM5"
                    printSlow("(New path unlocked: Dark Corridor)")
                else:
                    print("ACCESS DENIED. Wrong password.")
            else:
                print("There is nothing to enter a password into here.")
        elif command == "+answer":
            if not argument:
                print("Answer what? (Ex: '+answer [number]')")
            
            elif player.current_room == "ROOM3":
                if argument == "are you hungry":
                    printSlow("CORRECT! The lock clicks open.")
                    rooms["ROOM3"]["locked"] = False
                else:
                    print("Wrong answer. The door remains locked.")
            
            elif player.current_room == "ROOM5":
                if argument == "1":
                    printSlow("CORRECT! The steel door opens.")
                    rooms["ROOM5"]["locked"] = False
                else:
                    print("Access Denied. Incorrect answer.")
            else:
                print("There is no puzzle here.")

        elif command == "+craft":
            if "meat" in player.inventory and "bread" in player.inventory:
                player.inventory["meat"] -= 1
                player.inventory["bread"] -= 1
                if player.inventory["meat"] <= 0: del player.inventory["meat"]
                if player.inventory["bread"] <= 0: del player.inventory["bread"]
                
                if "patties" in player.inventory: player.inventory["patties"] += 1
                else: player.inventory["patties"] = 1
                
                printSlow("You mixed Meat and Bread... Crafted: HAMBURGER PATTIES!")
            
            elif "patties" in player.inventory and "lettuce" in player.inventory and "tomato" in player.inventory:
                player.inventory["patties"] -= 1
                player.inventory["lettuce"] -= 1
                player.inventory["tomato"] -= 1
                if player.inventory["patties"] <= 0: del player.inventory["patties"]
                if player.inventory["lettuce"] <= 0: del player.inventory["lettuce"]
                if player.inventory["tomato"] <= 0: del player.inventory["tomato"]

                printSlow("Mixing the legendary ingredients...")
                time.sleep(1)
                printSlow("You crafted: THE ABSOLUTE BURGER!")
                player.inventory["absolute burger"] = 1
                
                if player.current_room == "ROOM6":
                    textSeperator()
                    printSlow("Selman Hoca smells the burger. His eyes open wide.")
                    printSlow("DECISION TIME: Type '+feed' to save him OR '+eat' to betray him.")
            else:
                print("You don't have the right ingredients.")
                print("Recipe 1: Meat + Bread = Patties")
                print("Recipe 2: Patties + Lettuce + Tomato = Absolute Burger")

        elif command == "+feed":
            if "absolute burger" in player.inventory and player.current_room == "ROOM6":
                textSeperator()
                printSlow("You give the burger to Selman Hoca.")
                printSlow("He takes a bite... Tears of joy run down his face.")
                printSlow("'My memory... It's back! The recipe was inside us all along.'")
                printSlow("Peace is restored. Everyone gets an 'AA'.")
                printSlow("\n--- GOOD ENDING: THE SAVIOR ---")
                break
            else:
                print("You can't do that yet.")

        elif command == "+eat":
            if "absolute burger" in player.inventory and player.current_room == "ROOM6":
                textSeperator()
                printSlow("You're starving...")
                printSlow("You look at the burger. God dammit, it looks awsome!")
                printSlow("You eat it in one giant bite. Selman Hoca screams in despair.")
                printSlow("Power surges through you! You are the new Food Tyrant.")
                printSlow("\n--- BAD ENDING: THE GLUTTON ---")
                break
            else:
                print("You can't do that yet.")
        
        else:
            print("I don't understand that command.")


try:
    mainGameLoop()
except KeyboardInterrupt:
    print("\nForce close.")