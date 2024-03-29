from Habit import Habit

import sqlite3



class Database:
    """
    A class to represent a database to store and retrieve information.
    
    Attributes:
        name: str
            Name to be given for database.
        database: sqlite3.Connection
            Database that represents by this class."""
    def __init__(self, name: str = "AppDatabase.db"):
        self.name = name
        self.database = self.connect_database(name)

    # Database creation
    def connect_database(self, name: str = "AppDatabase.db") -> sqlite3.Connection:
        """
        Creates a connection to the database with a passed name.

        Parameters:
            name: str
                Name to be given for database."""
        database = sqlite3.connect(name)
        self.create_database_tables(database)
        return database

    def create_database_tables(self, database: sqlite3.Connection) -> None:
        """
        Creates tables in database, namely, for habits and their log.

        Parameters:
            database: sqlite3.Connection
                Database used for tasks."""
        # Since the "IF NOT EXISTS" clause is used, we don't need to check weather tables exist or not.
        # Moreover, code won't affect tables if they already exist.
        cursor = database.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                name TEXT PRIMARY KEY,
                periodicity TEXT,
                time_span INTEGER,
                state TEXT,
                current_streak INTEGER,
                longest_streak INTEGER,
                start_time TEXT,
                start_date TEXT,
                end_time TEXT,
                end_date TEXT
        )
    ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits_log (
                name TEXT,
                current_streak INTEGER,
                longest_streak INTEGER,
                end_time TEXT,
                end_date TEXT                
        )
    ''')
        database.commit()
        cursor.close()

    def disconnect_database(self) -> None:
        """
        Breaks the connection to the database.

        Parameters:
            self: Database
                The instance of the class itself."""
        self.database.close()

    def clean_tables_in_database(self) -> None:
        """
        Deletes all habits from database"""
        cursor = self.database.cursor()
        cursor.execute("DELETE FROM habits")
        cursor.execute("DELETE FROM habits_log")
        self.database.commit()
        cursor.close()

    # Function for debugging
    def delete_tables_in_database(self) -> None:
        """
        Deletes table structures from database. It is useful if you restructure your tables (you want more/less columns).
        Only for developers!"""
        cursor = self.database.cursor()
        cursor.execute("DROP TABLE IF EXISTS habits")
        cursor.execute("DROP TABLE IF EXISTS habits_log")
        self.database.commit()
        cursor.close()



    # Habits processing: adding, updating, deleting
    def insert_habit_to_database(self, habit: Habit) -> None:
        """
        Adds a habit with its corresponding information (parameters) 
        to the 'habits' and 'habits_log' tables in the database.

        Parameters:
            habit: Habit
                Habit that have to be added to database."""
        cursor=self.database.cursor()
        cursor.execute("""INSERT INTO habits VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            habit.name, 
            habit.periodicity, 
            habit.time_span, 
            habit.state,
            habit.current_streak, 
            habit.longest_streak, 
            habit.start_time, 
            habit.start_date, 
            habit.end_time, 
            habit.end_date,))
        cursor.execute("""INSERT INTO habits_log VALUES(?, ?, ?, ?, ?)""", (
            habit.name,
            habit.current_streak, 
            habit.longest_streak, 
            habit.end_time, 
            habit.end_date,))
        self.database.commit()
        cursor.close()

    def update_habit_characteristic_in_database(self, habit: Habit, characteristics: list, 
                                                new_values: list)-> None:
        """
        Changes the habit's value of a given characteristic.

        Parameters:
            habit: Habit
                Habit whose updated parameter should be updated in the database.
            characteristic_name: str
                Name of the characteristic to be updated.
            new_value: type depends on the charateristic
                Value that replaces the old one."""
        cursor=self.database.cursor()
        for characteristic, new_value in zip(characteristics, new_values):
            cursor.execute(f"""UPDATE habits SET {characteristic} = ? WHERE name = ?""",
                            (new_value, habit.name,))
        self.database.commit()
        cursor.close()

    def update_habit_logs(self, habit: Habit) -> None:
        """
        Updates habits_log table by adding new row with secondary information.
        
        Parameters:
            habit: Habit
                Habit whose updated secondary parameters should be added into logы."""
        cursor=self.database.cursor()
        cursor.execute("""INSERT INTO habits_log VALUES(?, ?, ?, ?, ?)""", (
            habit.name,
            habit.current_streak, 
            habit.longest_streak, 
            habit.end_time, 
            habit.end_date,))
        self.database.commit()
        cursor.close()
        

    def delete_habit_from_database(self, habit_name: str) -> None:
        """
        Deletes habit from each table in the database

        Parameters:
            habit_name: str
                Name of the habit to be deleted from the database."""
        cursor=self.database.cursor()
        cursor.execute("""DELETE FROM habits WHERE name = ?""", 
                       (habit_name,))
        cursor.execute("""DELETE FROM habits_log WHERE name = ?""", 
                       (habit_name,))
        self.database.commit()
        cursor.close()