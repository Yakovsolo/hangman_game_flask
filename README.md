# Hangman Game App

Hangman Game App is a classic word-guessing game where players try to guess a hidden word by suggesting letters within a limited number of tries. This repository contains a web-based implementation of the Hangman game with user registration, leaderboards, multiple difficulty modes, and user account summaries.

![Play](/app/static/play.png "Homepage")

## Getting Started

Follow these instructions to set up and run the Hangman Game App on your local machine.

### Prerequisites

- Python 3.10 or higher
- Docker
- Git

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/vmatevicius/Hangman.git
cd Hangman
```
 
2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/Scripts/activate
```
3. Install the required packages:

```bash
pip install -r requirements.txt
```

### Running the App

1. Type this code in terminal

```bash
python run.py
```

### Dockerization

1. Build Docker containers:

```bash
docker compose build --no-cache
```

2. Run containers:

```bash
docker compose up
```

# Features

- ### User registration and login functionality

#### Login example

![Login](/app/static/gifs/login.gif "Login")

#### Registration example

![Registration](/app/static/gifs/registration.gif "Registration")

- ### Leaderboards displaying the top scores

#### Leaderboards example

![Leaderboards](/app/static/gifs/leaderboards.gif "Leaderboards")

- ### Three difficulty modes: easy, medium, and hard

#### Difficulties example

![Difficulties](/app/static/difficulties.png "Difficulties")

- ### Score system based on difficulty: easy (10 points), medium (20 points), hard (30 points)

- ### User account summary with statistics on games played, games won/lost, correct/wrong guesses

#### Summary example

![Summary](/app/static/gifs/account.gif "Summary")

- ### Letter reveal tickets

- ### Credit currency

- ### Ability to reveal letters using tickets

- ### Gambling

#### Gambling example

![Gambling](/app/static/gifs/gambling.gif "Gambling")

- ### Shop where you can buy tickets

#### Shop example

![Shop](/app/static/gifs/shop.gif "Shop")

### How to Play

#### Gameplay example

![victory](/app/static/gifs/victory.gif "victory")

### How to Start

0. Go to http://{your local host}:5000/

1. Register or log in to your account.

2. Choose a difficulty mode (easy, medium, or hard).

3. Guess letters to reveal the hidden word.

4. Each incorrect guess reduces the remaining tries by 1.

5. Win the game by guessing the entire word within the allotted number of tries.

6. Your score is based on the difficulty level and the number of remaining tries.