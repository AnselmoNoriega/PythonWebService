from flask import Flask, request, jsonify
import time
from openai import OpenAI

app = Flask(__name__)


keyID = "sk-proj-UJlJP7IIAccXodn8iARnT3BlbkFJV8PWozcARMGmt2Gf7CA7"
assistantID = "asst_XOyqJAlc7oJuEKCa1blkFyT7"
promptHistory = ["Whats your name", "What is the biggest animal"]

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
stri = []
for it in messages.data:
    stri.append(it.content[0].text.value + "\n")
print(stri)