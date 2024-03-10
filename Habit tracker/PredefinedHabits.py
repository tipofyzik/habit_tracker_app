from Database import Database
from Habit import Habit

from dateutil.relativedelta import relativedelta 
from datetime import datetime
import random



def predefine_habits() -> list[Habit]:
    """
    Returns 5 predefined habits to demonstrate to the user what it could be.

    No parametes."""
    habit1 = Habit("Brush my teeth", "Day", 28)
    habit2 = Habit("Go to the gym", "Week", 4)
    habit3 = Habit("Go to my therapist", "Month", 6)
    habit4 = Habit("Take medicines", "Hour", 8)
    habit5 = Habit("Plant trees for charity", "Year", 3)
    return [habit1, habit2, habit3, habit4, habit5] 



def generate_habit_history(predefined_habit: Habit, database: Database) -> None:
    """
    Generates approximate history for a certain habit. Used only to examplify how habit could be defined and developed.
    
    Parameters:
        habit: Habit
            Predefined habit which history should be generated.
        database: Database
            Database into which data about predefined habit will be uploaded."""
    start_datetime = datetime(2024, 1, 17, 12, 4, 36)
    start_time = start_datetime.strftime("%H:%M:%S")
    start_date = start_datetime.strftime("%Y-%m-%d")
    predefined_habit.start_time = start_time
    predefined_habit.start_date = start_date

    def check_off_predefined_habit(predefined_habit: Habit) -> None:
        """
        Updates streaks of a predefined habit.
        
        Parameters:
            habit: Habit
                Habit to \'check-off\'"""
        predefined_habit.current_streak += 1
        if predefined_habit.current_streak>predefined_habit.longest_streak:
            predefined_habit.longest_streak = predefined_habit.current_streak

    def update_data(predefined_habit: Habit) -> None:
        """
        Updates end datetime, state and streaks of a predefined habit. It also updates logs.
        
        Parameters:
            predefined_habit: Habit
                Habit which data in the database should be updated."""
        end_time = end_datetime.strftime("%H:%M:%S")
        end_date = end_datetime.strftime("%Y-%m-%d")
        predefined_habit.end_time = end_time
        predefined_habit.end_date = end_date
        check_off_predefined_habit(predefined_habit)
        database.update_habit_characteristic_in_database(predefined_habit, ["end_time", "end_date"], 
                                                         [predefined_habit.end_time, predefined_habit.end_date])
        if predefined_habit.complete_habit():
            database.update_habit_characteristic_in_database(predefined_habit, ["state"], [predefined_habit.state])
        database.update_habit_characteristic_in_database(predefined_habit, ["current_streak", "longest_streak"], 
                                                         [predefined_habit.current_streak, predefined_habit.longest_streak])
        database.update_habit_logs(predefined_habit)

    for i in range(predefined_habit.time_span):
        if predefined_habit.periodicity == "Hour":
            end_datetime = start_datetime + relativedelta(hours=i, minutes=random.randint(1, 59))
        elif predefined_habit.periodicity == "Day":
            end_datetime = start_datetime + relativedelta(days=i, hours=random.randint(1, 23))
        elif predefined_habit.periodicity == "Week":
            end_datetime = start_datetime + relativedelta(weeks=i, days=random.randint(1, 6))
        elif predefined_habit.periodicity == "Month":
            end_datetime = start_datetime + relativedelta(months=i, days=random.randint(1, 30))
        elif predefined_habit.periodicity == "Year":
            end_datetime = start_datetime + relativedelta(years=i, days=random.randint(1, 364))
        update_data(predefined_habit)
