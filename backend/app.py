from flask import Flask, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL database configuration
DB_HOST = 'tfrrs-database.cvyguqokm3xa.us-east-2.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASS = 'andrewtommydatabases' #replace with your own password
DB_NAME = 'tfrrs_data'

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/top_performers', methods=['GET'])
def top_performers():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM top_performers ORDER BY race_year DESC, CAST(place AS UNSIGNED) ASC;")
        data = cursor.fetchall()
        print(data)
    connection.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
