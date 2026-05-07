export const words = [
  "EXECUTION", "DUNGEON", "SORCERY", "MEDIEVAL", "GALLOWS",
  "GUILLOTINE", "VAMPIRE", "DRAGON", "WITCHCRAFT", "CASTLE",
  "PHANTOM", "GRAVEYARD", "BLOODLINE", "REVENGE", "SHADOW",
  "TORTURE", "NIGHTMARE", "NECROMANCER", "SKELETON", "ABYSS"
];

export const getWord = () => words[Math.floor(Math.random() * words.length)];
