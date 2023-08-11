import os
import configparser
from flask import Flask
from flask import request, jsonify, make_response

# import jsonify
import pyodbc
app = Flask(__name__)




def get_connection_string():
    # Obtainn string from azure environment before local
    azure_db = os.environ.get('DB_CONNECTION_STRING')
    
    if azure_db:
        return azure_db
    
    # Local db string
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    server = config['DATABASE']['server']
    db = config['DATABASE']['db']
    username = config['DATABASE']['user']
    password = config['DATABASE']['password']
    driver = config['DATABASE']['driver']
    port = config['DATABASE']['port']
    
    return f'DRIVER={driver};SERVER={server};PORT={port};DATABASE={db};UID={username};PWD={password}'

def create_connection():
    return pyodbc.connect(get_connection_string())
 
connection = create_connection()



@app.route('/return_foods')
def select_data():
    connection = create_connection()
    cursor = connection.cursor()
    select_query = "SELECT * FROM Foods;"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'food_name': row[1],
            'quantity': row[2],
            'expiry_date': row[3],
            'date_added': row[4]
        })

    connection.close()
    
    print(result)

    # return jsonify(result)

@app.route('/test', methods=['GET'])
def test_route():
    return "Test successful!"

print(test_route())
select_data()
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5002, debug=True)

# testingh