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

@app.route('/xc_nationals_results', methods=['GET'])
def xc_nationals_results():
    year = request.args.get('year')
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT *
            FROM xc_nationals_results
            WHERE race_year = %s
            ORDER BY 
                CASE WHEN CAST(place AS UNSIGNED) = 0 THEN 1 ELSE 0 END, 
                CAST(place AS UNSIGNED) ASC;
        """, (year,))
        data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/team_rankings', methods=['GET'])
def team_rankings():
    year = request.args.get('year')  # Get the 'year' parameter from the request
    query = """
        SELECT *
        FROM xc_team_rankings
        WHERE race_year = %s
        ORDER BY team_rank ASC;
    """ if year != 'None' else """
        SELECT *
        FROM xc_team_rankings
        ORDER BY race_year DESC, team_rank ASC;
    """
    connection = get_connection()
    with connection.cursor() as cursor:
        if year != 'None':
            cursor.execute(query, (year,))
        else:
            cursor.execute(query)
        data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/xc_2024_5k_analysis', methods=['GET'])
def xc_2024_5k_analysis():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                team, 
                meet_rank, 
                avg_5k_time_mm_ss, 
                team_5k_rank 
            FROM xc_2024_5k_analysis 
            ORDER BY team_5k_rank;
        """)
        data = cursor.fetchall()
    connection.close()
    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True)
