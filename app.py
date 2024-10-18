from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Adnan@123'
app.config['MYSQL_DB'] = 'clients_db'

# Connect to MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    

@app.route('/', methods=['GET'])
def home():
    return 'server started'

@app.route('/getClients', methods=['GET'])
def get_clients():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = connection.cursor()
        # Updated SQL query based on your provided query
        query = """
        SELECT 
            p.PTY_ID, 
            p.PTY_FirstName, 
            p.PTY_LastName, 
            p.PTY_Phone, 
            p.PTY_SSN, 
            a.Add_ID, 
            a.Add_Line1, 
            a.Add_City, 
            a.Add_Zip, 
            s.Stt_Name AS Add_State
        FROM 
            OPT_Party p
        LEFT JOIN 
            OPT_Address a ON p.PTY_ID = a.Add_PartyID
        LEFT JOIN 
            SYS_State s ON a.Add_State = s.Stt_ID
        """
        cursor.execute(query)
        clients = cursor.fetchall()

        # Constructing JSON response
        json_result = [
            {
                'partyID': row[0],
                'firstName': row[1],
                'lastName': row[2],
                'phone': row[3],
                'ssn': row[4],  # Handle this with caution due to sensitivity
                'addressID': row[5],
                'addressLine1': row[6],
                'city': row[7],
                'zipCode': row[8],
                'state': row[9]
            } for row in clients
        ]
    except Error as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Failed to retrieve data"}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(json_result)

if __name__ == '__main__':
    app.run(debug=True)
