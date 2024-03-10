from Habit import Habit
from Database import Database
from DatabaseAnalyzer import DatabaseAnalyzer

from dateutil.relativedelta import relativedelta 
from datetime import datetime

import unittest

"""
This module test critical points in Habit tracking application, namely,
Habit, Database and DatabaseAnalyzer classes. 

The CommandLineInterface class is based on these three classes, so it isn't tested here."""



class TestHabitClass(unittest.TestCase):
    """
    This class tests the basic functionality of the Habit class."""
    def test_habit_creation(self) -> None:
        """
        Creates a habit instance and asserts whether this object is an object of the Habit class.
        
        Assertioons:
        - Assert that created instance is an instance oh the Habit class."""
        habit_obj = Habit('name', 'Day', 0)
        self.assertIsInstance(habit_obj, Habit)

    def test_habit_update(self) -> None:
        """
        Creates a habit instance, updates its characteristic and then 
        compares updated habit characteristic value with that new value.
        
        Assertioons:
        - Assert that updated characteristic is equal to new value."""
        habit_obj = Habit('name', 'Day', 0)
        characteristic = 'periodicity'
        new_value = 'Week'
        habit_obj.update_habit_characteristic(characteristic, new_value)
        self.assertEqual(habit_obj.periodicity, new_value)

    def test_habit_check_off(self) -> None:
        """
        Creates a habit instance, checks it off several times and 
        compares habit's streaks with the updated one.
        
        Assertioons:
        - Assert that updated habit's streaks are equal to new values."""
        habit_obj = Habit('name', 'Day', 7)
        current_streak, longest_streak = habit_obj.current_streak, habit_obj.longest_streak
        for _ in range(habit_obj.time_span-2):
            habit_obj.check_off_habit()
            current_streak += 1
            longest_streak += 1
        self.assertEqual(current_streak, habit_obj.current_streak)
        self.assertEqual(longest_streak, habit_obj.longest_streak)

    def test_habit_completion(self) -> None:
        """
        Creates a habit instance, 'develops' it and asserts whether 
        the state of the habit is equal to \'Completed\'.
        
        Assertioons:
        - Assert that completed habit have \'Completed\' state."""
        habit_obj = Habit('name', 'Day', 5)
        for _ in range(habit_obj.time_span):
            habit_obj.check_off_habit()
        habit_obj.complete_habit()
        self.assertEqual(habit_obj.state, "Completed")

    def test_streak_reset(self) -> None:
        """
        Creates a habit instance, checks it off several times, changes habit end datetime 
        and then checks habit again. The streak should be reset to zero, because the allotted time for 
        performing the habit has been exceeded. After reseting, the program adds 1 to streak, because the habit 
        has been checked off. Function asserts that the current streak is equal to 1."""
        habit_obj = Habit('name', 'Day', 9)
        for _ in range(habit_obj.time_span-2):
            habit_obj.check_off_habit()
        end_date = datetime.strptime(habit_obj.end_date, '%Y-%m-%d')
        end_date = end_date - relativedelta(days=3)
        habit_obj.end_date = end_date.strftime('%Y-%m-%d')
        habit_obj.check_off_habit()
        self.assertEqual(habit_obj.current_streak, 1)



class TestDatabaseAndDatabaseAnalyzer(unittest.TestCase):
    """
    This class tests the functionality of both the Database class and the DatabaseAnalyzer class simultaneously. 
    The reason is that the first class is responsible for inserting and updating information, 
    while the second class is responsible for retrieving information from the database.
    We can't check inserted/updated information correctly without retrieving it."""
    @classmethod
    def setUpClass(cls) -> None:
        cls.database = Database(name='TestDatabase.db')
        cls.database.clean_tables_in_database()
        cls.analyzer = DatabaseAnalyzer(cls.database.name)

    def test_database_name(self) -> None:
        """
        Assertions:
        - Assert that database name is \'TestDatabase.db\'"""
        self.assertEqual(self.database.name, "TestDatabase.db")

    def test_habit_insertion_and_extraction(self) -> None:
        """
        Creates habit instance and inserts it into the TestDatabase.db.

        Then, this function extracts uploaded information from database 
        and compares it with habit's attribute values.
        
        Assertions:
        - Assert that the habit's attribute values match the extracted information."""
        habit_obj = Habit('name', 'Day', 0)
        self.database.insert_habit_to_database(habit_obj)

        habit_info = list(vars(habit_obj).values())
        extracted_info = self.analyzer.return_detailed_information_about_habit(habit_obj.name)[1]
        self.assertEqual(habit_info, extracted_info)

        # Delete data from database not to raise error in the next tests
        self.database.delete_habit_from_database(habit_obj.name)

    def test_habit_update(self) -> None:
        """
        Creates habit instance and inserts it into the TestDatabase.db.

        Then, this function updates habit and the corresponding information in database. 
        Next, it retrieves the data about the uploaded habit and makes sure that retrived 
        information is equal to updated habit.
        
        Assertions:
        - Assert that the habit's updated characteristic match the value from database."""
        habit_obj = Habit('name', 'Day', 0)
        self.database.insert_habit_to_database(habit_obj)
        habit_obj.update_habit_characteristic('periodicity', 'Week')
        self.database.update_habit_characteristic_in_database(habit_obj, ['periodicity'], ['Week'])

        retrived_habit_info = self.analyzer.return_detailed_information_about_habit(habit_obj.name)[1]
        retrieved_habit = Habit(*retrived_habit_info)

        self.assertEqual(retrieved_habit.periodicity, "Week")
        self.assertEqual(habit_obj.periodicity, retrieved_habit.periodicity)
        
        # Delete data from database not to raise error in the next tests
        self.database.delete_habit_from_database(habit_obj.name)

    def test_habit_deletion_from_database(self) -> None:
        """
        Creates habit instance and inserts it into the TestDatabase.db.

        Then, this function deletes habit from database and tries to retrive 
        information about this habit. Test passed if the result of extraction is None.

        Assertions:
        - Assert that the result of habit extraction from database is None."""
        habit_obj = Habit('name', 'Day', 0)
        self.database.insert_habit_to_database(habit_obj)
        self.database.delete_habit_from_database(habit_obj.name)

        retrived_habit_info = self.analyzer.return_detailed_information_about_habit(habit_obj.name)[1]
        self.assertIsNone(retrived_habit_info)

    def test_returning_streaks(self) -> None:
        """
        Test functions that are responsible for returning longest streak
        among all habits and the longest streak of a give, respectively."""
        habit_obj1 = Habit('name1', 'Day', 15)
        range1 = 7
        for _ in range(range1):
            habit_obj1.check_off_habit()

        habit_obj2 = Habit('name2', 'Week', 7)
        range2 = 4
        for _ in range(range2):
            habit_obj2.check_off_habit()

        self.database.insert_habit_to_database(habit_obj1)
        self.database.insert_habit_to_database(habit_obj2)

        longest_streak_of_all_habits = self.analyzer.return_longest_streak_of_all_habits()[1]
        longest_streaks_of_given_habit = self.analyzer.return_longest_streaks_of_given_habit(habit_obj2.name)
        self.assertEqual(longest_streak_of_all_habits, range1)
        self.assertEqual(longest_streak_of_all_habits, habit_obj1.longest_streak)
        self.assertEqual(longest_streaks_of_given_habit, range2)
        self.assertEqual(longest_streaks_of_given_habit, habit_obj2.longest_streak)

        # Delete data from database not to raise error in the next tests
        self.database.delete_habit_from_database(habit_obj1.name)
        self.database.delete_habit_from_database(habit_obj2.name)               

    def test_return_habits(self) -> None:
        """
        Test functions that are responsible for returning habits in DatabaseAnalyzer, i.e.,
        return_currently_tracked_habits and return_habits_with_the_same_periodicity."""
        def compare_class_objects(class_obj1: Habit, class_obj2: Habit):
            habit1_attributes = list(vars(class_obj1).values())
            habit2_attributes = list(vars(class_obj2).values())
            for value1, value2 in zip(habit1_attributes, habit2_attributes):
                self.assertEqual(value1, value2)

        # Return habits all tracked habits
        habit_obj1 = Habit('name1', 'Day', 0)
        habit_obj2 = Habit('name2', 'Week', 0)
        self.database.insert_habit_to_database(habit_obj1)
        self.database.insert_habit_to_database(habit_obj2)

        currently_tracked_habits = self.analyzer.return_currently_tracked_habits()
        habits = [Habit(*habit) for habit in currently_tracked_habits]
        compare_class_objects(habit_obj1, habits[0])
        compare_class_objects(habit_obj2, habits[1])
        self.database.delete_habit_from_database(habit_obj1.name)
        self.database.delete_habit_from_database(habit_obj2.name)

        # Return habits with the same periodicity
        habit_obj1 = Habit('name1', 'Day', 0)
        habit_obj2 = Habit('name2', 'Day', 0)
        self.database.insert_habit_to_database(habit_obj1)
        self.database.insert_habit_to_database(habit_obj2)

        habits_with_the_same_periodicity = self.analyzer.return_habits_with_the_same_periodicity('Day')
        habits = [Habit(*habit) for habit in habits_with_the_same_periodicity]
        compare_class_objects(habit_obj1, habits[0])
        compare_class_objects(habit_obj2, habits[1])

        # Delete data from database not to raise error in the next tests
        self.database.delete_habit_from_database(habit_obj1.name)
        self.database.delete_habit_from_database(habit_obj2.name)

    def test_detailed_habit_info(self) -> None:
        """Tests return_detailed_information_about_habit function in DatabaseAnalyzer module.
        Creates habit, updates it several times, checks it off and finally compares data in database 
        with the habit attributes itself.
        
        No parameters."""
        def check_off_loop(habit_obj: Habit, loop_range: int):
            """Checks habit off for several times.
            
            Parameters:
                habit: Habit
                    Habit to be checked-off.
                loop_range: int
                    The number for for-loop."""
            for _ in range (loop_range):
                habit_obj.check_off_habit()
                self.database.update_habit_characteristic_in_database(habit_obj, 
                                                                    ["end_time", "end_date"], 
                                                                    [habit_obj.end_time, habit_obj.end_date])
                if habit_obj.complete_habit():
                    self.database.update_habit_characteristic_in_database(habit_obj, ["state"], [habit_obj.state])
                self.database.update_habit_characteristic_in_database(habit_obj, 
                                                                    ["current_streak", "longest_streak"], 
                                                                    [habit_obj.current_streak, habit_obj.longest_streak])

        habit_obj = Habit("name", "Day", 4)
        self.database.insert_habit_to_database(habit_obj)
        habit_obj.update_habit_characteristic("periodicity", "Month")
        self.database.update_habit_characteristic_in_database(habit_obj, ["periodicity"], [habit_obj.periodicity])
        range1=3
        check_off_loop(habit_obj, range1)

        habit_obj.update_habit_characteristic("time_span", 11)
        self.database.update_habit_characteristic_in_database(habit_obj, ["time_span"], [habit_obj.time_span])
        range2 = 5
        check_off_loop(habit_obj, range2)
        
        extracted_habit = self.analyzer.return_detailed_information_about_habit(habit_obj.name)[1]
        extracted_habit = Habit(*extracted_habit)
        self.assertEqual(extracted_habit.name, "name")
        self.assertEqual(habit_obj.name, extracted_habit.name)

        self.assertEqual(extracted_habit.periodicity, "Month")
        self.assertEqual(habit_obj.periodicity, extracted_habit.periodicity)

        self.assertEqual(extracted_habit.time_span, 11)
        self.assertEqual(habit_obj.time_span, extracted_habit.time_span)

        self.assertEqual(extracted_habit.state, "In progress")
        self.assertEqual(habit_obj.state, extracted_habit.state)

        self.assertEqual(extracted_habit.current_streak, range1+range2)
        self.assertEqual(habit_obj.current_streak, extracted_habit.current_streak)

        self.assertEqual(extracted_habit.longest_streak, range1+range2)
        self.assertEqual(habit_obj.longest_streak, extracted_habit.longest_streak)

        self.assertEqual(habit_obj.start_time, extracted_habit.start_time)
        self.assertEqual(habit_obj.start_date, extracted_habit.start_date)
        self.assertEqual(habit_obj.end_time, extracted_habit.end_time)
        self.assertEqual(habit_obj.end_date, extracted_habit.end_date)

        # Delete data from database not to raise error in the next tests
        self.database.delete_habit_from_database(habit_obj.name)




if __name__ == '__main__':
    unittest.main()
