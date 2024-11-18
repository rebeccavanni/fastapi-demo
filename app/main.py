#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

import json
import os
import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
load_dotenv()
DBHOST = os.getenv("Database_Host")
DBUSER = os.getenv("Database_User")
DBPASS = os.getenv("Database_Pass")
DB = "ecn2wh"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}


@app.get('/songs')
def get_songs():
    try:
        db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
        cur = db.cursor()
        query = "SELECT * FROM songs ORDER BY songid;"
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = [dict(zip(headers, result)) for result in results]
        cur.close()  # Close the cursor
        db.close()   # Close the database connection
        return json_data
    except Error as e:
        return {"Error": f"MySQL Error: {str(e)}"}


@app.get('/songs/details')
def get_song_details():
    query = """
        SELECT 
            s.title AS title, 
            s.album AS album, 
            s.artist AS artist, 
            s.year AS year, 
            CONCAT('https://your-s3-bucket-url/', s.file) AS mp3_url, 
            CONCAT('https://your-s3-bucket-url/', s.image) AS image_url, 
            g.name AS genre
        FROM songs s
        JOIN genres g ON s.genre = g.genreid
        ORDER BY s.songid;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = [dict(zip(headers, result)) for result in results]
        return json_data
    except Error as e:
        return {"Error": f"MySQL Error: {str(e)}"}




