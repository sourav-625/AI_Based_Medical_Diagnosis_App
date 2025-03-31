from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Load OpenAI API key
openai.api_key = "your_openai_api_key_here"  # Replace with your actual API key

# Function to open files
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"response": "Please enter a valid message."})
    
    # Create conversation history using intake.md
    conversation = [
        {"role": "system", "content": open_file('Commands/intake.md')},
        {"role": "user", "content": user_input}
    ]
    
    bot_response = chatbot(conversation)
    return jsonify({"response": bot_response})

@app.route('/generate_notes', methods=['POST'])
def generate_notes():
    data = request.json
    chat_log = data.get("chat_log", "")
    
    if not chat_log:
        return jsonify({"notes": "No chat log provided."})
    
    # Use prepare_notes.md for generating notes
    conversation = [
        {"role": "system", "content": open_file('Commands/prepare_notes.md')},
        {"role": "user", "content": chat_log}
    ]
    
    notes = chatbot(conversation)
    return jsonify({"notes": notes})

@app.route('/diagnosis', methods=['POST'])
def diagnosis():
    data = request.json
    notes = data.get("notes", "")
    
    if not notes:
        return jsonify({"report": "No notes provided."})
    
    # Use diagnosis.md for generating diagnosis
    conversation = [
        {"role": "system", "content": open_file('Commands/diagnosis.md')},
        {"role": "user", "content": notes}
    ]
    
    report = chatbot(conversation)
    return jsonify({"report": report})

@app.route('/clinical_evaluation', methods=['POST'])
def clinical_evaluation():
    data = request.json
    notes = data.get("notes", "")
    
    if not notes:
        return jsonify({"evaluation": "No notes provided."})
    
    # Use clinical.md for clinical evaluation
    conversation = [
        {"role": "system", "content": open_file('Commands/clinical.md')},
        {"role": "user", "content": notes}
    ]
    
    evaluation = chatbot(conversation)
    return jsonify({"evaluation": evaluation})

@app.route('/referrals', methods=['POST'])
def referrals():
    data = request.json
    notes = data.get("notes", "")
    
    if not notes:
        return jsonify({"referrals": "No notes provided."})
    
    # Use referrals.md for generating referrals
    conversation = [
        {"role": "system", "content": open_file('Commands/referrals.md')},
        {"role": "user", "content": notes}
    ]
    
    referrals = chatbot(conversation)
    return jsonify({"referrals": referrals})

if __name__ == '__main__':
    app.run(debug=True)