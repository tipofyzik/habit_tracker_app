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



def check_off_habit(predefined_habit: Habit, new_end_datetime: datetime) -> None:
    """
    Updates streaks of a habit.
    
    Parameters:
        predefined_habit: Habit
            Predefined habit to be checked-off.
        new_end_datetime: datetime
            New end date and time for habit. This is an analog to \'current_datetime\' in case 
            we check habit off in real time."""
    if predefined_habit.end_time is not None and predefined_habit.end_date is not None:
        check_time_excess(predefined_habit, new_end_datetime)

    predefined_habit.current_streak += 1
    if predefined_habit.current_streak>predefined_habit.longest_streak:
        predefined_habit.longest_streak = predefined_habit.current_streak

def check_time_excess(predefined_habit: Habit, new_end_datetime: datetime) -> None:
    """
    Checks whether the user exceeded time to complete a habit within a specific period.
    Habit is broken if the time difference between current time and the time of the last check
    greater than 1 periodicity. 
    E.g.: Periodicity is \'Week\'. Assume the user start the habit \'this\' week. If the user don't check it off
    until the end of the \'next\' week, the habit's currenet streak would be reset.

    Parameters:
        predefined_habit: Habit
            Predefined habit to be checked-off.
        new_end_datetime: datetime
            New end date and time for habit. This is an analog to \'current_datetime\' in case 
            we check habit off in real time."""
    end_time = datetime.strptime(predefined_habit.end_time, '%H:%M:%S').time()
    end_date = datetime.strptime(predefined_habit.end_date, '%Y-%m-%d')
    end_datetime = datetime.combine(end_date, end_time)

    time_difference = [end_datetime.hour - new_end_datetime.hour,
                        end_datetime.day - new_end_datetime.day,
                        end_datetime.isocalendar().week - new_end_datetime.isocalendar().week,
                        end_datetime.month - new_end_datetime.month,
                        end_datetime.year - new_end_datetime.year]     
    time_excess = False
    range_codes = {
        "Hour": 5,
        "Day": 4,
        "Week": 3,
        "Month": 2,
        "Year": 1
    }
    for i in range(range_codes[predefined_habit.periodicity]):
        if abs(time_difference[-i-1])>1:
            time_excess = True

    if time_excess:
        predefined_habit.current_streak = 0
        print("Time has passed and your current streak has been reset!")



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


    def update_data(predefined_habit: Habit, end_datetime: datetime) -> None:
        """
        Updates end datetime, state and streaks of a predefined habit. It also updates logs.
        
        Parameters:
            predefined_habit: Habit
                Habit which data in the database should be updated."""
        end_time = end_datetime.strftime("%H:%M:%S")
        end_date = end_datetime.strftime("%Y-%m-%d")
        predefined_habit.end_time = end_time
        predefined_habit.end_date = end_date
        check_off_habit(predefined_habit, end_datetime)
        database.update_habit_characteristic_in_database(predefined_habit, ["end_time", "end_date"], 
                                                         [predefined_habit.end_time, predefined_habit.end_date])
        if predefined_habit.complete_habit():
            database.update_habit_characteristic_in_database(predefined_habit, ["state"], [predefined_habit.state])
        database.update_habit_characteristic_in_database(predefined_habit, ["current_streak", "longest_streak"], 
                                                         [predefined_habit.current_streak, predefined_habit.longest_streak])
        database.update_habit_logs(predefined_habit)

    for i in range(predefined_habit.time_span):
        if predefined_habit.periodicity == "Hour":
            delta = relativedelta(hours=i, minutes=random.randint(1, 59 - start_datetime.minute))
        elif predefined_habit.periodicity == "Day":
            delta = relativedelta(days=i, hours=random.randint(1, 23 - start_datetime.hour))
        elif predefined_habit.periodicity == "Week":
            delta = relativedelta(weeks=i, days=random.randint(1, 6 - start_datetime.weekday()))
        elif predefined_habit.periodicity == "Month":
            delta = relativedelta(months=i, days=random.randint(1, 30 - start_datetime.day))
        elif predefined_habit.periodicity == "Year":
            delta = relativedelta(years=i)
        end_datetime = start_datetime + delta
        update_data(predefined_habit, end_datetime)
