import json

from flask import Flask, render_template, jsonify, request
from llm_schemas import theme_schema, character_schema, ResponseSchema
from AITools import AITools

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="A!-Adv3ntur3s",
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
)
ai = AITools()
new_history = False

@app.route('/')
def main():
    global new_history
    new_history = True
    return render_template('home.html')

@app.route('/submit/<step>', methods=['POST'])
def submit(step):
    global new_history
    user_input = request.form.get('input')
    feedback = request.form.get('feedback')

    # Lade den Prompt aus einer JSON-Datei
    with open("./resources/prompts.json", "r") as file:
        prompts = json.load(file)
    with open("./resources/texts.json", "r") as file:
        texts = json.load(file)

    # Erstelle den Benutzer-Prompt
    
    if step == "1":
        text = texts["text_theme"]
        schema = theme_schema
        if user_input == "":
            user_prompt = prompts["themes"]
        else:
            user_prompt = prompts["themes_input"].format(input=user_input)
    elif step == "2":
        if feedback != "":
            step = "1"
            text = texts["text_theme"]
            schema = theme_schema
            user_prompt = prompts["feedback"].format(feedback=feedback)
        else:
            text = texts["text_character"]
            schema = character_schema
            user_prompt = prompts["character"].format(theme=user_input)
    elif step == "3":
        if feedback != "":
            step = "2"
            text = texts["text_character"]
            schema = character_schema
            user_prompt = prompts["feedback"].format(feedback=feedback)
        else:
            schema = ResponseSchema
            user_prompt = prompts["adventure_start"].format(protagonist=user_input)
    elif step >= "4":
        schema = ResponseSchema
        user_prompt = prompts["adventure_continue"].format(choice=user_input)
    print(f'user_prompt: {user_prompt}')

    # Rufe das LLM an und verarbeite die Antwort
    if new_history:
        response = ai.chat_call(user_prompt, schema, new_history=True)
    else:
        response = ai.chat_call(user_prompt, schema)
    chatbot_response = response.model_dump()["response"]
    print(f'LLM Response: {chatbot_response}')

    new_history = False

    if step == "1" or step == "2":
        images = ai.image_call(chatbot_response)

        data = {"options": [], "text": text}
        for img, info in zip(images, chatbot_response):
            # Füge die Entscheidungen mit Titel, Beschreibung und Bild-URL der Liste hinzu
            data["options"].append({
                "title": info["title"],
                "description": info["description"],
                "imageUrl": img
            })
        return jsonify({"response": data,
                        "step": step})
    
    else: 
        images = ai.image_call(chatbot_response["options"])

        data = {"options": [], "text": chatbot_response["text"]}
        for img, info in zip(images, chatbot_response["options"]):
            # Füge die Entscheidungen mit Titel, Beschreibung und Bild-URL der Liste hinzu
            data["options"].append({
                "title": info["title"],
                "description": info["description"],
                "imageUrl": img
            })
        return jsonify({"response": data,
                        "step": step})
