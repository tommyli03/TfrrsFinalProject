import time
import requests
from bs4 import BeautifulSoup
import pymysql
import re
# ----------------------------
# MySQL database configuration
# ----------------------------
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = 'Hhhmddyjuietmn4ae33$' #replace with your own password
DB_NAME = 'tfrrs_data'

# Connect to MySQL (adjust as needed)
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_soup(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, 'html.parser')

def insert_track_result(year, season, event, place, athlete_name, athlete_year, team, time_str, meet, meet_date, wind):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO outdoor_qualifying_results 
        (year, season, event, place, athlete_name, athlete_year, team, time_str, meet, meet_date, wind)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (year, season, event, place, athlete_name, athlete_year, team, time_str, meet, meet_date, wind))
    connection.commit()

def insert_xc_result(year, place, name, athlete_year, team, avg_mile, time_str, score, athlete_url, fastest_5k = None):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO xc_nationals_results
        (race_year, place, athlete_name, athlete_year, team, avg_mile, time_str, score, athlete_url, fastest_5k)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (year, place, name, athlete_year, team, avg_mile, time_str, score, athlete_url, fastest_5k))
    connection.commit()




# ----------------------------
# Scrape Outdoor Qualifying Data
# Example: 2024 Qualifying page
# URL: https://tf.tfrrs.org/lists/4517/2024_NCAA_Division_III_Outdoor_Qualifying_FINAL
# ----------------------------

# The events you want:
TRACK_EVENTS = ["100", "200", "400", "800", "1500", "5000", "10000", "110H", "400H", "3000S"]

def scrape_outdoor_qualifying(year, url):
    soup = get_soup(url)
    print('here')
    # Find all event divs. 
    # Your snippet shows multiple event divs like <div id="event0" name="event0" ...>, <div id="event1" ...>
    # We’ll search by a pattern. If the ID structure differs, adjust accordingly.
    event_divs = soup.find_all("div", id=lambda x: x and x.startswith("event"))

    for event_div in event_divs:
        event_id = event_div.get("id", "")
        
        # Attempt to find event name. 
        # Possibly a nearby element with class "custom-table-title"
        # If not present, you may know the mapping beforehand or print event_div and inspect.
        event_title_div = event_div.find("div", class_="custom-table-title")
        if event_title_div:
            event_name = event_title_div.get_text(strip=True)
        else:
            event_name = event_id  # fallback if event title not found

        # Find the table within this event_div
        # The table may have id like "myTable6" and classes including "tablesorter".
        # You can be more specific if needed:
        table = event_div.find("table", class_="tablesorter")
        if not table:
            continue

        # Find tbody with class "body"
        tbody = table.find("tbody", class_="body")
        if not tbody:
            continue

        rows = tbody.find_all("tr", class_="allRows")
        # Limit to top 500
        rows = rows[:500]
        for row in rows:
            cols = row.find_all("td")
            # The expected column order based on previous assumptions:
            # 0: &nbsp; (Place)
            # 1: Athlete
            # 2: Year
            # 3: Team
            # 4: Time
            # 5: Meet
            # 6: Meet Date
            # 7: Wind (optional)
            
            if len(cols) < 8:
                # Not a valid row?
                continue

            place_col = cols[0].get_text(strip=True)
            athlete_col = cols[1].get_text(strip=True)
            athlete_year_col = cols[2].get_text(strip=True)
            team_col = cols[3].get_text(strip=True)
            time_col = cols[4].get_text(strip=True)
            meet_col = cols[5].get_text(strip=True)
            meet_date_col = cols[6].get_text(strip=True)
            wind_col = cols[7].get_text(strip=True) if len(cols) > 7 else ""

            # Insert into DB
            insert_track_result(year, "Outdoor", event_name, place_col, athlete_col, athlete_year_col, team_col, time_col, meet_col, meet_date_col, wind_col)

        # Be polite to the server
        time.sleep(1)

# ----------------------------
# Scrape Cross Country Nationals
# Example: 2024 XC Championships URL
# URL: https://www.tfrrs.org/results/xc/25327/NCAA_Division_III_Cross_Country_Championships#event162754
# ----------------------------
def scrape_xc_nationals(year_of_meet, url):
    soup = get_soup(url)

    # Step 1: Find the <h3> heading that contains "Individual Results"
    # Find the first <h3> containing "Individual Results"
    h3_heading = soup.find('h3', class_='font-weight-500', string=re.compile(r'Individual Results', re.IGNORECASE))

# Locate the table immediately after the <h3> tag
    if h3_heading:
        table = h3_heading.find_next('table', class_='tablesaw tablesaw-xc table-striped table-bordered table-hover')
    else:
        print("Heading not found! Defaulting to the second table.")
        tables = soup.find_all('table', class_='tablesaw tablesaw-xc table-striped table-bordered table-hover')
        table = tables[1] if len(tables) > 1 else None


    # Step 2: From the heading, find the next sibling table
    # table = h3_heading.find_next('table', class_='tablesaw tablesaw-xc table-striped table-bordered table-hover')
    # if not table:
    #     print("Individual Results table not found!")
    #     return

    # Table body
    tbody = table.find("tbody", class_="color-xc")
    if not tbody:
        print("Table body not found!")
        return

    rows = tbody.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 7:  # Ensure we have enough columns
            continue
        
        # Extract the relevant data
        place = cols[0].get_text(strip=True)
        print(place)
        # Name and athlete profile URL
        name_col = cols[1]
        name = name_col.get_text(strip=True)
        athlete_url = None
        a_tag = name_col.find("a", href=True)
        if a_tag:
            athlete_url = a_tag["href"]
            if athlete_url.startswith("/"):
                athlete_url = "https://www.tfrrs.org" + athlete_url
        
        athlete_year = cols[2].get_text(strip=True)
        team = cols[3].get_text(strip=True)
        avg_mile = cols[4].get_text(strip=True)
        time_str = cols[5].get_text(strip=True)
        score = cols[6].get_text(strip=True)

        # Optional: Scrape the athlete's fastest 5k from their profile page
        fastest_5k = None
        if athlete_url:
            fastest_5k = scrape_athlete_fastest_5k(athlete_url)

        # Insert the scraped data into the database
        insert_xc_result(year_of_meet, place, name, athlete_year, team, avg_mile, time_str, score, athlete_url, fastest_5k)

    print("XC Nationals Results Scraped Successfully!")



import re

def scrape_athlete_fastest_5k(athlete_url):
    print(f"Scraping 5k time from: {athlete_url}")  # Debug message

    soup = get_soup(athlete_url)

    # Tables to check (only track tables)
    # "all_bests" may contain track times from any season type
    # "indoor_bests" for indoor track
    # "outdoor_bests" for outdoor track
    table_ids = ["all_bests"]
    table_classes = ["indoor_bests", "outdoor_bests"]
    valid_event_name = "5000"

    all_times = []

    # Check #all_bests by ID
    all_bests_table = soup.find("table", id="all_bests")
    if all_bests_table:
        times = find_5k_in_table(all_bests_table, valid_event_name)
        all_times.extend(times)

    # Check indoor_bests and outdoor_bests
    for cls in table_classes:
        tbl = soup.find("table", class_=cls)
        if tbl:
            times = find_5k_in_table(tbl, valid_event_name)
            all_times.extend(times)

    if not all_times:
        print(f"No track 5000 time found for {athlete_url}")
        return None

    # Determine the fastest time
    fastest_time = min(all_times, key=time_to_seconds)
    print(f"Fastest 5000 time for {athlete_url} is {fastest_time}")
    return fastest_time

def find_5k_in_table(table, valid_event_name):
    """Searches a given table for '5000' event and returns a list of all found times."""
    rows = table.find_all("tr")
    found_times = []
    for row in rows:
        # Each row likely has up to 4 <td> elements for two events: 
        # [eventTd, timeTd, eventTd, timeTd]
        td_list = row.find_all("td", class_=re.compile("panel-heading-(text|normal-text)"))
        # Iterate in steps of 2 to pair event and time
        for i in range(0, len(td_list), 2):
            if i+1 < len(td_list):
                event_td = td_list[i]
                time_td = td_list[i+1]

                event_name = event_td.get_text(strip=True).upper()
                if event_name == "5000":
                    # Extract time from time_td
                    a_tag = time_td.find("a")
                    if a_tag:
                        time_str = a_tag.get_text(strip=True)
                        # Store it
                        found_times.append(time_str)
    return found_times

def time_to_seconds(t):
    """Convert a time string MM:SS.xx or M:SS.xx to seconds for comparison."""
    # Split by ':'
    parts = t.split(':')
    if len(parts) == 2:
        # Format: MM:SS.xx or M:SS.xx
        try:
            minutes = float(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        except ValueError:
            return float('inf')  # invalid time
    else:
        # Unexpected format
        return float('inf')


def is_faster(time_a, time_b):
    # Convert times to a comparable measure (seconds) and compare
    def time_to_seconds(t):
        # handle possible formats (e.g. "14:30.00" = 14min 30.00s)
        parts = t.split(':')
        if len(parts) == 2:
            min_part = float(parts[0])
            sec_part = float(parts[1])
            return min_part * 60 + sec_part
        else:
            # Unexpected format
            return None

    a_sec = time_to_seconds(time_a)
    b_sec = time_to_seconds(time_b)
    if a_sec is None or b_sec is None:
        return False
    return a_sec < b_sec


# ----------------------------
# Running the Scrapers
# ----------------------------
if __name__ == "__main__":
    # Example: Scrape 2024 Outdoor Qualifying
    outdoor_url_2024 = "https://tf.tfrrs.org/lists/4517/2024_NCAA_Division_III_Outdoor_Qualifying_FINAL"
    scrape_outdoor_qualifying(2024, outdoor_url_2024)

    # Example: Scrape 2024 XC Nationals
    # You'll need the URL for each year’s NCAA DIII XC Championship from 2015-2024.
    # For now, just 2024 as given:
    xc_url_2024 = "https://www.tfrrs.org/results/xc/25327/NCAA_Division_III_Cross_Country_Championships#event162754"
    scrape_xc_nationals(2024, xc_url_2024)

    # For other years, once you have their URLs, do something like:
    # xc_urls = {
    #   2015: "https://www.tfrrs.org/results/xc/xxxx/NCAA_Division_III_Cross_Country_Championships",
    #   2016: "...",
    #   ...
    #   2024: "https://www.tfrrs.org/results/xc/25327/NCAA_Division_III_Cross_Country_Championships"
    # }
    # for yr, u in xc_urls.items():
    #     scrape_xc_nationals(yr, u)

    connection.close()
