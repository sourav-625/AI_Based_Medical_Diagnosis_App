from flask import Flask, request, jsonify
import openai
import time
import textwrap
import os

app = Flask(__name__)

# Function to save files
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

# Function to open files
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

# Load OpenAI API key
openai.api_key = open_file('key_openai.txt').strip()

# Chatbot function
def chatbot(conversation, model="gpt-4-0613", temperature=0, max_tokens=2000):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content']
    except Exception as err:
        return f"Error: {err}"

# Store conversations in memory
user_messages = []
all_messages = []

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"response": "Please enter a valid message."})
    
    user_messages.append(user_input)
    all_messages.append(f'PATIENT: {user_input}')
    
    # Create conversation history
    conversation = [{"role": "system", "content": open_file('intake.md')},
                    {"role": "user", "content": user_input}]
    
    bot_response = chatbot(conversation)
    conversation.append({"role": "assistant", "content": bot_response})
    all_messages.append(f'BOT: {bot_response}')
    
    return jsonify({"response": bot_response})

@app.route('/generate_notes', methods=['POST'])
def generate_notes():
    text_block = '\n\n'.join(all_messages)
    chat_log = f'<<BEGIN PATIENT INTAKE CHAT>>\n\n{text_block}\n\n<<END PATIENT INTAKE CHAT>>'
    save_file(f'chats/chat_{time.time()}_history.txt', chat_log)
    
    conversation = [{"role": "system", "content": open_file('prepare_notes.md')},
                    {"role": "user", "content": chat_log}]
    
    notes = chatbot(conversation)
    return jsonify({"notes": notes})

@app.route('/diagnosis', methods=['POST'])
def diagnosis():
    data = request.json
    notes = data.get("notes", "")
    
    conversation = [{"role": "system", "content": open_file('diagnosis.md')},
                    {"role": "user", "content": notes}]
    
    report = chatbot(conversation)
    return jsonify({"report": report})

@app.route('/clinical_evaluation', methods=['POST'])
def clinical_evaluation():
    data = request.json
    notes = data.get("notes", "")
    
    conversation = [{"role": "system", "content": open_file('clinical.md')},
                    {"role": "user", "content": notes}]
    
    evaluation = chatbot(conversation)
    return jsonify({"evaluation": evaluation})

@app.route('/referrals', methods=['POST'])
def referrals():
    data = request.json
    notes = data.get("notes", "")
    
    conversation = [{"role": "system", "content": open_file('referrals.md')},
                    {"role": "user", "content": notes}]
    
    referrals = chatbot(conversation)
    return jsonify({"referrals": referrals})

if __name__ == '__main__':
    os.makedirs("chats", exist_ok=True)
    app.run(debug=True)
