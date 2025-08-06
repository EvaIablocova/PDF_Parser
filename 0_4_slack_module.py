import requests
import json


def send_slack_message(message):
    with open('sec_config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    webhook_url = config['webhook_url']

    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Message to Slack sent successfully.")
    else:
        print(f"Failed to send message to Slack: {response.text}")

