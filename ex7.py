###################
# Name: Ariel Mizrahi
# ID: 
# Assignment: ex7
###################

import csv

# Global BST root
owner_root = None
########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    while True:
        user_input = input(prompt).strip()
        # only true if the user enters -num or num
        if user_input.isdigit() or user_input.startswith('-') and user_input[1:].isdigit():
            return int(user_input)
        else:
            print("Invalid input.")

def get_poke_dict_by_id(poke_id):
    for pokemon in HOENN_DATA:
        if pokemon['ID'] == poke_id:
            return pokemon
    return None
    
def get_poke_dict_by_name(name):
    for pokemon in HOENN_DATA:
        if pokemon['Name'].lower() == name.lower():
            return pokemon
    return None

########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon):
    pokedex = []
    pokedex.append(first_pokemon)
    owner = {"Name":owner_name ,"Pokedex": pokedex,"Left": None , "Right": None }
    return owner

def insert_owner_bst(root, new_node):
    # declare
    global  owner_root 
    # if the owner tree is empty, give owner root the value of the new node
    if not owner_root:
        owner_root = new_node
        return owner_root
    # when we get to the wanted node after traversing the tree alphabeticlly
    if not root:
        return new_node
    # traversing the tree recursevly 
    if new_node['Name'].lower() < root['Name'].lower():
        root['Left'] = insert_owner_bst(root['Left'], new_node)
    else:
        root['Right'] = insert_owner_bst(root['Right'], new_node)
    return root

def find_owner_bst(root, owner_name):
    # if the owner tree is empty, return None
    if not root:
        return None
    # lower both string to ignore caps
    compare_name = root['Name'].lower()
    owner_name = owner_name.lower()
    # if we found the owner Node that contains the name
    if compare_name == owner_name:
        return root
    if compare_name < owner_name:
        return find_owner_bst(root['Right'], owner_name)
    if compare_name > owner_name:
        return find_owner_bst(root['Left'], owner_name)

def min_node(node):
    while (node['Left']):
        node = node['Left']
    return node

def delete_owner_bst(root, owner_name):
    # empty tree
    if not root:
        return None
     # traverse the tree alphabetically to find the node 
    if root['Name'].lower() > owner_name.lower():
        root['Left'] = delete_owner_bst(root['Left'], owner_name)
    elif root['Name'].lower() < owner_name.lower():
        root['Right'] = delete_owner_bst(root['Right'], owner_name)
    else:
        # No smaller children, switch with the right one
        if not root['Left']:
            return root['Right']
        # No bigger children, switch with the left one
        elif not root['Right']:
            return root['Left']
        else:
            # Find the smallest node on the right subtree
            temp = min_node(root['Right'])
            # Copy the successor's content to this node
            root['Name'] = temp['Name']
            root['Pokedex'] = temp['Pokedex']
            # Delete the successor
            root['Right'] = delete_owner_bst(root['Right'], temp['Name'])
    return root

########################
# 3) Pokedex Operations
########################

def check_if_pokemon_exist_by_id(pokedex, id):
    for pokemon in pokedex:
        if id == pokemon['ID']:
            return True
    return False

def check_if_pokemon_exist_by_name(pokedex, name):
    for pokemon in pokedex:
        if name.lower() == pokemon['Name'].lower():
            return True
    return False

def add_pokemon_to_owner(owner_node):
    chosen_id = read_int_safe("Enter Pokemon ID to add: ")
    # check if the id is legal
    if chosen_id < 1 or chosen_id > 135:
        print(f"ID {chosen_id} not found in Honen data.")
        return owner_node
    # check if the id exists
    if check_if_pokemon_exist_by_id(owner_node['Pokedex'], chosen_id):
        print("Pokemon already in the list. No changes made.")
        return owner_node
    # create the pokemon dic from the hoenn data list and append it to pokedex
    pokemon = HOENN_DATA[chosen_id-1]
    owner_node['Pokedex'].append(pokemon)
    print(f"Pokemon {pokemon['Name']} (ID {chosen_id}) added to {owner_node['Name']}'s Pokedex.")
    return owner_node

def release_pokemon_by_name(owner_node):
    name_to_release = input("Enter Pokemon Name to release: ")
    # check if the poke exist in the pokedex
    if not check_if_pokemon_exist_by_name(owner_node['Pokedex'], name_to_release):
        print(f"No Pokemon named '{name_to_release}' in {owner_node['Name']}'s Pokedex.")
    else:
        poke_to_release = get_poke_dict_by_name(name_to_release)
        owner_node['Pokedex'].remove(poke_to_release)
        print(f"Releasing {poke_to_release['Name']} from {owner_node['Name']}.")
    return owner_node

def evolve_pokemon_by_name(owner_node):
    # get name to evo
    name_to_evo = input("Enter Pokemon Name to evolve: ")
    # check if the poke exists in the owner pokedex
    if not check_if_pokemon_exist_by_name(owner_node['Pokedex'], name_to_evo):
        print(f"No Pokemon named '{name_to_evo}' in {owner_node['Name']}'s Pokedex.")
        return owner_node
    else:
        # get the complete pokemon from the hoenn pokedex with get poke dict by name
        poke_to_evo = get_poke_dict_by_name(name_to_evo)
        # if the poke cannot evolve exit
        if not poke_to_evo['Can Evolve']:
            print(f"{poke_to_evo['Name']} cannot evolve.")
            return owner_node
        if poke_to_evo['Can Evolve']:
            evolved_poke = get_poke_dict_by_id(poke_to_evo['ID'] + 1)
        # if the evolved poke already exists delete the poke to evo and exit
        if check_if_pokemon_exist_by_id(owner_node['Pokedex'], evolved_poke['ID']):
            print(f"Pokemon evolved from {poke_to_evo['Name']} (ID {poke_to_evo['ID']}) to {evolved_poke['Name']} (ID {evolved_poke['ID']}).")
            print(f"{evolved_poke['Name']} was already present; releasing it immediately.")
            owner_node['Pokedex'].remove(poke_to_evo)
            return owner_node
        # otherwise all conditions are met and we append the evo poke and remove the poke to evo
        owner_node['Pokedex'].remove(poke_to_evo)
        owner_node['Pokedex'].append(evolved_poke)
        print(f"Pokemon evolved from {poke_to_evo['Name']} (ID {poke_to_evo['ID']}) to {evolved_poke['Name']} (ID {evolved_poke['ID']}).")
        return owner_node

########################
# 4) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    # append to the list all of the roots recursevly
    if root is not None:
        arr.append(root)
        gather_all_owners(root['Left'], arr)
        gather_all_owners(root['Right'], arr)
    return arr

def sort_owners_by_num_pokemon(arr):
    # bublle sort the list by pokemon count (if count's are equal check alphabetically)
    for i in range (len(arr)):
        for j in range (len(arr)- i - 1):
            if len(arr[j]['Pokedex']) > len(arr[j+1]['Pokedex']):
                arr[j], arr[j+1] = arr[j+1], arr[j]
            if len(arr[j]['Pokedex']) == len(arr[j+1]['Pokedex']):
                if arr[j]['Name'].lower() > arr[j+1]['Name'].lower():
                    arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
    


########################
# 5) Print All
########################

def print_all_owners():
    print("""1) BFS
2) Pre-Order
3) In-Order
4) Post-Order""")
    choice = read_int_safe("Your choice: ")
    if choice == 1:
        bfs_print(owner_root)
    elif choice == 2:
        pre_order_print(owner_root)
    elif choice == 3:
        in_order_print(owner_root)
    elif choice == 4:
        post_order_print(owner_root)
    else:
        print("Invalid choice.")
        return
    
def bfs_print(root):
    """Perform BFS on a binary tree and print all node values."""
    # checks if the root is None
    if not root:
        return  
    # initialize the queue List
    queue = [root] 
    # run this loop until the queue is empty meaning we finished traversing the tree and printing everything 
    while queue:
        # pop the first node each time and print it
        current = queue.pop(0)  
        print(f"\nOwner: {current['Name']}")
        for pokemon in current['Pokedex']:
            print(f"ID: {pokemon['ID']},"
            f" Name: {pokemon['Name']},"
            f" Type: {pokemon['Type']},"
            f" HP: {pokemon['HP']},"
            f" Attack: {pokemon['Attack']},"
            f" Can Evolve: {pokemon['Can Evolve']}")  
        # append the left and right child if they exist
        if current['Left']:
            queue.append(current['Left'])
        if current['Right']:
            queue.append(current['Right'])

def pre_order_print(root):
    if not root:
        return
    print(f"\nOwner: {root['Name']}")
    for pokemon in root['Pokedex']:
        print(f"ID: {pokemon['ID']},"
        f" Name: {pokemon['Name']},"
        f" Type: {pokemon['Type']},"
        f" HP: {pokemon['HP']},"
        f" Attack: {pokemon['Attack']},"
        f" Can Evolve: {pokemon['Can Evolve']}")
    pre_order_print(root['Left'])
    pre_order_print(root['Right'])

def in_order_print(root):
    if not root:
        return
    in_order_print(root['Left'])
    print(f"\nOwner: {root['Name']}")
    for pokemon in root['Pokedex']:
        print(f"ID: {pokemon['ID']},"
        f" Name: {pokemon['Name']},"
        f" Type: {pokemon['Type']},"
        f" HP: {pokemon['HP']},"
        f" Attack: {pokemon['Attack']},"
        f" Can Evolve: {pokemon['Can Evolve']}")
    in_order_print(root['Right'])

def post_order_print(root):
    if not root:
        return
    post_order_print(root['Left'])
    post_order_print(root['Right'])
    print(f"\nOwner: {root['Name']}")
    for pokemon in root['Pokedex']:
        print(f"ID: {pokemon['ID']},"
        f" Name: {pokemon['Name']},"
        f" Type: {pokemon['Type']},"
        f" HP: {pokemon['HP']},"
        f" Attack: {pokemon['Attack']},"
        f" Can Evolve: {pokemon['Can Evolve']}")
    


########################
# 6) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    choice = 1
    while choice != 7:
        print("""
-- Display Filter Menu --
1. Only a certain Type
2. Only Evolvable
3. Only Attack above __
4. Only HP above __
5. Only names starting with letter(s)
6. All of them!
7. Back""")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            # print by type
            poke_type = input("Which Type? (e.g. GRASS, WATER): ").strip().lower()
            is_printed = False
            for pokemon in owner_node['Pokedex']:
                check_type = pokemon['Type'].lower()
                if check_type == poke_type:
                    is_printed = True
                    print(f"ID: {pokemon['ID']},"
                      f" Name: {pokemon['Name']},"
                      f" Type: {pokemon['Type']},"
                      f" HP: {pokemon['HP']},"
                      f" Attack: {pokemon['Attack']},"
                      f" Can Evolve: {pokemon['Can Evolve']}")
            if not is_printed:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 2:
            # only evolvable
            is_printed = False
            for pokemon in owner_node['Pokedex']:
                if  pokemon['Can Evolve'] == "TRUE":
                    is_printed = True
                    print(f"ID: {pokemon['ID']},"
                      f" Name: {pokemon['Name']},"
                      f" Type: {pokemon['Type']},"
                      f" HP: {pokemon['HP']},"
                      f" Attack: {pokemon['Attack']},"
                      f" Can Evolve: {pokemon['Can Evolve']}")
            if not is_printed:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 3:
            # print by attack
            attack_threshold = read_int_safe("Enter Attack threshold: ")
            is_printed = False
            for pokemon in owner_node['Pokedex']:
                if pokemon['Attack'] > attack_threshold:
                    is_printed = True
                    print(f"ID: {pokemon['ID']},"
                      f" Name: {pokemon['Name']},"
                      f" Type: {pokemon['Type']},"
                      f" HP: {pokemon['HP']},"
                      f" Attack: {pokemon['Attack']},"
                      f" Can Evolve: {pokemon['Can Evolve']}")
            if not is_printed:
                print("There are no Pokemons in this Pokedex that match the criteria.")
        elif choice == 4:
            # print by HP
            HP_threshold = read_int_safe("Enter HP threshold: ")
            is_printed = False
            for pokemon in owner_node['Pokedex']:
                if pokemon['HP'] > HP_threshold:
                    is_printed = True
                    print(f"ID: {pokemon['ID']},"
                      f" Name: {pokemon['Name']},"
                      f" Type: {pokemon['Type']},"
                      f" HP: {pokemon['HP']},"
                      f" Attack: {pokemon['Attack']},"
                      f" Can Evolve: {pokemon['Can Evolve']}")
            if not is_printed:
                print("There are no Pokemons in this Pokedex that match the criteria.")
            pass
        elif choice == 5:
            # print by first letter
            starting_letter = input("Starting letter(s): ").lower().strip()
            is_printed = False
            for pokemon in owner_node['Pokedex']:
                if pokemon['Name'].lower().startswith(starting_letter):
                    is_printed = True
                    print(f"ID: {pokemon['ID']},"
                      f" Name: {pokemon['Name']},"
                      f" Type: {pokemon['Type']},"
                      f" HP: {pokemon['HP']},"
                      f" Attack: {pokemon['Attack']},"
                      f" Can Evolve: {pokemon['Can Evolve']}")
            if not is_printed:
                print("There are no Pokemons in this Pokedex that match the criteria.") 
        elif choice == 6:
            #print all
             is_printed = False
             for pokemon in owner_node['Pokedex']:
                    is_printed = True
                    print(f"ID: {pokemon['ID']},"
                      f" Name: {pokemon['Name']},"
                      f" Type: {pokemon['Type']},"
                      f" HP: {pokemon['HP']},"
                      f" Attack: {pokemon['Attack']},"
                      f" Can Evolve: {pokemon['Can Evolve']}")
             if not is_printed:
                print("There are no Pokemons in this Pokedex that match the criteria.") 
            
        elif choice == 7:
            print("Back to Pokedex Menu.")
            return
        else: 
            print("Invalid choice.")


########################
# 7) Sub-menu & Main menu
########################

def existing_pokedex(owner_node):
    choice = 1
    while choice != 5:
        print(f"""
-- {owner_node['Name']}'s Pokedex Menu --
1. Add Pokemon
2. Display Pokedex
3. Release Pokemon
4. Evolve Pokemon
5. Back to Main """)
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            owner_node = add_pokemon_to_owner(owner_node)
        elif choice == 2:
            display_filter_sub_menu(owner_node)
        elif choice == 3:
            owner_node = release_pokemon_by_name(owner_node)
        elif choice == 4:
            owner_node = evolve_pokemon_by_name(owner_node)
        elif choice == 5:
            print("Back to Main Menu.")
            return
        else: 
            print("Invalid choice.")
    
def main_menu():
   print("""
=== Main Menu ===
1. New Pokedex
2. Existing Pokedex
3. Delete a Pokedex
4. Display owners by number of Pokemon
5. Print All
6. Exit""")

def main():
    # decalre owner_root global so it can be used
    global owner_root
    choice = 1
    while choice != 6:
        main_menu()
        choice = read_int_safe("Your choice: ")
        # new pokedex
        if choice == 1:
            owner_name = input("Owner name: ").strip()
            # check if the owner name already exists
            if find_owner_bst(owner_root, owner_name):
                print(f"Owner '{owner_name}' already exists. No new Pokedex created.")
            else:
                print("""Choose your starter Pokemon:
1) Treecko
2) Torchic
3) Mudkip""")
                # create the starter pokemon dict for the new owner by getting data from heonn pokedex
                start_pokemon_id = read_int_safe("Your choice: ")
                if start_pokemon_id not in (1, 2, 3):
                    print("Invalid. No new Pokedex created.")
                else:
                    start_pokemon_id = start_pokemon_id - 1
                    #Treecko
                    if start_pokemon_id == 0:
                        starter = HOENN_DATA[0]
                    #Torchic
                    elif start_pokemon_id == 1:
                        starter = HOENN_DATA[3]
                    #Mudkip
                    elif start_pokemon_id == 2:
                        starter = HOENN_DATA[6]
                    # create and insert the node
                    new_node = create_owner_node(owner_name, starter)
                    owner_root = insert_owner_bst(owner_root, new_node)
                    print(f"New Pokedex created for {owner_name} with starter {starter['Name']}.")
        # existing pokedex
        elif choice == 2:
            owner_name = input("Owner name: ")
            # check if the owner name exist if so enter the existing pokedex(sub menu) with the wanted owner
            if not find_owner_bst(owner_root, owner_name):
                print(f"Owner '{owner_name}' not found.")
            else:
                existing_pokedex(find_owner_bst(owner_root, owner_name))
        # delete owner
        elif choice == 3:
            # check if there is at least 1 owner
            if not owner_root:
                print("No owner to delete.")
            else:
                owner_to_delete = input("Enter owner to delete: ")
                # check if the owner exists
                if not find_owner_bst(owner_root, owner_to_delete):
                     print(f"Owner '{owner_to_delete}' not found.")
                else:
                    # if found, delete the owner
                    owner_root = delete_owner_bst(owner_root, owner_to_delete)
                    print(f"Deleting {owner_to_delete}'s entire Pokedex...")
                    print("Pokedex deleted.")
        # display owners by number of Pokemon
        elif choice == 4:
            # check if there is at least 1 owner
            if not owner_root:
                print("No owners at all.")
            else:
                print("=== The Owners we have, sorted by number of Pokemons ===")
                # create a list, gather from the owner tree all the owners, sort them as requested and print each one
                owner_array= []
                owner_array = gather_all_owners(owner_root, owner_array)
                owner_array = sort_owners_by_num_pokemon(owner_array)
                for owner in owner_array:
                    print(f"Owner: {owner['Name']} (has {len(owner['Pokedex'])} Pokemon)")
        # print all owner
        elif choice == 5:
            # check if there is at least 1 owner
            if not owner_root:
                print("No owners in the BST.")
                return
            # call print all owner(sub menu)
            print_all_owners()
        elif choice == 6:
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
