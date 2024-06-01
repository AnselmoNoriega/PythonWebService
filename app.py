from flask import Flask, request, jsonify
import time
from openai import OpenAI

app = Flask(__name__)


keyID = "sk-proj-UJlJP7IIAccXodn8iARnT3BlbkFJV8PWozcARMGmt2Gf7CA7"
assistantID = "asst_XOyqJAlc7oJuEKCa1blkFyT7"
prompt = "Whats your name"

client = OpenAI(api_key = keyID)

thread = client.beta.threads.create()
thread.id = "thread_dX5ItcTiOWRY0cEsAs5yAMm5"

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
print(messages.data[0].content[0].text.value)

client = OpenAI(api_key = keyID)
thread = client.beta.threads.create()
thread.id = "thread_dX5ItcTiOWRY0cEsAs5yAMm5"
prompt = "What was my first question and whats 3 plus 3"

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
print(messages.data[0].content[0].text.value)