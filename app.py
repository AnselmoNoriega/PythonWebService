from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from openai import OpenAI
import struct

app = Flask(__name__)
CORS(app)

@app.route('/senddata', methods = ['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    keyID = "sk-proj-UJlJP7IIAccXodn8iARnT3BlbkFJV8PWozcARMGmt2Gf7CA7"
    assistantID = "asst_XOyqJAlc7oJuEKCa1blkFyT7"
    prompt = data.get('Prompt')
    threadID = data.get('ThreadID')
    
    client = OpenAI(api_key = keyID)
    
    thread = client.beta.threads.create()
    thread.id = threadID

    client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = prompt
    )

    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistantID
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id = thread.id, run_id = run.id)
        time.sleep(1)
        
    messages = client.beta.threads.messages.list(thread_id = thread.id)

    return jsonify(messages.data[0].content[0].text.value)

@app.route('/convert', methods=['POST'])
def convert_bytes_to_floats():
    byte_array = request.get_data()
    
    num_floats = len(byte_array) // 4
    float_array = struct.unpack('f' * num_floats, byte_array)
    
    return jsonify(float_array)

@app.route('/getdata', methods = ['GET'])
def send_data():
    keyID = "sk-proj-UJlJP7IIAccXodn8iARnT3BlbkFJV8PWozcARMGmt2Gf7CA7"
    client = OpenAI(api_key = keyID)
    id = client.beta.threads.create().id
    return jsonify(id)