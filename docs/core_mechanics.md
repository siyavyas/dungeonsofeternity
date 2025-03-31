### Game Design Document for Dungeons of Eternity

#### 1. Introduction
Dungeons of Eternity is a tactical card-based dungeon crawler that combines strategic deck building, resource management, and engaging combat mechanics. Players will traverse procedurally generated dungeons, battling enemies and collecting resources to improve their decks and character abilities.

---

#### 2. Core Gameplay Mechanics

##### 2.1 Card System Mechanics and Deck Building Rules
- **Card Types**: 
  - **Action Cards**: Represent abilities or attacks. They are divided into three categories:
    - **Attack Cards**: Deal damage to enemies.
    - **Defense Cards**: Provide shields or healing.
    - **Utility Cards**: Offer buffs, debuffs, or special effects.
  - **Item Cards**: Equipment or consumables that can enhance character abilities or provide one-time effects.
  - **Skill Cards**: Character-specific cards that unlock unique abilities as the player progresses.
  
- **Deck Building Rules**:
  - **Deck Size**: Each player can have a minimum of 20 cards and a maximum of 40 cards in their deck.
  - **Card Rarity**: Cards are categorized into common, rare, and legendary types, with legendary cards being limited to 2 copies per deck.
  - **Synergy**: Players are encouraged to build decks that have synergistic themes (e.g., fire-based, healing, etc.) to maximize effectiveness in combat.
  - **Card Acquisition**: Players acquire cards by defeating enemies, finding treasure chests, or purchasing them from in-game shops using resources.

---

##### 2.2 Movement and Combat Systems
- **Movement System**:
  - Players can move within a grid-based dungeon layout.
  - Each player has a movement range of 3 tiles per turn.
  - Players can interact with objects and NPCs within their movement range.
  
- **Combat System**:
  - **Initiative**: Combat is initiated based on the initiative value of characters and enemies. Higher initiative goes first.
  - **Turn Order**: Players and enemies take turns based on initiative; players can perform one action (move or play a card) per turn.
  - **Combat Resolution**: When a card is played, the damage or effect is calculated based on the card's attributes, any relevant modifiers, and the target's defenses.
  - **Status Effects**: Cards can inflict status effects (e.g., poison, stun) which can alter the flow of combat.

---

##### 2.3 Resource Management and Progression
- **Resources**:
  - **Gold**: Collected from defeated enemies and treasure chests, used to purchase cards and items.
  - **Mana**: Used to play cards; players start with a base mana of 3 and regenerate 1 mana per turn.
  - **Health Points (HP)**: Each character has a set HP that decreases when taking damage; if HP reaches 0, the character is knocked out.
  
- **Progression System**:
  - **Leveling Up**: Characters gain experience points (XP) from battles, which can be used to level up and improve stats (HP, Mana, Initiative).
  - **Skill Trees**: Players can unlock new abilities and passive effects by spending skill points earned upon leveling up.
  - **Card Upgrades**: Players can spend resources to upgrade cards, increasing their effectiveness or reducing their mana cost.

---

##### 2.4 Win/Lose Conditions and Game States
- **Win Conditions**:
  - Players win by defeating the final boss of a dungeon.
  - Completing specific objectives, such as rescuing NPCs or collecting artifacts, can also lead to victory.

- **Lose Conditions**:
  - If all player characters are reduced to 0 HP, the game is lost.
  - Players can also lose if they fail to complete specific objectives within a set number of turns.

- **Game States**:
  - **Exploration State**: Players navigate the dungeon, encountering enemies, events, and treasures.
  - **Combat State**: Activated when players engage with enemies, where turn-based actions take place.
  - **Shop State**: Players can buy and sell cards, items, and upgrades between dungeon levels.
  
---

#### 3. Conclusion
Dungeons of Eternity offers a rich blend of tactical gameplay involving strategic card mechanics, resource management, and a compelling progression system. The combination of deck building, movement, and combat systems creates an engaging experience that encourages players to adapt and optimize their strategies throughout the game. By balancing these core mechanics, Dungeons of Eternity aims to captivate players and provide a rewarding challenge as they delve deeper into its dungeons.