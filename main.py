import json


# Define the Knight class
class Knight:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.attack = 1
        self.defense = 1
        self.status = "LIVE"
        self.item = None

    def equip_item(self, item):
        self.item = item
        self.attack += item.attack
        self.defense += item.defense

    def drop_item(self):
        if self.item:
            self.attack -= self.item.attack
            self.defense -= self.item.defense
            dropped_item = self.item
            self.item = None
            return dropped_item
        return None

    def move(self, direction):
        if self.status != "LIVE":
            return
        x, y = self.position
        if direction == 'N':
            x -= 1
        elif direction == 'S':
            x += 1
        elif direction == 'E':
            y += 1
        elif direction == 'W':
            y -= 1

        # Check if the knight drowns (moves off the board)
        if x < 0 or x > 7 or y < 0 or y > 7:
            self.status = "DROWNED"
            self.position = None
            self.attack = 0  # Reset attack to 0 when drowned
            self.defense = 0  # Reset defense to 0 when drowned
        else:
            self.position = (x, y)



# Define the Item class
class Item:
    def __init__(self, name, position, attack=0, defense=0):
        self.name = name
        self.position = position
        self.attack = attack
        self.defense = defense
        self.equipped = False


# Initialize the knights and items
knights = {
    'R': Knight('red', (0, 0)),
    'B': Knight('blue', (7, 0)),
    'G': Knight('green', (7, 7)),
    'Y': Knight('yellow', (0, 7))
}

items = {
    'A': Item('axe', (2, 2), attack=2),
    'D': Item('dagger', (2, 5), attack=1),
    'M': Item('magic_staff', (5, 2), attack=1, defense=1),
    'H': Item('helmet', (5, 5), defense=1)
}


# Update the board and manage items, fights
def update_board(knight_symbol):
    knight = knights[knight_symbol]
    if knight.status != "LIVE":
        return

    x, y = knight.position
    # Check for items
    for item_key, item in items.items():
        if item.position == knight.position and not item.equipped:
            knight.equip_item(item)
            item.equipped = True
            break
    # Handle fights
    handle_fight(knight_symbol)


# Handle fights between knights on the same tile
def handle_fight(knight_symbol):
    knight = knights[knight_symbol]
    for other_knight_symbol, other_knight in knights.items():
        if other_knight != knight and other_knight.position == knight.position and other_knight.status == "LIVE":
            if knight.attack + 0.5 > other_knight.defense:
                other_knight.status = "DEAD"
                dropped_item = other_knight.drop_item()
                if dropped_item:
                    items[dropped_item.name].position = other_knight.position
            else:
                knight.status = "DEAD"
                dropped_item = knight.drop_item()
                if dropped_item:
                    items[dropped_item.name].position = knight.position


# Apply moves based on the moves.txt file
def apply_moves(moves_file):
    with open(moves_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line == "GAME-START" or line == "GAME-END":
            continue
        knight, direction = line.split(':')
        knights[knight].move(direction)
        update_board(knight)


# Save the final state of the board to a JSON file
def save_final_state(output_file):
    state = {}
    for knight_key, knight in knights.items():
        state[knight.color] = [
            knight.position,
            knight.status,
            knight.item.name if knight.item else None,
            knight.attack,
            knight.defense
        ]

    for item_key, item in items.items():
        state[item.name] = [item.position, item.equipped]

    with open(output_file, 'w') as f:
        json.dump(state, f, indent=4)


# Main code to run the game
if __name__ == "__main__":
    apply_moves('moves.txt')
    save_final_state('final_state.json')
