# TfrrsFinalProject

Make sure you setup mysql on your end. 
This one is the only relevant one for now:
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


This one is for ourdoor qualifying but may change: 
CREATE TABLE outdoor_qualifying_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    season VARCHAR(50) NOT NULL,
    event VARCHAR(50) NOT NULL,
    place VARCHAR(10),
    athlete_name VARCHAR(100),
    athlete_year VARCHAR(10),
    team VARCHAR(100),
    time_str VARCHAR(20),
    meet VARCHAR(100),
    meet_date VARCHAR(50),
    wind VARCHAR(10)
);
