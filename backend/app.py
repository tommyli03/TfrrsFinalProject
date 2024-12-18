from flask import Flask, request, jsonify
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
    year = request.args.get('year')  # Get 'year' from query parameters
    query = "SELECT * FROM top_performers"
    if year:
        query += " WHERE race_year = %s ORDER BY race_year DESC, CAST(place AS UNSIGNED) ASC"
    else:
        query += " ORDER BY race_year DESC, CAST(place AS UNSIGNED) ASC"

    with connection.cursor() as cursor:
        cursor.execute(query, (year,) if year else None)
        data = cursor.fetchall()
        print(data)
    connection.close()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
