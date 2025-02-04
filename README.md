# AI-Adventures
 
This project is an AI-powered text adventure game generator that creates immersive and dynamic storytelling experiences.

## Setup

1. Clone the repository:
    git clone https://github.com/OchOchs/AI-Adventures.git
    cd text-adventure-game-generator

2. Create a virtual environment (optional but recommended):
    python -m venv .venv
    . .venv/bin/activate # On Windows use venv\Scripts\activate

3. Install the required packages:
    pip install -r requirements.txt

4. Set up your OpenAI API key and OpenAI Model:
- Create a `.env` file in the project root
- Add your API key: `OPENAI_API_KEY=your_api_key_here`
- Add your API model: `OPENAI_MODEL=gpt-4o-mini` # or any else gpt model

## Usage

1. Run Flask to start generating your text adventure in your localhost:
    flask run
2. Open your browser:
    `http://localhost:5000`

## About the Game

AI-Adventures is an AI-powered tool that creates unique, interactive storytelling experiences. This project combines the nostalgia of classic text-based adventures with the power of modern artificial intelligence to produce dynamic, ever-changing narratives.
Key features include:
- Procedurally Generated Worlds: 
    Each game creates a unique theme and setting, ensuring no two adventures are alike.
- Dynamic Character Creation: 
    The AI crafts complex protagonists with rich backstories and unique abilities.
- Adaptive Storytelling: 
    The narrative evolves based on player choices, creating a personalized adventure every time.
- Rich Descriptions: 
    Vivid, AI-generated text brings the game world to life, stimulating the player's imagination.
- Multiple Genres: 
    From fantasy realms to sci-fi worlds, the game can span various genres and settings.
- Challenging Puzzles and Decisions: 
    Players face intriguing challenges and moral dilemmas that shape their journey.
- Images For Visualization:
    There will be few images for a little visualization of what you are doing, but those won't influence the upcoming story.
Whether you're a fan of classic interactive fiction or looking for a new way to experience storytelling, AI-Adevntures offers endless possibilities for exploration and adventure.

## Potential Improvements

- Implement a save/load game feature to allow players to continue their adventures later
- Optimize response time by displaying decisions sequentially rather than all at once
- Integrate a simple combat system to add depth to character interactions
- Implement adventure length options, including the ability to set a defined endpoint
- Design a distinctive logo to enhance brand identity
- Expand platform compatibility beyond web applications
- Incorporate voice recording for user feedback and commands
- Develop multi-user persistence for collaborative storytelling experiences
- Add comprehensive type hints throughout the codebase to improve code readability
