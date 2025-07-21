# MediBot - AI Based Medical Diagnosis

## Overview
This Python-based Medical Diagnosis App allows users to input their symptoms, which are then processed by an AI-powered chatbot (using OpenAI's GPT-4 model) to provide a diagnosis, clinical evaluation, and referral suggestions. The app helps users track their symptoms, summarize their condition, and potentially generate reports based on the diagnosis.

## Features
**Symptom Intake:** Users describe their symptoms, and the chatbot gathers information.  
**Notes Generation:** The chatbot processes the input to create a summary of the symptoms.  
**Diagnosis Report:** Based on the notes, the chatbot generates a hypothesis diagnosis.  
**Clinical Evaluation:** Further evaluation of the condition is generated based on the input.  
**Referrals and Tests:** Provides recommendations for referrals and tests.  
**Logs:** Logs user inputs and AI responses to text files for record-keeping.

## Requirements
Python 3.7 or higher  
OpenAI API key (for chatbot interaction)   
Required Python libraries (listed below)

## Installation
Clone this repository:

```bash
git clone https://github.com/sourav-625/MediBot.git
cd MediBot
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Required Python Libraries:

**openai** – For making requests to the OpenAI API.  
**halo**(Optional) – For a loading spinner during chatbot interactions.  
**textwrap** – For wrapping long text into readable lines.  
**time** – For timestamping log files.

## Get an OpenAI API Key:

Sign up for an API key from OpenAI if you don’t have one: https://beta.openai.com/signup/.  
Store the API key in a file named key_openai.txt in the root directory of the project.  
Usage  
Run the Application: To start the app, simply run the script:

```bash
python app.py
```

## Interact with the Bot:

You will be prompted to describe your symptoms.
The bot will ask follow-up questions based on your input until it receives enough information.
You’ll be asked to confirm the generated notes. If you disagree with the summary, you can provide more details.
The bot will then generate a diagnosis, clinical evaluation, and suggestions for tests or referrals.
Logs: The application will create log files in the logs/ directory, which include details of the chat, diagnosis, clinical evaluation, and referrals. You can view these logs at any time.

## Customization:

You can modify the system prompt files (intake.md, prepare_notes.md, etc.) to customize the questions or style of the responses.
You can adjust the temperature and max token settings in the chatbot() function for different types of responses from the AI model.  
Example Interaction  
plaintext
Copy  
Describe your symptoms to the intake bot.

```
PATIENT: I have a headache and a sore throat.

BOT: Can you tell me if you have a fever or any other symptoms?
...
Once the user confirms the notes and responses, the bot generates a diagnosis and suggestions for further evaluation or tests.
```

## Contributing

If you'd like to contribute to the project, feel free to submit a pull request or raise an issue.
