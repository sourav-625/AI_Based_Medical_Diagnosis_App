import openai
from time import time
from halo import Halo
import textwrap

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

def chatbot(conversation, model="gpt-4-0613", temperature=0, max_tokens=2000):
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
            text = response['choices'][0]['message']['content']
            spinner.stop()
            return text, response['usage']['total_tokens']
        except Exception as err:
            print(f'\n\nError communicating with OpenAI: "{err}"')
            exit(5)

def chat_print(text):
    formatted_lines = [textwrap.fill(line, width=120, initial_indent='    ', subsequent_indent='    ') for line in text.split('\n')]
    formatted_text = '\n'.join(formatted_lines)
    print('\n\n\nCHATBOT:\n\n%s' % formatted_text)


if __name__ == '__main__':
    openai.api_key = open_file('key_openai.txt').strip()
    user_messages = list()
    all_messages = list()
    def intake(conversation) :
        conversation.append({'role': 'system', 'content': open_file('intake.md')})
        print('Describe your symptoms to the intake bot.')        
        while True:
            text = input('\n\nPATIENT: ').lower().strip()
            user_messages.append(text)
            all_messages.append('PATIENT: %s' % text)
            conversation.append({'role': 'user', 'content': text})
            response, tokens = chatbot(conversation)
            conversation.append({'role': 'assistant', 'content': response})
            all_messages.append('BOT: %s' % response)
            if response == "done" :
                print('Thank You for cooperating.')
                break
            else :
                print('\n\nBOT: %s' % response)
        return conversation
    intakes = intake([])

    def generate_notes(conversation) :
        conversation = list()
        conversation.append({'role': 'system', 'content': open_file('prepare_notes.md')})
        while(True) :
            text_block = '\n\n'.join(all_messages)
            chat_log = '<<BEGIN PATIENT INTAKE CHAT>>\n\n%s\n\n<<END PATIENT INTAKE CHAT>>' % text_block
            save_file('chats/chat_%s_chat.txt' % time(), chat_log)
            conversation.append({'role': 'user', 'content': chat_log})
            notes, tokens = chatbot(conversation)
            print('\n\n Please check whether this summarizes you condition:\n\n%s' % notes)
            user_agree = input('\n\nPlease write yes or no: ')
            if 'no' in user_agree.split() :
                print('\n\nThen Please give more information about your condition.\n\n')
                intakes = intake(intakes)
                continue
            else : break
        return notes
    notes = generate_notes([])

    print('\n\nGenerating a Report for you')
    conversation = list()
    conversation.append({'role': 'system', 'content': open_file('diagnosis.md')})
    conversation.append({'role': 'user', 'content': notes})
    report, tokens = chatbot(conversation)
    notes_report = 'NOTES:\n\n' + notes + '\n\nREPORT:\n\n' + report
    print('\n\nReport:\n\n%s' % report)

    print('\n\nEvaluation')
    conversation = list()
    conversation.append({'role': 'system', 'content': open_file('clinical.md')})
    conversation.append({'role': 'user', 'content': notes})
    clinical, tokens = chatbot(conversation)
    notes_report_clinical = notes_report + '\n\nC' + clinical
    print('\n\nClinical Evaluation:\n\n%s' % clinical)

    print('\n\nFor better diagnosis please refer to:')
    conversation = list()
    conversation.append({'role': 'system', 'content': open_file('referrals.md')})
    conversation.append({'role': 'user', 'content': notes})
    referrals, tokens = chatbot(conversation)
    history = notes_report_clinical + referrals
    print('\n\nReferrals and Tests:\n\n%s' % referrals)

    save_file('chats/chat_%s_history.txt' % time(), history)
