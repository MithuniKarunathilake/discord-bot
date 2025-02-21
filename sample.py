from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get('action')
    repo_name = data['repository']['full_name']
    pr_number = data['pull_request']['number']
    pr_title = data['pull_request']['title']

    message = f'PR #{pr_number}: {pr_title} ({action}) in {repo_name}'

    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if webhook_url:
        requests.post(webhook_url, json={'content': message})

    return '', 200