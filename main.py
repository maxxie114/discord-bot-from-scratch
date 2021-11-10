import websocket
import json
import requests
import yaml

with open('config.yml', 'r') as f:
    try:
        dict = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

# DEBUG
print(f"token: {dict.get('token')}")
print(f"prefix: {dict.get('prefix')}")


session_id = 0
sequence = 0
channelId = "699800455655718965"
prefix = dict.get('prefix')
token = dict.get('token')
baseURL = "https://discordapp.com/api/channels/{}/messages".format(channelId)
headers = { "Authorization":"Bot {}".format(token),
            "User-Agent":"myBotThing (http://some.url, v0.1)",
            "Content-Type":"application/json", }

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def receive_json_reponse(ws):
    global sequence, session_id, token, resume
    resume = {
        "op": 6,
        "d": {
            "token": token,
            "session_id": session_id,
            "seq": sequence
        }
    }
    try:
        response = ws.recv()
        if response:
            json_data = json.loads(response)
            return json_data
    except websocket.WebSocketConnectionClosedException:
        print("Connection closed, reconnecting")

        ws.connect("wss://gateway.discord.gg/?v=9&encording=json")
        send_json_request(ws, resume)
    except Exception as ex:
        print(ex)

def send_embed(url, headers, title, msg, color):
    body = {
        "embeds": [{
            "title": title,
            "description": msg,
            "color": color
        }]
    }
    json_post_request = json.dumps(body)
    r = requests.post(url, headers = headers, data = json_post_request)

def send_message(url, headers, msg):
    body = {
        "content": msg
    }
    json_post_request = json.dumps(body)
    r = requests.post(url, headers = headers, data = json_post_request)

def parse_command(url, headers, token, command):
    cmd = command[1:].split(" ")
    if cmd[0] == "help":
        message = ("help - Get the help page\n"
                    "testbot - Get the status of the bot\n")
        send_embed(url, headers, "Help Page", message, 0xFF0000)
        return True
    if cmd[0] == "testbot":
        message = "bot online"
        send_message(url, headers, message)
        return True
    send_message(url, headers, "Command doesn't exist, use /help for more info.")
    return False



ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=9&encording=json")
# heartbeat_interval = receive_json_reponse(ws)["d"]["heartbeat_interval"]

# 513 = (1 << 0) + (1 << 9)
payload = {
    "op": 2,
    "d": {
        "token": token,
        "intents": 513,
        "properties": {
            "$os": "linux",
            "$browser": "curl",
            "$device": "server"
        }
    }
}

send_json_request(ws, payload)

while True:
    event = receive_json_reponse(ws)
    try:
        # print(json.dumps(event, indent=4, sort_keys=True))
        # opcode 10: Hello
        if event["op"] == 10:
            print("Hello")
        # opcode 0: Dispatch
        if event["op"] == 0:
            sequence = event["s"]
            if event["t"] == "READY":
                sid = event["d"]["session_id"]
                session_id = sid
            if event["t"] == "MESSAGE_CREATE":
                username = event["d"]["author"]["username"]
                message = event["d"]["content"]
                print(f"{username}:{message}")
                # First check if message is empty
                if not len(message) == 0:
                    # A greeting system
                    if message == "hello":
                        send_message(baseURL, headers, "hi")
                    if message[0] == prefix:
                        print(message)
                        parse_command(baseURL, headers, token, message)
    except Exception as e:
        print(f"Exception: {e}")
    print(f"session_id = {session_id}, sequence = {sequence}")
