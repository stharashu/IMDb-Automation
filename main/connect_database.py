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
            
            self.cursor.execute(insert_sql, values)
            self.conn.commit()

        except sqlite3.Error as e:
            print("Error inserting into database:", e)


    # def insert_data(self, Movie, Imdb_rating , Popularity, Storyline, Genre, Review_rating, Review_titles, Review_description, status):
    #     try:
    #         # Convert lists to JSON strings
    #         Genre_str = json.dumps(Genre)
    #         Review_rating_str = json.dumps(Review_rating)
    #         Review_titles_str = json.dumps(Review_titles)
    #         Review_description_str = json.dumps(Review_description)

    #         insert_sql = f'''INSERT INTO {self.table_name} (Movie, Imdb_rating, Popularity, Storyline, Genre, Review_rating, Review_titles, Review_description, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    #         values = (Movie, Imdb_rating, Popularity, Storyline, Genre_str, Review_rating_str, Review_titles_str, Review_description_str, status)
    #         self.cursor.execute(insert_sql, values)
    #         self.conn.commit()
    #     except sqlite3.Error as e:
    #         print("Error inserting into database:", e)


        #     insert_sql = f'''INSERT INTO {self.table_name} (Movie, Imdb_rating, Popularity, Storyline, Genre, Review_rating, Review_titles, Review_description, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        #     values = (Movie, Imdb_rating , Popularity, Storyline, Genre, Review_rating, Review_titles, Review_description, status)
        #     self.cursor.execute(insert_sql, values)
        #     self.conn.commit()
        # except sqlite3.Error as e:
        #     print("Error inserting into database:", e)
