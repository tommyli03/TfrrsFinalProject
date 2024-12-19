import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ----------------------------
# Database Configuration
# ----------------------------
DB_CONFIG = {
    'host': 'tfrrs-database.cvyguqokm3xa.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': 'andrewtommydatabases',
    'database': 'tfrrs_data'
}

# ----------------------------
# Scraping Configuration
# ----------------------------
URL = "https://tf.tfrrs.org/lists/4517/2024_NCAA_Division_III_Outdoor_Qualifying_FINAL"
#URL = "https://www.tfrrs.org/lists/4043/2023_NCAA_Division_III_Outdoor_Qualifying_FINAL"
#URL = " https://www.tfrrs.org/lists/3714/2022_NCAA_Division_III_Outdoor_Qualifying_FINAL"
#URL = "https://tf.tfrrs.org/lists/3195/2021_NCAA_Division_III_Outdoor_Qualifying_FINAL"
#URL = "https://tfrrs.org/lists/2572/2019_NCAA_Div_III_Outdoor_Qualifying_FINAL"

def connect_db():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Successfully connected to the database.")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        exit()

def insert_to_db(dataframe, table_name):
    """Insert the scraped data into MySQL."""
    conn = connect_db()
    cursor = conn.cursor()

    query = f"""
        INSERT INTO {table_name}
        (year, season, event, place, athlete_name, athlete_url, athlete_year, team, time_str, meet, meet_date, wind)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in dataframe.iterrows():
        values = (
            row['Year'], 'Outdoor', row['Event'], row['Rank'], row['Athlete'], row['Athlete_URL'],
            row['Class'], row['School'], row['Performance'], row['Meet'], row['Meet Date'], row.get('Wind', 'N/A')
        )
        cursor.execute(query, values)

    conn.commit()
    print(f"✅ Inserted {cursor.rowcount} rows into {table_name}.")
    cursor.close()
    conn.close()

def scrape_top_500(year):
    """Scrape NCAA Outdoor Qualifying Results for men, setting top 500 globally."""
    print("🚀 Starting scrape for NCAA Outdoor Results (Men)...")
    driver = webdriver.Chrome()
    driver.get(URL + "?gender=m")
    wait = WebDriverWait(driver, 30)

    data = []

    try:
        # Wait for page to load the dropdown
        limit_dropdown = wait.until(EC.presence_of_element_located((By.ID, "limit")))
        # Select "Top 500" globally
        Select(limit_dropdown).select_by_value("500")
        print("✅ Selected Top 500 globally.")
        time.sleep(5)

        # Once top 500 is selected, all events should now show up to 500 rows
        # Wait for the gender-specific events to load (they may reload after changing the limit)
        event_sections = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.gender_m')))
        print(f"📌 Found {len(event_sections)} event sections to scrape.")

        for event_section in event_sections:
            try:
                event_name = event_section.find_element(By.CSS_SELECTOR, 'div.custom-table-title h3.font-weight-500').text.strip()
                print(f"📌 Scraping Event: {event_name}")

                # Scroll to this event to ensure visibility and let rows load
                driver.execute_script("arguments[0].scrollIntoView();", event_section)
                time.sleep(3)

                # Extract all rows for this event
                rows = event_section.find_elements(By.CSS_SELECTOR, 'tr.allRows')
                print(f"✅ Found {len(rows)} rows for event: {event_name}.")

                # Parse row data
                for row in rows:
                    try:
                        cols = row.find_elements(By.TAG_NAME, 'td')
                        if len(cols) >= 5:
                            athlete_element = cols[1].find_element(By.TAG_NAME, 'a') if cols[1].find_elements(By.TAG_NAME, 'a') else None
                            athlete_name = athlete_element.text.strip() if athlete_element else "N/A"
                            athlete_url = athlete_element.get_attribute('href') if athlete_element else "N/A"

                            data.append({
                                'Year': year,
                                'Event': event_name,
                                'Rank': cols[0].text.strip() if len(cols) > 0 else "N/A",
                                'Athlete': athlete_name,
                                'Athlete_URL': athlete_url,
                                'Class': cols[2].text.strip() if len(cols) > 2 else "N/A",
                                'School': cols[3].text.strip() if len(cols) > 3 else "N/A",
                                'Performance': cols[4].text.strip() if len(cols) > 4 else "N/A",
                                'Meet': cols[5].text.strip() if len(cols) > 5 else "N/A",
                                'Meet Date': cols[6].text.strip() if len(cols) > 6 else "N/A",
                                'Wind': cols[7].text.strip() if len(cols) > 7 else None
                            })
                        else:
                            print("⚠️ Skipped a row due to insufficient columns.")
                    except Exception as e:
                        print(f"❌ Error processing row in event {event_name}: {e}")
                        continue

            except Exception as e:
                print(f"❌ Error processing event: {e}")
                continue

        print(f"✅ Scraped {len(data)} rows total for all events (Men).")
        return pd.DataFrame(data)

    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()

    finally:
        driver.quit()


# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    print("🚀 Starting the NCAA Outdoor Results Scraper...")

    # Scrape data for Men
    men_data = scrape_top_500(2024)

    # Insert into the database
    if not men_data.empty:
        print("📤 Inserting data into MySQL database...")
        insert_to_db(men_data, 'outdoor_qualifying_results')
        print("🎉 Data successfully inserted into the database.")
    else:
        print("❌ No data was scraped. Check website structure or script.")

    print("✅ Scraping process completed.")