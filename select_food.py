from flask import Flask
from flask import request, jsonify

# import jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://40268037flaskfrontend.azurewebsites.net"}})


dpp = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://40268037flaskfrontend.azurewebsites.net"}})

def get_connection_string():
    # ... [rest of the function remains the same]

def create_connection():
    return pyodbc.connect(get_connection_string())

@app.route('/return_foods', methods=['GET'])
def select_data():
    connection = create_connection()
    cursor = connection.cursor()
    select_query = "SELECT * FROM Foods;"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    result = []
    for row in rows:
       result.append({'food_name': row[1], 'quantity': row[2], 'expiry_date': row[3], 'date_added': row[4]})

    connection.commit()
    connection.close()
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
        
if __name__ == '__main__': 
    app.run(debug=True)


# testingh