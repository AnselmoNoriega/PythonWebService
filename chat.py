from openai import OpenAI
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/senddata', methods = ['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    first_string = data.get('firstString')
    second_string = data.get('secondString')

    if first_string is None or second_string is None:
        return jsonify({'error': 'Both "firstString" and "secondString" keys must be present in JSON payload'}), 400

    combined = f"{first_string} {second_string}"
    return jsonify({'combined': combined})

"""
client = OpenAI(api_key = "")

assistant = client.beta.assistants.create(
    name = "Roby",
    instructions = "Your are a math tutor. Write and run code to answer questions",
    tools = [{"type": "code_interpreter"}],
    model = "gpt-3.5-turbo"
    )

ASSISTANT_ID = ""

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "solve 3 plus 5"
)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id = thread.id, run_id = run.id)
    print("Run Status: {run.status}")
    time.sleep(1)
else:
    print("Finished")
    
messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

for it in reversed(messages.data):
    print(it.role + ": " + it.content[0].text.value)
"""