CREATE TABLE Team (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    coach VARCHAR(100)
);

CREATE TABLE Player (
    player_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES Team(team_id) ON DELETE CASCADE,
    player_name VARCHAR(100) NOT NULL,
    jersey_number INT,
    position VARCHAR(20)
);

CREATE TABLE Match (
    match_id SERIAL PRIMARY KEY,
    home_team_id INT REFERENCES Team(team_id),
    away_team_id INT REFERENCES Team(team_id),
    match_date TIMESTAMP NOT NULL,
    home_score INT DEFAULT 0,
    away_score INT DEFAULT 0
);

CREATE TABLE Player_Match_Stat (
    stat_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES Player(player_id) ON DELETE CASCADE,
    match_id INT REFERENCES Match(match_id) ON DELETE CASCADE,
    points INT DEFAULT 0,
    assists INT DEFAULT 0,
    rebounds INT DEFAULT 0
);

-- 預設測試資料
INSERT INTO Team (team_name, coach) VALUES ('勇士隊', 'Steve Kerr'), ('湖人隊', 'JJ Redick');
INSERT INTO Player (team_id, player_name, jersey_number, position) VALUES 
(1, 'Stephen Curry', 30, 'PG'),
(2, 'LeBron James', 23, 'SF');
