# TfrrsFinalProject
- Ignore this for right now:

CREATE TABLE xc_nationals_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    race_year INT NOT NULL,
    place VARCHAR(10),
    athlete_name VARCHAR(100),
    athlete_year VARCHAR(20),
    team VARCHAR(100),
    avg_mile VARCHAR(20),
    time_str VARCHAR(20),
    score VARCHAR(10),
    athlete_url VARCHAR(255),
    fastest_5k VARCHAR(20)
);


# INSTRUCTIONS:
brew install mysql@8.0
echo 'export PATH="/usr/local/opt/mysql@8.0/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
mysql -h tfrrs-database.cvyguqokm3xa.us-east-2.rds.amazonaws.com -u admin -p

ENTER PASSWORD: andrewtommydatabases
USE tfrrs_data;
SHOW TABLES;

IN PYTHON FILE: 
# ----------------------------
# MySQL database configuration
# ----------------------------
DB_HOST = 'tfrrs-database.cvyguqokm3xa.us-east-2.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASS = 'andrewtommydatabases' #replace with your own password
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
