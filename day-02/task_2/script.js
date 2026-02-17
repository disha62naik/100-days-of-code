// Select elements
const guessInput = document.getElementById("guessInput");
const guessBtn = document.getElementById("guessBtn");
const resetBtn = document.getElementById("resetBtn");
const feedback = document.getElementById("feedback");
const attemptsText = document.getElementById("attempts");
const gameCard = document.getElementById("gameCard");

// Game settings
const min = 1;
const max = 100;
const maxAttempts = 7;

// Game state
let secret = 0;
let remaining = maxAttempts;
let guesses = [];
let gameOver = false;

// Start game
function startGame() {
    secret = Math.floor(Math.random() * (max - min + 1)) + min;
    remaining = maxAttempts;
    guesses = [];
    gameOver = false;

    feedback.textContent = "";
    attemptsText.textContent = remaining;
    guessInput.value = "";
    guessInput.disabled = false;
    guessBtn.disabled = false;
    gameCard.classList.remove("bg-green-200");
}

// Handle Guess
function handleGuess() {

    if (gameOver) return;

    const value = Number(guessInput.value);

    // Validate input
    if (!Number.isInteger(value) || value < min || value > max) {
        feedback.textContent = "Please enter a valid number between 1 and 100.";
        return;
    }

    // Check repeated guess
    if (guesses.includes(value)) {
        feedback.textContent = "You already guessed this number!";
        return;
    }

    guesses.push(value);
    remaining--;
    attemptsText.textContent = remaining;

    // Check result
    if (value === secret) {
        feedback.textContent = "🎉 Correct! You Win!";
        gameCard.classList.add("bg-green-200");
        endGame();
        return;
    }

    if (remaining === 0) {
        feedback.textContent = `❌ Game Over! The number was ${secret}`;
        endGame();
        return;
    }

    feedback.textContent = value < secret ? "Too Low!" : "Too High!";
    guessInput.value = "";
}

// End Game
function endGame() {
    gameOver = true;
    guessInput.disabled = true;
    guessBtn.disabled = true;
}

// Event Listeners
guessBtn.addEventListener("click", handleGuess);

guessInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        handleGuess();
    }
});

resetBtn.addEventListener("click", startGame);

// Start first game
startGame();
