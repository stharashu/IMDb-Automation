import sqlite3
import json

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("IMDb.db")
            self.cursor = self.conn.cursor()
            self.table_name = "Movies"
        except sqlite3.Error as e:
            print("Error connecting to SQLite database:", e)

    def create_table(self):
        try:
            create_table_sql = f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                Movie TEXT,
                Imdb_rating REAL,
                Popularity REAL,
                Storyline TEXT,
                Genre TEXT,
                Review_1 TEXT,
                Review_2 TEXT,
                Review_3 TEXT,
                Review_4 TEXT,
                Review_5 TEXT,
                status TEXT
                )'''
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def insert_data(self, Movie, Imdb_rating, Popularity, Storyline, Genre, Review_1,Review_2, Review_3, Review_4, Review_5, status):
        try:
            
            # Review_description_1, Review_description_2, Review_description_3, Review_description_4, Review_description_5 = Review_descriptions

            insert_sql = f'''INSERT INTO {self.table_name} (Movie, Imdb_rating, Popularity, Storyline, Genre, Review_1,Review_2, Review_3, Review_4, Review_5, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            values = (Movie, Imdb_rating, Popularity, Storyline, Genre, Review_1,Review_2, Review_3, Review_4, Review_5, status)
            values = ["N/A" if v is None else v for v in values]
            self.cursor.execute(insert_sql, values)
            self.conn.commit()

        except sqlite3.Error as e:
            print("Error inserting into database:", e)
