import pymysql
from app import app
from config import mysql
from flask import jsonify, request

@app.route('/select')
def select():
    try:
        name = request.args.get('name')
        age = request.args.get('age')
        gender = request.args.get('gender')

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM user WHERE 1=1"
        args = []

        if name:
            sqlQuery += " AND name LIKE %s"
            args.append("%" + name + "%")
        if age:
            sqlQuery += " AND age = %s"
            args.append(age)
        if gender:
            sqlQuery += " AND gender = %s"
            args.append(gender)
        
        cursor.execute(sqlQuery, args)
        userRows = cursor.fetchall()
        
        response = jsonify(userRows)
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/create', methods=['POST'])
def create():
    try:
        req = request.get_json()

        name = req['params']['name']
        age = req['params']['age']
        gender = req['params']['gender']

        if name and age and gender and request.method == 'POST':
            sqlQuery = "INSERT INTO user (name, age, gender) VALUES (%s, %s, %s)"
            bindData = (name, age, gender)

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            response = jsonify("success")
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update', methods=['PUT'])
def update():
    try:
        id = request.json['id']
        name = request.json['name']
        age = request.json['age']
        gender = request.json['gender']

        if name and age and gender and request.method == 'PUT':
            sqlQuery = "UPDATE user SET name=%s, age=%s, gender=%s WHERE id=%s"
            bindData = (name, age, gender, id)

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            response = jsonify("User updated successfully.")
            response.status_code = 200
            return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/delete', methods=['DELETE'])
def delete():
    try:
        id = request.json['id']

        if id and request.method == 'DELETE':
            sqlQuery = "DELETE FROM user WHERE id=%s"
            bindData = (id)

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()

            response = jsonify("User deleted successfully.")
            response.status_code = 200
            return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Resource not found: ' + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')