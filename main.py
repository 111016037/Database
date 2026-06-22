from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List

app = FastAPI(title="籃球賽事管理系統 API")

# 允許前端跨網域存取 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 資料庫連線設定 (請根據實際環境修改)
DB_CONFIG = {
    "dbname": "basketball_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# Pydantic Models
class TeamCreate(BaseModel):
    team_name: str
    coach: str

# API 路由
@app.get("/teams")
def get_teams():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Team;")
    teams = cur.fetchall()
    cur.close()
    conn.close()
    return teams

@app.post("/teams")
def create_team(team: TeamCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Team (team_name, coach) VALUES (%s, %s) RETURNING *;",
            (team.team_name, team.coach)
        )
        new_team = cur.fetchone()
        conn.commit()
        return new_team
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/players/stats")
def get_player_stats():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT p.player_name, t.team_name, p.jersey_number, 
               SUM(s.points) as total_points, SUM(s.assists) as total_assists, SUM(s.rebounds) as total_rebounds
        FROM Player p
        JOIN Team t ON p.team_id = t.team_id
        LEFT JOIN Player_Match_Stat s ON p.player_id = s.player_id
        GROUP BY p.player_id, t.team_name;
    """
    cur.execute(query)
    stats = cur.fetchall()
    cur.close()
    conn.close()
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
