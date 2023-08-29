# Hangman Game App

Hangman is originally a guessing game for two or more players. One player comes up with a word, phrase or sentence, and the other(s) tries to guess it by suggesting letters or numbers within a certain number of tries. Originally it was a paper and pencil game, but now you have the opportunity to play the electronic version of this exciting game. The role of the player who asks you the words will be performed by your computer.
This repository contains a web-based implementation of the Hangman game with user registration, leaderboards, multiple difficulty modes, and user account summaries.

![Title](/hangman/static/game/title.png "Title")

# Getting Started

Follow these instructions to set up and run the Hangman Game App on your local machine.

## Prerequisites

- Python 3.10 or higher
- Docker
- Git

## Installation

1. Clone the repository to your local machine:

```bash
git clone git@github.com:Yakovsolo/hangman_game_flask.git
cd hangman_game_flask
```
 
## Dockerization

1. Build Docker containers:

```bash
docker compose build 
```

2. Run containers:

```bash
docker compose up
```

## Aim of the Game:
To guess the hidden word by guessing one letter at a time. If the player guesses a correct letter, it is revealed in the word. If the letter is not part of the word, a part of the hangman figure is drawn.

## Rules
![Start](/hangman/static/game/rules/start_game.jpg "Start game")

1. The player chooses a category from the available options: "animals", "home", "jobs", "food", "clothes", "countries", "cities", "space", "mountains".

2. Based on the chosen category and difficulty, the program randomly selects a word within the specified letter range.

![Difficulty](/hangman/static/game/rules/difficulty.jpg "Difficulty")

3. Based on the chosen category and difficulty, the program randomly selects a word within the specified letter range.

![Gameplay](/hangman/static/game/rules/gameplay_first.jpg "Gameplay")

4. The player starts guessing letters by entering them one by one.

5. If the guessed letter is incorrect, a new part of the hangman figure is drawn (head, body, arms, legs, etc.).

![Wrong letter](/hangman/static/game/rules/wrong_letter.jpg "Wrong letter")

6. If a correct letter is guessed, it is revealed in the appropriate positions in the word.

![Correct letter](/hangman/static/game/rules/correct_letter.jpg "Correct letter")

7. The player continues guessing letters until they guess the entire word or the hangman figure is completely drawn.

8. The game ends when the player guesses the word or when the hangman figure is fully drawn. In case of loss, the correct word is revealed.

9. You can make a mistake in guessing the letter ten times. After ten mistakes, the gallows will be over and you will be hanged.

![Game win](/hangman/static/game/rules/game_win.jpg "Game win")

10. The player can play another game by selecting a new category and difficulty.


## How to Start

1. Go to http://{your local host}:8000/

2. Register or log in to your account.

3. Enjoy the game

# Good luck

