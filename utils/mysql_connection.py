import pyodbc
#from DBUtils.PooledDB import PooledDB
import os
from flask import jsonify
import json
pyodbc.pooling= True

class Database:
    def __init__(self):
        self.server = os.environ.get("MYSQL_SERVER")
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.port = 1433
        self.database = os.environ.get("MYSQL_DATABASE")
        self.username = os.environ.get("MYSQL_USERNAME")
        self.password = os.environ.get("MYSQL_PASSWORD")
        self._CreatePool()

    def _CreatePool(self):
       #self.Pool = PooledDB(creator=pyodbc, mincached=2, maxcached=5, maxshared=3, maxconnections=6, blocking=True, DRIVER=self.driver, SERVER=self.server, PORT=self.port, DATABASE=self.database, UID=self.username, PWD=self.password)
        print("skip")

    def _Getconnect(self):
        #self.conn = self.Pool.connection()
        print("Connecting")
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        conn = pyodbc.connect(connection_string)
        return conn
    # query sql

    def ExecQuery(self, sql):
        conn = self._Getconnect()
        cur = conn.cursor()
        cur.execute(sql)

        # Get column names from cursor description
        column_names = [desc[0] for desc in cur.description]

        # Fetch all rows
        rows = cur.fetchall()

        result_list = []

        for row in rows:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                # Attempt to parse the string as JSON
                try:
                    parsed_json = json.loads(row[i])
                    row_dict[col_name] = parsed_json
                except (TypeError, json.JSONDecodeError):
                    # If it's not valid JSON or not a string, leave it as-is
                    row_dict[col_name] = row[i]
            result_list.append(row_dict)
        
        cur.close()
        conn.close()
        
        return result_list
    # non-query sql

    def ExecNoQuery(self, sql):
        try:
            conn = self._Getconnect()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            # Rollback in case of error
            conn.rollback()
            raise e