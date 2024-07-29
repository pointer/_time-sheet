# You can change this to the country you need
from workalendar.europe import France
from datetime import date, datetime
import os
import hashlib
import asyncio
import websockets  # Add this import
from websockets.server import serve
import json
import sqlite3
from datetime import datetime, timedelta
import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import random
import calendar
from calendar import monthrange
from websocket_server import WebsocketServer

# Called for every client connecting (after handshake)

PEPPER = "SECRET_KEY"


def create_secure_password(password):
    salt = os.urandom(16)
    iterations = 100_000
    hash_value = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8') + PEPPER.encode('utf-8'),
        salt,
        iterations
    )
    password_hash = salt + hash_value
    return password_hash


# print(create_secure_password("HelloWorld"))


def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))


# PORT = 9001
# server = WebsocketServer(port=PORT)
# server.set_fn_new_client(new_client)
# server.set_fn_client_left(client_left)
# server.set_fn_message_received(message_received)
# server.run_forever()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("open success")
        # timer that sends data to the front end once per second
        self.timer = tornado.ioloop.PeriodicCallback(self.send_data, 1000)
        self.timer.start()

    def on_close(self):
        self.timer.stop()

    def send_data(self):
        # send the current time to the front end
        self.write_message('Now is' + str(time.time()))


# application = tornado.web.Application([
#     (r'/', WebSocketHandler),
# ])

# if __name__ == '__main__':
#     application.listen(3001)
#     tornado.ioloop.IOLoop.instance().start()

# Connect to SQLite database
conn = sqlite3.connect('effort-tracking.db')
cursor = conn.cursor()


# def calculate_working_days(year, month, country):
def calculate_working_days() -> int:
    # Initialize the calendar for the desired country
    cal = France()
    today = datetime.today()
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year

    num_days = calendar.monthrange(current_year, current_month)[1]
    print(">>>>>>>>>>>", current_year, current_month, num_days)
    # Define the start and end dates
    start_date = date(current_year, current_month, 1)
    end_date = date(current_year, current_month, num_days)
    # start_date = date(2024, 8, 1)
    # end_date = date(2024, 8, num_days)
    # Calculate the number of working days
    working_days = cal.get_working_days_delta(start_date, end_date)

    # print(f"Number of working days: {working_days}")
    return working_days


# def calculate_working_days(year, month, country):
    # Placeholder implementation, replace with actual logic based on country regulations
    # wdim2022 = [get_wdim(year, month) for month in list(range(1, 13))]
    # now = datetime.datetime.now()

    # cal = calendar.Calendar()

    # working_days = len([x for x in cal.itermonthdays2(now.year, now.month) if x[0] !=0 and x[1] < 5])

    # print( "Total working days this month: " + str(working_days)    )
    # # weekday_count = 0
    # cal = calendar.Calendar()

    # for week in cal.monthdayscalendar(year, 8):
    #     for i, day in enumerate(week):
    #         # not this month's day or a weekend
    #         if day == 0 or i >= 5:
    #             continue
    #         # or some other control if desired...
    #         weekday_count += 1

    # print( weekday_count)
    # start_date = datetime(year, month, 1)
    # end_date = (start_da
    #             te + timedelta(days=32)
    #             ).replace(day=1) - timedelta(days=1)
    # working_days = 0
    # current_date = start_date

    # while current_date <= end_date:
    #     if current_date.weekday() < 5:  # Monday to Friday are considered working days
    #         working_days += 1
    #     current_date += timedelta(days=1)

    # return working_days


def get_wdim(year, month):
    cal = calendar.Calendar()
    working_days = len([x for x in cal.itermonthdays2(
        year, month) if x[0] != 0 and x[1] < 5])
    holidays = {
        1: 1,
        2: 1,
        4: 1,
        5: 1,
        7: 1,
        9: 1,
        10: 1,
        11: 4,
        12: 1
    }
    return int(working_days) - holidays.get(month, 0)


async def handler(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "login":
                user_name = data.get("user_name")
                password = data.get("password")

                # Query the database for the user
                cursor.execute('''
                SELECT account.role, account.account_id FROM account WHERE user_name = ? AND password = ?
                ''', (user_name, password))
                # cursor.execute('''
                # SELECT role.role_name, user.user_name FROM user
                # JOIN role ON user.role_id = role.role_id
                # WHERE user_name = ? AND password = ?
                # ''', (user_name, password))
                user = cursor.fetchone()

                if user:
                    working_days = calculate_working_days()
                    response = {"success": True, "working_days": working_days, "user": {
                        "role": user[0], "user_id": user[1]}}
                else:
                    response = {"success": False}

                await websocket.send(json.dumps(response))

            elif action == "submit_timesheet":
                user_id = data.get("user_id")
                date = data.get("date")
                month = data.get("month")
                worked = data.get("worked")

                # Calculate working days
                working_days = calculate_working_days()
                projects = ['STLA', 'POC-BMW', 'DCROSS']
                project = random.choice(projects)
                # Insert timesheet data into the database
                cursor.execute('''
                INSERT INTO timesheet (account_id, date, month, project, worked)
                VALUES (?, ?, ?, ?, ?)
                ''', (user_id, date, month, project, worked))
                conn.commit()

                response = {"success": True}
                await websocket.send(json.dumps(response))

            elif action == "approve_timesheet":
                timesheet_id = data.get("timesheet_id")
                supervisor_id = data.get("supervisor_id")
                approved = data.get("approved")
                approval_date = data.get("approval_date")
                # month = data.get("month")

                # Insert approval data into the database
                cursor.execute('''
                INSERT INTO timesheet_approval (timesheet_id, supervisor_id, approved, approval_date)
                VALUES (?, ?, ?, ?)
                ''', (timesheet_id, supervisor_id, approved, approval_date))
                conn.commit()

                response = {"success": True}
                await websocket.send(json.dumps(response))

            elif action == "update_user_data":
                user_data = data.get("user_data")

                # Insert or update user data into the database
                cursor.execute('''
                INSERT INTO user_data (user_id, first_name, last_name, phone, email, role, contract_number, company, tax_number, client, city, date_start, date_end, rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    first_name=excluded.first_name,
                    last_name=excluded.last_name,
                    phone=excluded.phone,
                    email=excluded.email,
                    role=excluded.role,
                    contract_number=excluded.contract_number,
                    company=excluded.company,
                    tax_number=excluded.tax_number,
                    client=excluded.client,
                    city=excluded.city,
                    date_start=excluded.date_start,
                    date_end=excluded.date_end,
                    rate=excluded.rate
                ''', (
                    user_data["user_id"], user_data["first_name"], user_data["last_name"], user_data["phone"], user_data["email"], user_data["role"], user_data["contract_number"], user_data[
                        "company"], user_data["tax_number"], user_data["client"], user_data["city"], user_data["date_start"], user_data["date_end"], user_data["rate"]
                ))
                conn.commit()

                response = {"success": True}
                await websocket.send(json.dumps(response))

            elif action == "fetch_timesheet":
                month = data.get("month")
                approved = False
                # SELECT * FROM timesheet where month = ? ''', (month,))
                cursor.execute('''
                SELECT timesheet.timesheet_id, timesheet.account_id, timesheet.date, timesheet.month,
                timesheet.project, timesheet.worked, account.first_name, account.last_name FROM timesheet
                LEFT JOIN account ON timesheet.account_id = account.account_id
                where month = ? ''', (month,))
                timesheets = cursor.fetchall()
                response = {"success": True, "timesheets": timesheets}
                await websocket.send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed as e:
        print(f'Closed OK: {e}')
    except Exception as e:
        print(f'unexpected exception: {e}')
    finally:
        print(f'connected')


async def main():
    async with serve(handler, "localhost", 8765):
        print(">>>>>> Bienvenue à bord\n>>>>>> Server listening @ localhost:8765")
        await asyncio.get_running_loop().create_future()  # run forever
if __name__ == "__main__":
    asyncio.run(main())
