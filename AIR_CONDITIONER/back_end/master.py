import inspect
import threading
import pymysql
import json
import os
import time
from queue import Queue
from slave import *
import copy
# import csv
from mysqlTable import *

NORMAL_TEMPERATURE = 25

DATABASE_USER_NAME = "root"
DATABASE_USER_PASSWORD = "ps123456"
DATABASE_SCHEMA = "user"

lock = threading.Lock()

class Master(Base):
    def __init__(self):
        self.db = pymysql.connect(
            "localhost", DATABASE_USER_NAME, DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        self.cursor = self.db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        
        # 建表
        self.cursor.execute(admin_drop)
        self.cursor.execute(admin_create)

        self.cursor.execute(slave_drop)
        self.cursor.execute(slave_create)

        self.cursor.execute(oprecord_drop)
        self.cursor.execute(oprecord_create)

        self.cursor.execute(checkrecord_drop)
        self.cursor.execute(checkrecord_create)
        self.db.commit()

        self.add_admin('a@c','123')

        self.power = False
        self.state = 'Standby'
        self.mode = "Cold"
        self.temp = 25

        self.frequence = 120    # 刷新频率120s
        self.opened_time = 0

        # 直接将各个slave抽象成为master的一个部件
        self.SLAVE_NUM = 10
        # self.slaves = [Slave(str(i), "") for i in range(self.SLAVE_NUM)]
        self.slaves = []
        for i in range(self.SLAVE_NUM):
            self.slaves.append(Slave(str(i), ''))
            self.init_slave(self.slaves[i].__dict__)

        # 管理员列表
        # self.admins = []
        self.slave_init = copy.deepcopy(self.slaves)

        # HTTP请求队列
        self.signals = [threading.Condition() for i in range(self.SLAVE_NUM)]
        self.request_queue = Queue()

        # 调度队列
        self.blowing_list = []
        self.schedule_queue = []

        self.socketio = None

    # center_page

    def center_data(self) -> dict:
        center = {}
        center['power'] = self.power
        center['state'] = self.state
        center['mode'] = self.mode
        center['temp'] = self.temp
        center['freq'] = self.frequence
        return center

    def __del__(self):
        self.cursor.close()  # 关闭游标
        self.db.close()     # 关闭数据库连接

    # init_room
    def init_slave(self, d: dict):
        try:
            sql = 'insert into slave values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            self.cursor.execute(sql, (d['id'], d['name'], d['idCard'], d['checkInDate'],
                                      d['cost'], d['expectTemp'], d['speed'], d['temp'], False, '0', False, False))
            self.db.commit()
            # print("insert slave", end=' ')
        except:    # 主键约束
            sql = 'update slave set name=%s, idCard=%s, checkInDate=%s, cost=%s, expectTemp=%s, speed=%s, temp=%s, \
                    power=%s, timer=%s, haveCheckIn=%s, showDetails=%s where id = %s'
            self.cursor.execute(sql, (d['name'], d['idCard'], d['checkInDate'], d['cost'],
                                      d['expectTemp'], d['speed'], d['temp'], False, '0', False, False, d['id']))
            self.db.commit()
            # print("update slave", end=' ')

    # /rooms/路由 all_rooms_info

    def get_all_room(self) -> list:
        rooms = []
        db = pymysql.connect("localhost", DATABASE_USER_NAME, DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        lock.acquire()
        cursor.execute("select * from slave")
        lock.release()
        db.commit()
        
        while 1:
            res = cursor.fetchone()
            if res is None:  # 表示已经取完结果集
                break
            d = {
                'id': res[0],
                'haveCheckIn': False if res[10] == '0' else True,
                'name': res[1],
                'idCard': res[2],
                'checkInDate': res[3],
                'cost': res[4],
                'expectTemp': res[5],
                'speed': res[6],
                'temp': res[7],
                'power': False if res[8] == '0' else True,
                '_showDetails': False if res[11] == '0' else True,
                'is_blowing_in': self.slaves[int(res[0])].is_blowing_in
            }
            rooms.append(d)
        
        cursor.close()
        db.close()
        return rooms

    # 获取当前房间的记录号(tzy)
    def get_CheckRecord_Record(self, roomId: str):
        # 对于当前房间号，获取其入住状态为1的记录，即入住中的记录
        sql = 'select Record from CheckRecord where id = %s and state =%s'
        lock.acquire()
        self.cursor.execute(sql, (roomId, '1'))
        self.db.commit()
        lock.release()
        rec_no = ''
        if self.cursor is not None:  # 注意这里: 单纯判断cursor是否为None是不够的
            row = self.cursor.fetchone()
            if row is not None:
                rec_no = row[0]

        return rec_no

    # 获取当前房间的从控机状态(tzy)
    def get_slave_power(self, roomId: str):
        try:    # 如果开始数据库没有数据怎么办...
            sql = 'select power from slave where id = %s'
            lock.acquire()
            self.cursor.execute(sql, (roomId))
            power = self.cursor.fetchone()[0]
            self.db.commit()
            lock.release()
        except Exception as reason:
            power = '0'
            print(reason)
        return power  # 对于当前房间号，获取其从控机的开关机情况

    # 获取当前的入住记录数(tzy)

    def get_CheckRecord_count(self):
        query = " select count(*) from CheckRecord "
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return count

    # 获取操作记录记录数(tzy)
    def get_OpRecord_count(self):
        query = " select count(*) from OpRecord "
        lock.acquire()
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        self.db.commit()
        lock.release()
        return count

    # 获取送风时间,读出计时器的值(tzy)
    def get_slave_timer(self, roomId: str):
        sql = 'select timer from slave where id = %s'
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(sql, (roomId))
        tim = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return tim

    # 更新计时器的值(tzy)
    def update_slave_timer(self, roomId: str, timer: str):
        sql = 'update slave set timer=%s where id = %s'
        
        lock.acquire()
        self.cursor.execute(sql, (timer, roomId))
        lock.release()
        self.db.commit()

    # 获取风速(tzy)
    def get_slave_speed(self, roomId: str):
        sql = 'select speed from slave where id = %s'
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(sql, (roomId))
        speed = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return speed

    # 获取新的阶段送风量 = 风速 * 时间(tzy)
    def cal_wind(self, roomId: str, speed: str):
        wind = 0
        tim = self.get_slave_timer(roomId)
        if speed == 'High':
            wind = 1.2 * float(tim) / 60
        if speed == 'Mid':
            wind = 1 * float(tim) / 60
        if speed == 'Low':
            wind = 0.8 * float(tim) / 60
        return wind

    # 获取新的总费用 = 原花费 + 单位 * 送风量(tzy)
    def cal_cost(self, roomId: str, wind: str):
        # 获取原先费用
        sql = 'select cost from slave where id = %s'

        lock.acquire()
        self.cursor.execute(sql, roomId)
        lock.release()
        cost = self.cursor.fetchone()[0]
        # 获取价钱
        cost = round(float(cost), 2) + 5 * round(float(wind), 2)
        return cost

    # 更新某房间的送风量和费用，插入新记录(tzy)
    # type初始为0；1，开关机；2，设定温度 temp1 -> temp2；3，设定风速 speed1 -> speed2;4，每一分钟的例行更新；
    def update_cost_and_wind(self, roomId: str, typ: str, old: str, new: str):  # time以秒为单位
        speed = ' '
        if typ != '3':
            speed = self.get_slave_speed(roomId)
        else:
            speed = old
        wind = self.cal_wind(roomId, speed)
        cost = self.cal_cost(roomId, wind)
        # 对于当前房间号，获取其入住状态为1的记录，即入住中的记录
        rec_no = self.get_CheckRecord_Record(roomId)
        print("this op is oprated by rec_no = %s" % (rec_no))
        now_time = time.strftime('%Y-%m-%d %H:%M:%S ',
                                 time.localtime(time.time()))
        # 将slave和oprecord中的cost和wind更新
        # print("roomid = %s  wind=%s cost = %s timer = %s" %(roomId,wind, cost, run_time))
        sql = 'insert into OpRecord(Record,time, type, old, new, wind, cost) values(%s, %s,%s, %s, %s, %s, %s)'
        
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(sql, (rec_no, now_time, typ, old, new, str(round(wind, 2)), str(round(cost, 2))))
        db.commit()
        cursor.execute("update slave set cost=%s where id=%s", (round(cost, 2), roomId))
        db.commit()
        cursor.close()
        db.close()

    # room checkIn
    def checkIn(self, roomId: str, name: str, idCard: str, date: str, show: bool):
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        sql = 'update slave set name=%s, idCard=%s, checkInDate=%s, timer=%s, haveCheckIn=%s, showDetails=%s where id = %s'
        lock.acquire()
        cursor.execute(sql, (name, idCard, date, '0', True, show, roomId))
        lock.release()
        db.commit()
        # 入住，check in会增加一次开房记录(tzy)
        sql = 'insert into CheckRecord(Record,idcard, id, checkInDate, checkOutDate, state) values(%s, %s, %s, %s, %s, %s)'
        rec_num = self.get_CheckRecord_count()
        lock.acquire()
        cursor.execute(sql, (rec_num, idCard, roomId, date, 'NULL', '1'))
        lock.release()
        db.commit()
        cursor.close()
        db.commit()
        # 把开房编号赋值给从控机
        self.slaves[int(roomId)].record = rec_num

    # 离开，把这一次入住记录改为离开(tzy)
    def checkOut(self, roomId: str, date: str):
        # 查看房间空调状态是否为关机，不是关机就计算费用，插入记录
        sql = 'select power from slave where id = %s'
        
        lock.acquire()
        self.cursor.execute(sql, roomId)
        lock.release()
        res = self.cursor.fetchone()[0]
        if res != '0':  # 数据库中状态变为关机就计算费用，同时清零原计时，后台运行的线程会停止计时
            self.update_cost_and_wind(roomId, '1', '1', '0')
            sql = 'update slave set power=(not power), showDetails=%s, haveCheckIn = %s where id = %s'
            # 
            lock.acquire()
            self.cursor.execute(sql, (False, '0', roomId))
            lock.release()
            self.db.commit()
            self.update_slave_timer(roomId, 0)
        # 对于当前房间号，获取其入住状态为1的记录，即入住中的记录
        rec_no = self.get_CheckRecord_Record(roomId)
        # 将这个记录号的状态改为离开
        sql = 'update CheckRecord set checkOutDate=%s, state=%s where Record=%s'
        # 
        lock.acquire()
        self.cursor.execute(sql, (date, '0', rec_no))
        lock.release()
        self.slave_init[int(roomId)].temp = self.slaves[int(roomId)].temp
        self.init_slave(self.slave_init[int(roomId)])
        self.db.commit()

    # 添加管理员
    def add_admin(self, email: str, code: str) -> bool:
        try:
            sql = 'insert into admin values(%s, %s)'
            
            lock.acquire()
            self.cursor.execute(sql, (email, code))
            self.db.commit()    # 需要commit才可以提交插入
            lock.release()
        except Exception as reason:
            print("add_admin", reason)
            return False
        return True

    # 管理员登录
    def login_admin(self, email: str, code: str) -> bool:
        sql = "select * from admin where email = %s"
        
        lock.acquire()
        self.cursor.execute(sql, email)
        res = self.cursor.fetchone()
        lock.release()
        self.db.commit()
        if res == None or res[1] != code:
            return False
        else:
            return True

    # 客户（从控机）登录
    def login(self, roomId: str, idCard: str) -> bool:
        sql = "select * from slave where id = %s"
        
        lock.acquire()
        self.cursor.execute(sql, roomId)
        res = self.cursor.fetchone()
        lock.release()
        self.db.commit()
        if res == None or res[2] != idCard:
            return False
        else:
            return True

    # 获取一个房间信息
    def get_one_room(self, roomId: str) -> dict:
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                              DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        lock.acquire()
        cursor.execute("select * from slave where id = %s", roomId)
        lock.release()
        db.commit()
        res = cursor.fetchone()
        d = {
            'id': res[0],
            'name': res[1],
            'idCard': res[2],
            'checkInDate': res[3],
            'cost': res[4],
            'expectTemp': res[5],
            'speed': res[6],
            'temp': res[7],
            'power': False if res[8] == '0' else True,
            'haveCheckIn': False if res[10] == '0' else True,
            '_showDetails': False if res[11] == '0' else True,
            'is_blowing_in':self.slaves[int(res[0])].is_blowing_in
        }
        cursor.close()
        db.close()
        return d

    # slave/flipPower
    def slaveFilpPower(self, roomId: str):
        sql = 'update slave set power=(not power), showDetails=%s where id = %s'
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        cursor.execute(sql, (True, roomId))
        db.commit()

        sql = 'select power from slave where id = %s'
        lock.acquire()
        cursor.execute(sql, roomId)
        lock.release()
        res = cursor.fetchone()[0]
        if res == '0':
            # 数据库中状态变为关机就计算费用，同时清零原计时，后台运行的线程会停止计时
            self.update_cost_and_wind(roomId, '1', '1', '0')
            self.update_slave_timer(roomId, 0)
        else:
            # 数据库中状态变为开机开始计算费用，同时后台运行的线程会开始计时
            self.update_cost_and_wind(roomId, '1', '0', '1')
        cursor.close()
        db.close()

    # 从控机温度变化，salve/temp_add
    def slaveTempadd(self, roomId: str, temp: int):
        self.db.ping(reconnect=True)
        lock.acquire()
        self.cursor.execute("select expectTemp from slave where id=%s", roomId)
        res = self.cursor.fetchone()[0]
        exp_temp = int(res) + temp
        self.cursor.execute(
            "update slave set expectTemp=%s, showDetails=%s where id=%s", (str(exp_temp), True, roomId))
        lock.release()
        self.update_cost_and_wind(roomId, '2', res, exp_temp)
        self.update_slave_timer(roomId, 0)
        self.db.commit()

    # 从控机速度变化，送风计时清零，计算上一阶段的费用
    def slave_setSpeed(self, roomId: str, wind: str):
        res = self.get_slave_speed(roomId)
        
        lock.acquire()
        self.cursor.execute(
            "update slave set speed=%s, showDetails=%s where id=%s", (wind, True, roomId))
        lock.release()
        self.update_cost_and_wind(roomId, '3', res, wind)
        self.update_slave_timer(roomId, 0)
        self.db.commit()

    def get_OpRecord_id(self, Record: str):
        sql = 'select id from CheckRecord where Record = {}'.format(Record)
        
        lock.acquire()
        self.cursor.execute(sql)
        lock.release()
        id = self.cursor.fetchone()[0]
        self.db.commit()
        return id

    def get_room_list(self):
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        cursor = db.cursor()
        lock.acquire()
        cursor.execute("select id from slave")
        lock.release()
        db.commit()
        ret = []
        while 1:
            t = cursor.fetchone()
            if t is None:
                break
            ret.append(t)
        cursor.close()
        db.close()
        return ret

    # 获取表单staring date,ending date,starting room,ending room
    def get_form(self, sd, ed, sr, er):
        sql = "select * from OpRecord where time between \"{}\" and \"{}\"".format(sd, ed)
        self.cursor.execute(sql)
        ret = []
        all_record = self.cursor.fetchall()
        count = 0
        if all_record is not None:
            count = len(all_record)

        i = 0
        while i < count:
            t = all_record[i]
            if t is None:
                break
            rid = self.get_OpRecord_id(t[0])
            if  int(sr[0])  <= int(rid) and int(rid) <= int(er[0]):
                ret.append({
                    "id": rid,
                    "time": t[1],
                    "type": t[2],
                    "old": t[3],
                    "new": t[4],
                    "wind": t[5],
                    "cost": t[6]
                })
            i = i + 1
        self.db.commit()
        return ret

    def update_state(self):
        db = pymysql.connect("localhost", DATABASE_USER_NAME,
                             DATABASE_USER_PASSWORD, DATABASE_SCHEMA)  # 打开数据库连接
        wind = {'Low': 5, 'Mid': 4, 'High': 3, 'Shutdown': 7}



        for idx, slave in enumerate(self.slaves):
            # print(slave.jsonify())
            if slave['power'] == True:
                if abs(int(slave.expectTemp) - int(slave.temp)) >= 1:
                    if idx not in self.blowing_list and idx not in self.schedule_queue:
                        # 温度未达到要求,且没有加入队列,那么将其加入到等待队列
                        self.schedule_queue.append(idx)
                        if self.mode == 'Cold' and int(slave.expectTemp) > int(slave.temp):
                            self.schedule_queue.remove(idx)
                        if self.mode == 'Hot' and int(slave.expectTemp) < int(slave.temp):
                            self.schedule_queue.remove(idx)
                    else:
                        if idx in self.blowing_list:
                            # 该机器被调度到送风队列了,开启送风
                            if slave['is_blowing_in'] == False:
                                self.update_cost_and_wind(idx,'5','0','1')
                                slave['is_blowing_in'] = True
                            else:
                                # 已经在送风了,啥也不用管
                                pass
                else:
                    if idx in self.blowing_list:
                        self.blowing_list.remove(idx)
                    if idx in self.schedule_queue:
                        self.schedule_queue.remove(idx)
                    if slave['is_blowing_in'] == True:
                        # 温度已经达到要求,送风停止
                        self.update_cost_and_wind(idx,'5','1','0')
                        slave['is_blowing_in'] = False
            else:
                if idx in self.blowing_list:
                    self.blowing_list.remove(idx)
                if idx in self.schedule_queue:
                    self.schedule_queue.remove(idx)
                if slave['is_blowing_in'] == True:
                    # 空调关机,送风停止
                    self.update_cost_and_wind(idx,'5','1','0')
                    slave['is_blowing_in'] = False

            if slave['power'] == True and slave['is_blowing_in'] == True:
                # 开机状态
                if self.opened_time % wind[slave.speed] == 0:
                    if int(slave.expectTemp) - int(slave.temp) >= 1:
                        slave.temp = str(int(slave.temp) + 1)
                    elif int(slave.expectTemp) - int(slave.temp) <= -1:
                        slave.temp = str(int(slave.temp) - 1)
            else:
                if self.opened_time % wind['Shutdown'] == 0:
                    if NORMAL_TEMPERATURE > int(slave.temp):
                        slave.temp = str(int(slave.temp) + 1)
                    elif NORMAL_TEMPERATURE < int(slave.temp):
                        slave.temp = str(int(slave.temp) - 1)

            detail_str = "%s"  % "1" if slave._showDetails else "0"
            
            cursor = db.cursor()
            lock.acquire()
            cursor.execute("update slave set name=%s, idCard=%s, temp=%s, showDetails=%s where id=%s", 
                                (slave.name, slave.idCard, slave.temp, detail_str, idx))
            lock.release()
            db.commit()
        cursor.close()
        db.close()


    def schedule(self):
        # 各种调度算法
        # self.blowing_list = list(set(self.blowing_list))
        # self.schedule_queue = list(set(self.schedule_queue))

        # 时间片轮转
        # if self.opened_time % 4 == 0:
        #     if self.blowing_list.__len__() > 0:
        #         temp_idx = self.blowing_list[0]
        #         self.blowing_list.remove(temp_idx)
        #         self.schedule_queue.append(temp_idx)

        #         self.slaves[temp_idx]['is_blowing_in'] = False
        #         self.update_cost_and_wind(temp_idx,'5','1','0')

        # print("\033c\n")
        # print("送风队列:",self.blowing_list)
        # print("等待队列:", self.schedule_queue)


        if self.blowing_list.__len__() < 3:
            # 如果存在空余,且有空调等待送风
            if self.schedule_queue.__len__() != 0:
                # 取队首元素加入到送风集合
                idx = self.schedule_queue[0]
                self.schedule_queue.pop(0)
                self.blowing_list.append(idx)
                # 将目标设置为正在送风
                # self.slaves[idx].is_blowing_in = True


    def respond_to_request(self):
        # 这个函数基本没啥用的,懒得去掉了.因为这个去掉了其他也得改
        while not self.request_queue.empty():
            request = self.request_queue.get()
            request()

    def background(self):
        """后台处理"""
        while 1:
            try:
                self.opened_time += 1
                # print(self.opened_time)
                time.sleep(1)
                self.respond_to_request()

                self.schedule()
                self.update_state()

                # 增加送风计时的代码
                # 当修改风速时，重新计时，原来的用来计算那一段的费用
                # 每计时一分钟，也输出一个结果，用来计算费用
                for i in range(self.SLAVE_NUM):
                    power = self.get_slave_power(i)
                    Record = self.get_CheckRecord_Record(i)
                    if Record is not None and power == '1':  # 如果已经入住且当前是开机状态，就计时,并且检查计时状态，进行
                        tim = int(self.get_slave_timer(i))
                        Record = Record[0]
                        # print("slave %d time = %s" %(i, tim))
                        if tim % 60 == 0 and tim != 0:  # 如果当前计满了60s，就更新一次，然后计时器归0
                            print("now time = %s" % (tim))
                            self.update_cost_and_wind(i, '4', '0', '0')
                            self.update_slave_timer(i, 0)
                        else:
                            if self.slaves[i].is_blowing_in == False:
                                self.update_slave_timer(i, 0)
                            else:
                                self.update_slave_timer(i, tim + 1)
            except Exception as e:
                print("********出现了一下错误***********:", e)
                time.sleep(1)
                print("尝试重连")
                self.db.ping(reconnect=True)
                print("重连成功")


# if __name__ == "__main__":
#     master = Master()
#     # print(master.keys())


# 操作记录[当前时间，住房记录号(主键)，操作类型，原来值，请求值，总送风量，总花费]

# 用户所有按钮操作都记录下来：
# 每一分钟就更新一次费用
# 从控机开机时，计时器从0开始
# 从控机关机时，更新费用，状态变为关机，计时器更新的时候发现状态关机，停止计时，
# 修改风速时，计时器导出值，清零开始，更新费用
# 签退时，如果计时器还开着，就关闭计时器，更新费用；如果关了，就不用管了
