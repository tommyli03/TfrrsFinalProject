import mysql.connector
from mysql.connector import Error
from bs4 import BeautifulSoup
import requests

DB_CONFIG = {
    'host': 'tfrrs-database.cvyguqokm3xa.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': 'andrewtommydatabases',
    'database': 'tfrrs_data'
}

def connect_db():
    """Connect to MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✅ Successfully connected to the database.")
            return conn
    except Error as e:
        print(f"❌ Error: {e}")
        exit()

def get_athletes(conn):
    """Fetch distinct athlete_name, team, athlete_url from outdoor_qualifying_results."""
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT DISTINCT athlete_name, team, athlete_url
        FROM outdoor_qualifying_results
        WHERE athlete_url IS NOT NULL AND athlete_url != ''
    """
    cursor.execute(query)
    athletes = cursor.fetchall()
    cursor.close()
    return athletes

def insert_athlete_record(conn, athlete_name, team, athlete_url, event, performance):
    """Insert or update a single PR record into the Athlete table."""
    cursor = conn.cursor()
    query = """
        INSERT INTO Athlete (athlete_name, team, athlete_url, event, performance)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          performance=VALUES(performance);
    """
    cursor.execute(query, (athlete_name, team, athlete_url, event, performance))
    conn.commit()
    cursor.close()

def parse_athlete_page(html):
    """
    Parse the athlete page HTML to extract PR events and performances (no wind).
    """
    soup = BeautifulSoup(html, 'html.parser')
    bests_table = soup.find('table', id='all_bests')
    if not bests_table:
        return []

    pr_data = []
    rows = bests_table.find_all('tr')
    for row in rows:
        cells = row.find_all('td', recursive=False)
        if len(cells) < 4:
            continue

        # Left event & performance
        event_left = cells[0].get_text(strip=True)
        perf_left_a = cells[1].find('a')
        if perf_left_a:
            performance_left = perf_left_a.get_text(strip=True)
            if event_left and performance_left:
                pr_data.append((event_left, performance_left))

        # Right event & performance
        event_right = cells[2].get_text(strip=True)
        perf_right_a = cells[3].find('a')
        if perf_right_a:
            performance_right = perf_right_a.get_text(strip=True)
            if event_right and performance_right:
                pr_data.append((event_right, performance_right))

    return pr_data

def main():
    conn = connect_db()
    athletes = get_athletes(conn)

    total_athletes = len(athletes)
    half_count = total_athletes // 2
    # Partner will process the second half
    athletes_to_process = athletes[half_count:]

    print(f"Found {total_athletes} athletes in total. Processing last {total_athletes - half_count} athletes...")

    for i, athlete in enumerate(athletes_to_process, start=1):
        athlete_name = athlete['athlete_name']
        team = athlete['team']
        athlete_url = athlete['athlete_url']

        # Print a status update every 500 athletes
        if i % 500 == 0:
            print(f"Processed {i} athletes so far in the second half...")

        if not athlete_url:
            continue

        try:
            response = requests.get(athlete_url, timeout=10)
            response.raise_for_status()
            html = response.text
        except Exception:
            continue

        prs = parse_athlete_page(html)

        # Insert/update each PR into Athlete table
        for event, performance in prs:
            insert_athlete_record(conn, athlete_name, team, athlete_url, event, performance)

    conn.close()
    print("✅ Done processing the second half of the athletes.")

if __name__ == "__main__":
    main()
