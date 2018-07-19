from flask import Flask, request
from flask_mysqldb import MySQL
import yaml
import datetime
import json

DEBUG = True 
app = Flask(__name__)
# https://github.com/lalamove/challenge-2018/blob/master/backend.md

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']     = db['mysql_host']
app.config['MYSQL_USER']     = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB']       = db['mysql_db']

mysql = MySQL(app)

@app.route("/")
def index():
    return "You're at home page"

# POST Order
@app.route("/order", methods=['POST'])
def order():
    origin       = json.loads(request.args.get('origin'))
    destination  = json.loads(request.args.get('destination'))
    print(origin)
    print(destination)
    cur = mysql.connection.cursor()

    sql = """
        INSERT INTO order_tbl(orig_lat, orig_long, dest_lat, dest_long, 
                              isTaken, distance)
        VALUES({}, {}, {}, {}, {}, {}, {})
        """.format(origin[0], origin[1], destination[0], destination[1], False, 1000)
    print(sql)
    cur.execute(sql)
    mysql.connection.commit()
    cur.close()
    return "youre at order page you sent id {} origin {} destination {}".format(id, origin, destination)


# PUT Order
@app.route("/order/<id>", methods=['PUT'])
def take_order(id):
    #id = request.args.get('id')
    return "taking order {}".format(id)

# GET Order List
@app.route("/orders", methods=['GET'])
def get_order_list():
    page =  request.args.get('page')
    limit = request.args.get('limit')
    return "taking order page = {} limit = {}".format(page, limit) 


if __name__ == "__main__":
    app.run(debug=True)