```csharp
// Dungeons of Eternity Core Systems

using System;
using System.Collections.Generic;

// Enum for Card Types
public enum CardType
{
    Action,
    Item,
    Event
}

// Enum for Card Rarity
public enum CardRarity
{
    Common,
    Uncommon,
    Rare,
    Legendary
}

// Card class representing a card in the game
public class Card
{
    public string Name { get; }
    public CardType Type { get; }
    public CardRarity Rarity { get; }
    public int Cost { get; }
    public string EffectDescription { get; }

    public Card(string name, CardType type, CardRarity rarity, int cost, string effectDescription)
    {
        Name = name;
        Type = type;
        Rarity = rarity;
        Cost = cost;
        EffectDescription = effectDescription;
    }
}

// Deck class for card management
public class Deck
{
    private List<Card> cards;
    private const int MaxDeckSize = 30;

    public Deck()
    {
        cards = new List<Card>();
    }

    public void AddCard(Card card)
    {
        if (cards.Count < MaxDeckSize)
        {
            cards.Add(card);
        }
        else
        {
            throw new InvalidOperationException("Deck size limit reached.");
        }
    }

    public void RemoveCard(Card card)
    {
        cards.Remove(card);
    }

    public List<Card> GetCards()
    {
        return cards;
    }
}

// Player class for managing player state
public class Player
{
    public int Health { get; private set; }
    public int ActionPoints { get; private set; }
    public Deck PlayerDeck { get; }
    
    public Player(int health, int actionPoints)
    {
        Health = health;
        ActionPoints = actionPoints;
        PlayerDeck = new Deck();
    }

    public void TakeDamage(int damage)
    {
        Health -= damage;
        if (Health <= 0)
        {
            // Handle player defeat
            Console.WriteLine("Player has been defeated!");
        }
    }

    public void RestoreHealth(int amount)
    {
        Health += amount;
    }

    public void SpendActionPoints(int amount)
    {
        ActionPoints -= amount;
    }
}

// GameState enum for different game states
public enum GameState
{
    Exploration,
    Combat,
    Shop
}

// Main Game class to manage game flow
public class Game
{
    public GameState CurrentState { get; private set; }
    public Player CurrentPlayer { get; private set; }

    public Game()
    {
        CurrentState = GameState.Exploration;
        CurrentPlayer = new Player(100, 5); // Starting health and action points
    }

    public void ChangeState(GameState newState)
    {
        CurrentState = newState;
        Console.WriteLine($"Game state changed to: {CurrentState}");
    }

    public void SaveGame(string filePath)
    {
        // Save game state to file (pseudo-code)
        // Serialize CurrentPlayer and CurrentState
        Console.WriteLine("Game saved.");
    }

    public void LoadGame(string filePath)
    {
        // Load game state from file (pseudo-code)
        // Deserialize and set CurrentPlayer and CurrentState
        Console.WriteLine("Game loaded.");
    }

    public void StartCombat()
    {
        ChangeState(GameState.Combat);
        // Initialize combat mechanics
    }

    public void EndCombat()
    {
        ChangeState(GameState.Exploration);
        // Handle post-combat logic
    }
}

// Example Usage
public class Program
{
    public static void Main(string[] args)
    {
        Game game = new Game();
        game.CurrentPlayer.PlayerDeck.AddCard(new Card("Fireball", CardType.Action, CardRarity.Rare, 3, "Deal 10 damage to an enemy."));
        game.CurrentPlayer.PlayerDeck.AddCard(new Card("Health Potion", CardType.Item, CardRarity.Common, 1, "Restore 5 health."));
        
        game.StartCombat(); // Transition to combat state
        game.CurrentPlayer.SpendActionPoints(3); // Spend action points for an action
        game.CurrentPlayer.TakeDamage(20); // Example of taking damage
        game.SaveGame("savefile.dat"); // Save the game
    }
}
```

### Documentation:
- **Card Class**: Represents the different types of cards available, including their properties such as name, type, rarity, cost, and effects.
- **Deck Class**: Manages the player's deck, allowing for adding and removing cards, while enforcing the maximum deck size limit.
- **Player Class**: Represents the player's state, including health, action points, and their deck. Provides methods for health management and action points usage.
- **Game Class**: Manages the overall game state, transitions between exploration, combat, and shop modes, and includes save/load functionality.
- **GameState Enum**: Represents different states the game can be in, facilitating state management and flow control.

This implementation provides a solid foundation for the core game systems in Dungeons of Eternity, ensuring maintainability and scalability as new features are added.