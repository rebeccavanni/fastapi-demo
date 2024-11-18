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



