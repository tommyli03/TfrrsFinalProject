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
    """Insert a single PR record into the Athlete table."""
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
    Parse the athlete page HTML to extract PR events and performances.
    Wind data is ignored as per the request.
    """
    soup = BeautifulSoup(html, 'html.parser')
    bests_table = soup.find('table', id='all_bests')
    if not bests_table:
        return []

    pr_data = []
    rows = bests_table.find_all('tr')
    for row in rows:
        cells = row.find_all('td', recursive=False)
        # Typically, 4 <td>s per row: event_left, perf_left, event_right, perf_right
        if len(cells) < 4:
            continue

        # Left event & performance
        event_left = cells[0].get_text(strip=True)
        perf_left_td = cells[1]
        perf_left_a = perf_left_td.find('a')
        if perf_left_a:
            performance_left = perf_left_a.get_text(strip=True)
            if event_left and performance_left:
                pr_data.append((event_left, performance_left))

        # Right event & performance
        event_right = cells[2].get_text(strip=True)
        perf_right_td = cells[3]
        perf_right_a = perf_right_td.find('a')
        if perf_right_a:
            performance_right = perf_right_a.get_text(strip=True)
            if event_right and performance_right:
                pr_data.append((event_right, performance_right))

    return pr_data

def main():
    conn = connect_db()
    athletes = get_athletes(conn)

    total_athletes = len(athletes)
    print(f"Found {total_athletes} athletes.")

    for i, athlete in enumerate(athletes, start=1):
        athlete_name = athlete['athlete_name']
        team = athlete['team']
        athlete_url = athlete['athlete_url']

        if not athlete_url:
            continue

        # Print progress every 500 athletes
        if i % 500 == 0:
            print(f"Processed {i} athletes...")

        # Fetch athlete page HTML
        try:
            response = requests.get(athlete_url, timeout=10)
            response.raise_for_status()
            html = response.text
        except Exception:
            # If we can't fetch this athlete's page, just continue to the next
            continue

        # Parse PR data
        prs = parse_athlete_page(html)

        # Insert each PR into Athlete table (no wind field)
        for event, performance in prs:
            insert_athlete_record(conn, athlete_name, team, athlete_url, event, performance)

    conn.close()
    print("✅ Done processing all athletes.")

if __name__ == "__main__":
    main()
