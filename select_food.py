from flask import Flask
from flask import request, jsonify, make_response

# import jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://40268037flaskfrontend.azurewebsites.net", "Allow Headers": "*"}})



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
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    
    return response

        
if __name__ == '__main__': 
    app.run(debug=True)


# testingh