from openai import OpenAI
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    api_key = data.get('ApiKey')
    ASSISTANT_ID = data.get('AssistentID')
    prompt = data.get('Prompt')

    client = OpenAI(api_key)
    
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = prompt
    )

    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = ASSISTANT_ID
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id = thread.id, run_id = run.id)
        time.sleep(1)

    messages = client.beta.threads.messages.list(
    thread_id = thread.id
    )

    for it in reversed(messages.data):
        return jsonify(it.content[0].text.value)