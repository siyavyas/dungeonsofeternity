// Game State
let gameState = {
    player: {
        health: 100,
        mana: 100,
        hand: [],
        deck: []
    },
    enemy: {
        health: 100,
        hand: [],
        deck: []
    },
    board: [],
    currentTurn: 'player',
    gameStarted: false
};

// UI Elements
const menuButton = document.querySelector('.menu-button');
const menuPanel = document.querySelector('.menu-panel');
const instructionsButton = document.querySelector('#instructions-button');
const instructionsPanel = document.querySelector('.instructions-panel');
const restartButton = document.querySelector('#restart-button');
const closeMenuButton = document.querySelector('#close-menu');
const closeInstructionsButton = document.querySelector('#close-instructions');

// Event Listeners
menuButton.addEventListener('click', toggleMenu);
instructionsButton.addEventListener('click', toggleInstructions);
restartButton.addEventListener('click', restartGame);
closeMenuButton.addEventListener('click', toggleMenu);
closeInstructionsButton.addEventListener('click', toggleInstructions);

// Menu Functions
function toggleMenu() {
    menuPanel.classList.toggle('visible');
}

function toggleInstructions() {
    instructionsPanel.classList.toggle('visible');
    menuPanel.classList.remove('visible');
}

// Game Functions
function startGame() {
    if (!gameState.gameStarted) {
        initializeDecks();
        drawInitialHands();
        gameState.gameStarted = true;
        updateUI();
    }
}

function restartGame() {
    gameState = {
        player: {
            health: 100,
            mana: 100,
            hand: [],
            deck: []
        },
        enemy: {
            health: 100,
            hand: [],
            deck: []
        },
        board: [],
        currentTurn: 'player',
        gameStarted: false
    };
    updateUI();
    startGame();
}

function initializeDecks() {
    // Initialize player deck
    gameState.player.deck = [
        { id: 1, name: 'Attack', damage: 20, mana: 30, image: '/static/images/cards/attack.png' },
        { id: 2, name: 'Defend', defense: 15, mana: 20, image: '/static/images/cards/defend.png' },
        { id: 3, name: 'Heal', healing: 25, mana: 25, image: '/static/images/cards/heal.png' }
    ];
    
    // Initialize enemy deck
    gameState.enemy.deck = [
        { id: 4, name: 'Enemy Attack', damage: 15, mana: 25, image: '/static/images/cards/enemy_attack.png' },
        { id: 5, name: 'Enemy Defend', defense: 10, mana: 15, image: '/static/images/cards/enemy_defend.png' }
    ];
    
    // Shuffle decks
    shuffleDeck(gameState.player.deck);
    shuffleDeck(gameState.enemy.deck);
}

function shuffleDeck(deck) {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
    }
}

function drawInitialHands() {
    // Draw 5 cards for player
    for (let i = 0; i < 5; i++) {
        drawCard('player');
    }
    
    // Draw 3 cards for enemy
    for (let i = 0; i < 3; i++) {
        drawCard('enemy');
    }
}

function drawCard(player) {
    const deck = gameState[player].deck;
    if (deck.length > 0) {
        const card = deck.pop();
        gameState[player].hand.push(card);
        updateUI();
    }
}

function playCard(cardId, player) {
    const cardIndex = gameState[player].hand.findIndex(card => card.id === cardId);
    if (cardIndex !== -1) {
        const card = gameState[player].hand[cardIndex];
        
        // Check if player has enough mana
        if (player === 'player' && gameState.player.mana < card.mana) {
            alert('Not enough mana!');
            return;
        }
        
        // Remove card from hand
        gameState[player].hand.splice(cardIndex, 1);
        
        // Add card to board
        gameState.board.push({
            ...card,
            player: player
        });
        
        // Apply card effects
        applyCardEffects(card, player);
        
        // Update UI
        updateUI();
        
        // End turn if it's player's turn
        if (player === 'player') {
            endTurn();
        }
    }
}

function applyCardEffects(card, player) {
    if (card.damage) {
        const target = player === 'player' ? 'enemy' : 'player';
        gameState[target].health = Math.max(0, gameState[target].health - card.damage);
    }
    
    if (card.healing && player === 'player') {
        gameState.player.health = Math.min(100, gameState.player.health + card.healing);
    }
    
    if (player === 'player') {
        gameState.player.mana = Math.max(0, gameState.player.mana - card.mana);
    }
}

function endTurn() {
    gameState.currentTurn = gameState.currentTurn === 'player' ? 'enemy' : 'player';
    
    if (gameState.currentTurn === 'enemy') {
        // Enemy AI logic
        setTimeout(enemyTurn, 1000);
    } else {
        // Draw new cards
        drawCard('player');
        gameState.player.mana = Math.min(100, gameState.player.mana + 20);
        updateUI();
    }
}

function enemyTurn() {
    // Simple AI: Play first card if possible
    if (gameState.enemy.hand.length > 0) {
        const card = gameState.enemy.hand[0];
        playCard(card.id, 'enemy');
    }
    
    // Draw new card
    drawCard('enemy');
    
    // End enemy turn
    gameState.currentTurn = 'player';
    updateUI();
}

// UI Update Functions
function updateUI() {
    updateHealthBars();
    updateManaBar();
    updateHands();
    updateBoard();
    checkGameEnd();
}

function updateHealthBars() {
    document.querySelector('.player-stats .health-bar').textContent = `Health: ${gameState.player.health}`;
    document.querySelector('.enemy-stats .health-bar').textContent = `Health: ${gameState.enemy.health}`;
}

function updateManaBar() {
    document.querySelector('.player-stats .mana-bar').textContent = `Mana: ${gameState.player.mana}`;
}

function updateHands() {
    const playerHand = document.querySelector('.player-hand');
    const enemyHand = document.querySelector('.enemy-hand');
    
    // Clear hands
    playerHand.innerHTML = '';
    enemyHand.innerHTML = '';
    
    // Update player hand
    gameState.player.hand.forEach(card => {
        const cardElement = createCardElement(card, 'player');
        playerHand.appendChild(cardElement);
    });
    
    // Update enemy hand (face down)
    gameState.enemy.hand.forEach(card => {
        const cardElement = createCardElement(card, 'enemy', true);
        enemyHand.appendChild(cardElement);
    });
}

function createCardElement(card, player, faceDown = false) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'card';
    
    if (faceDown) {
        cardDiv.innerHTML = '<img src="/static/images/cards/face_down.png" alt="Face Down Card">';
    } else {
        cardDiv.innerHTML = `
            <img src="${card.image}" alt="${card.name}">
            <div class="card-info">
                <h3>${card.name}</h3>
                ${card.damage ? `<p>Damage: ${card.damage}</p>` : ''}
                ${card.healing ? `<p>Healing: ${card.healing}</p>` : ''}
                ${card.defense ? `<p>Defense: ${card.defense}</p>` : ''}
                ${card.mana ? `<p>Mana: ${card.mana}</p>` : ''}
            </div>
        `;
        
        if (player === 'player') {
            cardDiv.addEventListener('click', () => playCard(card.id, 'player'));
        }
    }
    
    return cardDiv;
}

function updateBoard() {
    const boardArea = document.querySelector('.board-area');
    boardArea.innerHTML = '';
    
    gameState.board.forEach(card => {
        const cardElement = createCardElement(card, card.player);
        boardArea.appendChild(cardElement);
    });
}

function checkGameEnd() {
    if (gameState.player.health <= 0) {
        alert('Game Over! You lost!');
        restartGame();
    } else if (gameState.enemy.health <= 0) {
        alert('Congratulations! You won!');
        restartGame();
    }
}

// Start the game when the page loads
window.addEventListener('load', startGame); 