import pandas as pd #type:ignore
import mysql.connector #type:ignore
from transform import *
from extract import *
from config import *
from mysql.connector import Error #type:ignore
def establish_connection():
    try:
        global conn
        conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password='sandeep123@M',
            database='PythonLearningDB'
        )
        if conn.is_connected():
            print('Connected to MySQL Server\n')
            return conn
    except Error as e:
        print(f'Error connecting to SQL:{e}')
        return None