from flask import Flask, request, jsonify
import time
from openai import OpenAI

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    keyID = "sk-proj-UJlJP7IIAccXodn8iARnT3BlbkFJV8PWozcARMGmt2Gf7CA7"
    assistantID = "asst_XOyqJAlc7oJuEKCa1blkFyT7"
    promptHistory = data.get('PromptHistory')
    
    client = OpenAI(api_key = keyID)
    
    thread = client.beta.threads.create()

    for prevPromt in promptHistory:
        client.beta.threads.messages.create(
            thread_id = thread.id,
            role = "user",
            content = prevPromt
        )

    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistantID
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id = thread.id, run_id = run.id)
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id = thread.id)

    stri = ["start", "second"]
    for it in messages.data:
        stri.append(it.content[0].text.value)
    return jsonify(stri)