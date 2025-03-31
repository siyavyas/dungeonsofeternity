### Puzzle and Dungeon Generation Systems for Dungeons of Eternity

#### 1. Procedural Dungeon Generation Rules

To maintain player engagement and challenge, dungeons in Dungeons of Eternity will be procedurally generated using the following rules:

##### 1.1 Layout Generation
- **Grid System**: Dungeons are structured on a grid, typically 10x10 to 20x20 tiles.
- **Room Types**: Rooms will fall into several categories:
  - **Combat Rooms**: Contain enemies and are the primary source of XP and loot.
  - **Puzzle Rooms**: Feature puzzles that must be solved to progress.
  - **Treasure Rooms**: Contain chests with items or cards.
  - **Boss Rooms**: Final rooms that contain a powerful enemy.
- **Pathways**: Hallways connect rooms; they can be straight, L-shaped, or T-shaped, with a minimum of one path leading to the next room.

##### 1.2 Room and Path Generation
- **Randomized Room Placement**: Use noise functions (e.g., Perlin noise) to determine room placement and connectivity.
- **Weighted Randomization**: Combat rooms are more frequent, while boss rooms are rare, appearing only in specific floors or after certain conditions are met.
- **Secret Rooms**: A 10% chance for a room to be a secret room that provides additional rewards or lore.

##### 1.3 Environmental Features
- **Traps**: Randomly placed traps in hallways (e.g., spike pits, poison darts) to increase difficulty.
- **Environmental Hazards**: Certain rooms may have hazards (e.g., fire, ice) that affect player movement or card effects.
  
---

#### 2. Puzzle Mechanics and Difficulty Scaling

Puzzles will serve as a secondary challenge that complements combat. They will vary in complexity and type, adjusting difficulty based on the player's progress.

##### 2.1 Types of Puzzles
- **Logic Puzzles**: Players must deduce the correct sequence to unlock a door (e.g., matching colors or symbols).
- **Memory Games**: Players must remember a sequence of actions or card icons displayed briefly.
- **Environmental Puzzles**: Use objects in the environment to interact with mechanisms (e.g., pushing blocks to create a path).
- **Card-based Puzzles**: Require players to play specific cards in a certain order to solve (e.g., using a healing card to trigger a healing mechanism).

##### 2.2 Difficulty Scaling
- **Progressive Complexity**: As players advance, puzzles become more intricate, requiring more steps or combining different types of puzzles.
- **Hints**: Provide optional hints after a certain time has passed, with a penalty (e.g., losing health or resources).
- **Reward System**: Successful completion yields better rewards (e.g., rare cards or powerful items).

---

#### 3. Level Progression and Variety

##### 3.1 Dungeon Tiers
- **Tiered Dungeons**: Each dungeon will have tiers (e.g., Tier 1: Goblins, Tier 2: Undead, Tier 3: Demons), with increasing difficulty and variety in enemies, puzzles, and treasures.
- **Themed Dungeons**: Each tier will have a unique theme, such as a haunted castle for Tier 2, incorporating thematic puzzles and environmental aesthetics.

##### 3.2 Scaling Mechanics
- **Enemy Scaling**: Enemies will scale in health and damage based on the player's level and deck strength.
- **Card Acquisition**: Players will encounter card opportunities that match the theme of the current dungeon (e.g., fire-based cards in volcanic dungeons).
  
---

#### 4. Boss Room Designs

Boss rooms are critical for providing a climactic end to dungeon tiers. Their design will focus on unique mechanics and thematic elements.

##### 4.1 Boss Encounter Design
- **Unique Boss Mechanics**: Each boss will have specific abilities that require players to adapt their strategies (e.g., multi-phase fights where the boss changes abilities or weaknesses).
- **Arena Design**: Boss rooms will feature environmental hazards and dynamic elements (e.g., shifting walls, lava pools) that change the combat landscape.

##### 4.2 Boss Rewards
- **Legendary Cards**: Defeating a boss guarantees a legendary card or unique item.
- **Skill Points**: Players earn additional skill points for defeating bosses, which can be used for character upgrades.

##### 4.3 Visual and Thematic Elements
- **Art Style**: Each boss room will be visually distinct, with thematic decorations that reflect the boss's lore (e.g., dark, gothic for a vampire lord).
- **Sound Design**: Unique soundtracks and sound effects will enhance the atmosphere of boss encounters.

---

### Example Implementation

#### Dungeon Generation Example
- A Tier 1 dungeon begins with a layout of 12 rooms, 8 combat rooms, 2 puzzle rooms, and 1 treasure room.
- Rooms are connected via pathways, with traps placed randomly throughout the hallways to challenge players.

#### Puzzle Example
- A logic puzzle in a room requires players to solve a riddle based on symbols on the walls to unlock a door, where the answer changes with each playthrough.
  
#### Boss Room Example
- The final boss of Tier 1 is a Goblin King with high damage and the ability to summon minions. The arena has pitfalls that players must navigate while engaging in combat.

---

This structured approach to puzzle and dungeon generation aims to create a diverse, challenging, and engaging experience in Dungeons of Eternity, ensuring that players remain captivated as they explore and conquer each dungeon.