# -*- coding: UTF-8 -*- 

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import json
import threading
import multiprocessing
import time
from master import *

global MASTER
global center
MASTER = Master()

center = MASTER.center_data()

app = Flask('server')
CORS(app)
app.config['SECRET_KEY'] = '199624f47e49f3fb1e3f66484f4f7814'
socketio = SocketIO(app, cors_allowed_origins="*")

MASTER.socketio = socketio

@socketio.on('connect')
def handle_connect():
    print('received connection!')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')


@socketio.on('message')
def handle_message(message):
    print("receive: " + message)


@app.route('/')
@app.route('/home')
def home():
    return "Server Home"

'''
1️⃣ Rooms Part
'''

@socketio.on('update_rooms')
def handle_update_rooms():
    d = MASTER.get_all_room()
    # print(d)
    emit("getRooms", d, broadcast=True)

@app.route('/rooms/checkIn', methods=['POST'])
def checkIn():
    req = request.get_json(force=True)
    print(req)
    req['checkInDate'] = time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))
    req['haveCheckIn'] = True
    
    MASTER.slaves[int(req['id'])].name = req['name']
    MASTER.slaves[int(req['id'])].idCard = req['idCard']
    MASTER.slaves[int(req['id'])].checkInDate = req['checkInDate']
    MASTER.slaves[int(req['id'])].haveCheckIn = req['haveCheckIn']
    MASTER.slaves[int(req['id'])]._showDetails = req['_showDetails']
    
    print(MASTER.slaves[int(req['id'])].__dict__)
    MASTER.checkIn(req['id'], req['name'], req['idCard'], req['checkInDate'], req['_showDetails'])
    
    d = MASTER.get_all_room()
    socketio.emit("getRooms", d, broadcast=True)
    return  req


@app.route('/rooms/checkOut', methods=['POST'])
def checkOut():
    req = request.get_json(force=True)
    print(req)
    for k in req.keys():
        if k == 'id':
            continue
        if k == 'power' or k == '_showDetails':
            req[k] = 'False'
        else:
            req[k] = ''    
    MASTER.slaves[int(req['id'])].__dict__.update(MASTER.slave_init[int(req['id'])])

    now_time =time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))
    MASTER.checkOut(req['id'],now_time)
    socketio.emit("getRooms", MASTER.get_all_room(), broadcast=True)
    # 其实这个return还是会被rooms信息覆盖，走个形式
    return req


'''
2️⃣ Auth Part
'''


@app.route('/auth/register', methods=['POST'])
def register():
    req = request.get_json(force=True)
    print(req)
    if MASTER.add_admin(req['email'], req['pwd']) == False:
        return jsonify({'error': True})    
    return jsonify({'error': False})


@app.route('/auth/loginAdmin', methods=['POST'])
def loginAdmin():
    req = request.get_json(force=True)
    print(req)
    if MASTER.login_admin(req['email'], req['pwd']) == False:
        return jsonify({'error': True})
    return jsonify({'error': False})


@app.route('/auth/login', methods=['POST'])
def login():
    req = request.get_json(force=True)
    print(req)
    if req['idCard'] == '':
        return jsonify({'error':True})
    if int(req['roomId']) < 0 or int(req['roomId'])>=len(MASTER.slaves):
        return jsonify({'error': True})
    if MASTER.login(req['roomId'], req['idCard']) == False:
        return jsonify({'error': True})
    return jsonify({'error': False})


'''
3️⃣ Center Part 中央空调状态
'''

@socketio.on('update_center')
def handle_update_center():
    emit("getCenter", center, broadcast=True)


@app.route('/center/flipPower', methods=['POST'])
def flipPower():
    center['power'] = not center['power']
    MASTER.power = not MASTER.power
    socketio.emit("getCenter", center, broadcast=True)
    return jsonify(center)


@app.route('/center/setMode', methods=['POST'])
def setMode():
    req = request.get_json(force=True)
    print(req)
    MASTER.mode = center['mode'] = req['mode']
    MASTER.temp = center['temp'] = 25
    socketio.emit("getCenter", center, broadcast=True)
    return jsonify(center)


@app.route('/center/temp_add', methods=['POST'])
def temp_add():
    req = request.get_json(force=True)
    print(req)
    center['temp'] += req['offset']
    MASTER.temp = center['temp']
    socketio.emit("getCenter", center, broadcast=True)
    return jsonify(center)


@app.route('/center/freq_add', methods=['POST'])
def freq_add():
    req = request.get_json(force=True)
    print(req)
    center['freq'] += req['offset']
    MASTER.frequence = center['freq']
    socketio.emit("getCenter", center, broadcast=True)
    return jsonify(center)


'''
4️⃣ Slave Part 从控机状态，复用了rooms的状态
'''

def send_and_wait_task(t,id):
    def task():
        # MASTER.signals[id].acquire()
        t(id)
        # MASTER.signals[id].notify()
        # MASTER.signals[id].release()
        return
    # MASTER.signals[id].acquire()
    MASTER.request_queue.put(task)
    # MASTER.signals[id].release()
    # MASTER.signals[id].acquire()
    # MASTER.signals[id].wait()


#从控机开关机
@app.route('/rooms/flipPower', methods=['POST'])
def slave_flipPower():
    req = request.get_json(force=True)
    print(req)
    id = int(req['id'])
    MASTER.slaves[id]['power'] = not MASTER.slaves[id]['power']

    def task(id):
        MASTER.slaveFilpPower(str(id))
    send_and_wait_task(task,id)

    MASTER.respond_to_request()
    MASTER.update_state()
    data = MASTER.get_one_room(req['id'])
    socketio.emit("getRooms", MASTER.get_all_room(), broadcast=True)
    return jsonify(data)

# 从控机温度变化
@app.route('/rooms/temp_add', methods=['POST'])
def slave_temp_add():
    req = request.get_json(force=True)
    print(req)
    id = int(req['id'])
    # print(MASTER.slaves[id].expectTemp, type(MASTER.slaves[id].expectTemp))
    MASTER.slaves[id].expectTemp = str(int(MASTER.slaves[id].expectTemp) +  int(req['offset']))
    
    def task(id):
        MASTER.slaveTempadd(str(id), int(req['offset']))
    send_and_wait_task(task,id)

    MASTER.respond_to_request()
    MASTER.update_state()
    data = MASTER.get_one_room(req['id'])
    print(data)
    socketio.emit("getRooms", MASTER.get_all_room(), broadcast=True)
    return jsonify(data)

# 从控机风速变化
@app.route('/rooms/set_speed', methods=['POST'])
def slave_set_speed():
    req = request.get_json(force=True)
    print(req)
    id = int(req['id'])
    MASTER.slaves[id]['speed'] = req['speed']

    def task(id):
        MASTER.slave_setSpeed(req['id'], req['speed'])
    send_and_wait_task(task, id)
    
    MASTER.respond_to_request()
    MASTER.update_state()
    data = MASTER.get_one_room(req['id'])
    socketio.emit("getRooms", MASTER.get_all_room(), broadcast=True)
    return jsonify(data)


#打开details
@app.route('/rooms/flipShow', methods=['POST'])
def slave_flipShow():
    req = request.get_json(force=True)
    print(req)
    id = int(req['id'])
    MASTER.slaves[id]['_showDetails'] = not MASTER.slaves[id]['_showDetails']
    print(MASTER.slaves[id])
    MASTER.update_state()

    socketio.emit("getRooms", MASTER.get_all_room(), broadcast=True)
    return MASTER.slaves[id].jsonify()

# @app.route('/rooms/updateRooms', methods=['POST'])
# def slave_updateRooms():
#     req = request.get_json(force=True)
#     for slave_state in req:
#         MASTER.slaves[int(slave_state['id'])].__dict__.update(slave_state)
#     # MASTER.update_state()
#     return jsonify([s.__dict__ for s in MASTER.slaves])


@app.route('/rooms/updateRooms', methods=['POST'])
def slave_updateRooms():
    req = request.get_json(force=True)
    for slave_state in req:
        MASTER.slaves[int(slave_state['id'])].__dict__.update(slave_state)
        
        slave = MASTER.slaves[int(slave_state['id'])]
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute("update slave set name=%s, idCard=%s where id=%s",
                              (slave.name, slave.idCard, slave.id))
        cursor.close()
        db.commit()
        db.close()
    return jsonify([s.__dict__ for s in MASTER.slaves])

# @app.route('/slave/update_state', methods=['POST'])
# def slave_update_state():
#     req = request.get_json(force=True)
#     new_state = json.loads(req['new_state'])
#     id = int(new_state['id'])
#     def task(id):
#         MASTER.slaves[id].update(new_state)
#     send_and_wait_task(task,id)

#     return MASTER.slaves[id].jsonify()

'''
# Form Part
'''

@app.route('/form/roomList')
def get_room_list():
    ret = MASTER.get_room_list()
    print(ret)
    return jsonify(ret)


@app.route('/form/rep',methods=['POST'])
def get_form():
    req=request.get_json()
    sd,ed,sr,er=req['sd'],req['ed'],req['sr'],req['er']
    ret=MASTER.get_form(sd,ed,sr,er)
    return jsonify(ret)



if __name__ == "__main__":
    th = threading.Thread(target=MASTER.background, name="我是后台线程")
    th.daemon = True
    th.start()
    socketio.run(app)
    print("server.py中: main 函数退出.")
