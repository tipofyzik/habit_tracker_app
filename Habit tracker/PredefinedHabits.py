from dateutil.relativedelta import relativedelta 
from datetime import datetime
import random

from Database import Database
from Habit import Habit



def predefine_habits() -> list[Habit]:
    """
    Returns 5 predefined habits to demonstrate to the user what it could be.

    No parametes."""
    habit1 = Habit("Brush my teeth", "Day", 21)
    habit2 = Habit("Go to the gym", "Week", 4)
    habit3 = Habit("Go to my therapist", "Month", 6)
    habit4 = Habit("Take medicines", "Hour", 6)
    habit5 = Habit("Plant trees for charity", "Year", 3)
    return [habit1, habit2, habit3, habit4, habit5] 



def generate_habit_history(habit: Habit, database: Database) -> None:
    start_datetime = datetime(2024, 1, 17, 12, 4, 36)
    start_time = start_datetime.strftime("%H:%M:%S")
    start_date = start_datetime.strftime("%Y-%m-%d")
    habit.start_time = start_time
    habit.start_date = start_date

    def check_off_predefined_habit(habit: Habit) -> None:
        habit.current_streak += 1
        if habit.current_streak>habit.longest_streak:
            habit.longest_streak = habit.current_streak

    def update_data() -> None:
        end_time = end_datetime.strftime("%H:%M:%S")
        end_date = end_datetime.strftime("%Y-%m-%d")
        habit.end_time = end_time
        habit.end_date = end_date
        check_off_predefined_habit(habit)
        database.update_habit_characteristic_in_database(habit, ["end_time", "end_date"], 
                                                         [habit.end_time, habit.end_date])
        if habit.complete_habit():
            database.update_habit_characteristic_in_database(habit, ["state"], [habit.state])
        database.update_habit_characteristic_in_database(habit, ["current_streak", "longest_streak"], 
                                                         [habit.current_streak, habit.longest_streak])
        database.update_habit_logs(habit)

    for i in range(habit.time_span):
        if habit.periodicity == "Hour":
            end_datetime = start_datetime + relativedelta(hours=i, minutes=random.randint(1, 59))
        elif habit.periodicity == "Day":
            end_datetime = start_datetime + relativedelta(days=i, hours=random.randint(1, 23))
        elif habit.periodicity == "Week":
            end_datetime = start_datetime + relativedelta(weeks=i, days=random.randint(1, 6))
        elif habit.periodicity == "Month":
            end_datetime = start_datetime + relativedelta(months=i, days=random.randint(1, 30))
        elif habit.periodicity == "Year":
            end_datetime = start_datetime + relativedelta(years=i, days=random.randint(1, 364))
        update_data()
