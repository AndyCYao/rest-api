from flask import Flask, request as flask_request, Response, abort
from flask_mysqldb import MySQL
import yaml
import datetime
import json
import requests

app = Flask(__name__)
# https://github.com/lalamove/challenge-2018/blob/master/backend.md

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']     = db['mysql_host']
app.config['MYSQL_USER']     = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB']       = db['mysql_db']
app.config['MYSQL_PORT']     = db['mysql_port']
gmap_key                     = db['google_api_key']

mysql = MySQL(app)

def get_km_distance(origin, destination):
    rq = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&key={}'.format(','.join(str(x) for x in origin), 
                                                                                                             ','.join(str(x) for x in destination), gmap_key)
    data = requests.get(rq).json()
    distance = 0
    for element in data["rows"]:
        print(element["elements"][0]["distance"]["value"])
        distance += int(element["elements"][0]["distance"]["value"])
    return distance / 1000

# POST Order
@app.route("/order", methods=['POST'])
def order():
    data         = flask_request.get_json()
    origin       = data['origin']
    destination  = data['destination']
    cur          = mysql.connection.cursor()

    # Calculate google distance here
    try:
        distance = get_km_distance(origin, destination)
        sql = """
            INSERT INTO order_tbl(orig_lat, orig_long, dest_lat, dest_long, 
                                status, distance)
            VALUES({}, {}, {}, {}, 'UNASSIGN', {});
            """.format(origin[0], origin[1], destination[0], destination[1], distance)
        print(sql)
        cur.execute(sql)
        mysql.connection.commit()

        sql = "SELECT LAST_INSERT_ID();"
        cur.execute(sql)
        rv = cur.fetchall()
        payload = {"id": rv[0][0], "distance": distance, "status": "UNASSIGN"}
        cur.close()
        return Response(json.dumps(payload), status = 200, mimetype='application/json')
    except Exception as e:
        return abort(500)

# PUT Order
@app.route("/order/<id>", methods=['PUT'])
def take_order(id):
    data       = flask_request.get_json()
    new_status = data["status"]
    check_sql  = "SELECT status FROM order_tbl WHERE order_id = {}".format(id)
    
    cur = mysql.connection.cursor()
    cur.execute(check_sql)
    rv = cur.fetchall()
    old_status = rv[0][0]

    if old_status is not None and old_status.upper() != "TAKEN":
        update_sql = "UPDATE order_tbl SET status = '{}' WHERE order_id ={}".format(new_status, id)
        print(update_sql)
        cur.execute(update_sql)
        mysql.connection.commit()
        cur.close()
        return Response(json.dumps({"status": "SUCCESS"}), status=200, mimetype='application/json')
    else:
        cur.close()
        return Response(json.dumps({"error": "ORDER_ALREADY_BEEN_TAKEN"}), status=409, mimetype='application/json')



# GET Order List
@app.route("/orders", methods=['GET'])
def get_order_list():
    page    = flask_request.args.get('page')
    limit   = flask_request.args.get('limit')
    cur = mysql.connection.cursor()
    sql = """SELECT order_id, distance, status 
            FROM order_tbl 
            ORDER BY order_id ASC LIMIT {} 
            OFFSET {}""".format(limit, page)
    row_header = ["id", "distance", "status"]
    cur.execute(sql)
    rv = cur.fetchall()
    results = []
    for result in rv:
        results.append(dict(zip(row_header,result)))
    return json.dumps(results)

@app.errorhandler(500)
def internal_error(error):
    return json.dumps({"error": "ERROR_DESCRIPTION"})

@app.errorhandler(400)
def bad_request(error):
    return json.dumps({"error": "BAD_REQUEST"})

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='0.0.0.0', port=8080)