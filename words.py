import random

CATEGORIES = {
    "Weapons": ["LONGSWORD", "CROSSBOW", "HALBERD", "DAGGER", "MACE", "WARHAMMER", "SPEAR", "TREBUCHET", "BALLISTA"],
    "Creatures": ["DRAGON", "GOBLIN", "WEREWOLF", "VAMPIRE", "GRIFFIN", "TROLL", "WYVERN", "BASILISK", "GHOUL", "WRAITH"],
    "Places": ["DUNGEON", "CASTLE", "TAVERN", "FOREST", "VILLAGE", "CITADEL", "CRYPT", "GRAVEYARD", "FORTRESS"],
    "Magic": ["NECROMANCY", "PYROMANCY", "ILLUSION", "ENCHANTMENT", "RUNE", "SCROLL", "ALCHEMY", "SORCERY", "WARLOCK"]
}

def get_random_word():
    category = random.choice(list(CATEGORIES.keys()))
    word = random.choice(CATEGORIES[category])
    return word, category
