import os
import configparser
from flask import Flask
from flask import request, jsonify, make_response

import pyodbc
app = Flask(__name__)




def get_connection_string():
    # Obtainn string from azure environment before local
    azure_db = os.environ.get('DB_CONNECTION_STRING')
    
    if azure_db:
        print("azure db registered")
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

    # response = make_response(jsonify(result))
    # response.headers['x-content-type-options'] = 'nosniff'
    
    return result

# @app.route('/return_foods_python')
# def select_data2():
#     # Here, I'm assuming another service provides the food data.
#     response = requests.get("https:/40268037selectfood.azurewebsites.net/return_foods")
    
#     if response.status_code == 200:
#         return jsonify(response.json())
#     else:
#         return "error"
    
    
@app.route('/test', methods=['GET'])
def test_route():
    return "Test successful!"

print(test_route())
select_data()
# select_data2()
if __name__ == "__main__":
    app.run()

# testingh