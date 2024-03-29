from datetime import datetime
from dateutil.relativedelta import relativedelta 



# Returns current date and time
def return_current_date_and_time() -> list:
    """
    Returns current date and time. Used to track the start and end points of a habit. 

    No parameters."""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    return [current_time, current_date]



class Habit:
    """
    A class to represent a habit.
    
    Attributes:
        name: str
            Name to be given to the habit.
        periodicity: str
            Period unit (or habits period) for a habit that shows within which period
            the user performs the habit, namely, within hour/day/week/etc.
        time_span: int
            Duration for which the user wants to develop the habit. Combining with periodicity we 
            set, for example, 2 days or 5 weeks. 
        state: str
            The state of a habit, namely, \'In progress\'/\'Completed\'.
            Defaults to \'In progress\'.
        current_streak: int
            The current streak represents a number of successful, consequtive habit executions.
        longest_strek: int
            Stores the longest streak that has ever been achieved for a habit.
        start_time: str
            Stores a time of creation, i.e., starting a habit.
        start_date: str
            Stores a date of creation, i.e., starting a habit.
        end_time: str
            Stores the time of finishing, i.e., when habit is completed.
        end_time: str
            Stores the date of finishing, i.e., when habit is completed."""

    def __init__ (self, name: str, periodicity: str, 
                  time_span: int, state: str = "In progress",
                  current_streak: int = 0, longest_streak: int = 0,
                  start_time: str = None, start_date: str = None,
                  end_time: str = None, end_date: str = None) -> None:
        """
        Parameters:
            name: str
                Name to be given to the habit.
            periodicity: str
                Period unit (or habits period) for a habit that shows within which period
                the user performs the habit, namely, within hour/day/week/etc.
            time_span: int
                Duration for which the user wants to develop the habit. Combining with periodicity we 
                set, for example, 2 days or 5 weeks. 
            state: str, optimal
                The state of a habit, namely, \'In progress\'/\'Completed\'/\'Dropped\'.
                Defaults to \'In progress\'.
            current_streak: int, optimal
                The current streak represents a number of successful, consequtive habit executions.
            longest_strek: int, optimal
                Stores the longest streak that has ever been achieved for a habit.
            start_time: str, optimal
                Stores a time of creation, i.e., starting a habit.
            start_date: str, optimal
                Stores a date of creation, i.e., starting a habit.
            end_time: str, optimal
                Stores the time of finishing, i.e., when habit is completed.
            end_time: str, optimal
                Stores the date of finishing, i.e., when habit is completed.
                """     
        # Primary habit information to create it  
        self.name = name
        self.periodicity = periodicity
        self.time_span = time_span
        self.state = state

        # Secondary habit information to log it
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        if start_time == None and start_date == None:
            self.start_time, self.start_date = return_current_date_and_time()
        else:
            self.start_time, self.start_date = start_time, start_date
        self.end_time, self.end_date = end_time, end_date



    def update_habit_characteristic(self, characteristic_name: str, new_value) -> None:
        """
        Updates a habit characteristic.
        
        Parameters:
            characteristic_name: str
                Name of a characteristic to be updated.
            new_valie: any
                Value that replaces the old one."""
        if hasattr(self, characteristic_name):
            setattr(self, characteristic_name, new_value)
        else: 
            print(f"Characteristic {characteristic_name} doesn't exist. Try again.")



    def check_off_habit(self) -> None:
        """
        Updates streaks of a habit.
        
        No parameters."""
        if self.end_time is not None and self.end_date is not None:
            self.check_time_excess()

        self.current_streak += 1
        if self.current_streak>self.longest_streak:
            self.longest_streak = self.current_streak
        self.end_time, self.end_date = return_current_date_and_time() 

    def check_time_excess(self) -> None:
        """
        Checks whether the user exceeded time to complete a habit within a specific period.
        Habit is broken if the time difference between current time and the time of the last check
        greater than 1 periodicity. 
        E.g.: Periodicity is \'Week\'. Assume the user start the habit \'this\' week. If the user don't check it off
        until the end of the \'next\' week, the habit's currenet streak would be reset.

        No parameters."""
        current_time, current_date = return_current_date_and_time()
        current_time = datetime.strptime(current_time, '%H:%M:%S').time()
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
        current_datetime = datetime.combine(current_date, current_time)

        end_time = datetime.strptime(self.end_time, '%H:%M:%S').time()
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        end_datetime = datetime.combine(end_date, end_time)

        time_difference = [current_datetime.hour - end_datetime.hour,
                           current_datetime.day - end_datetime.day,
                           current_datetime.isocalendar().week - end_datetime.isocalendar().week,
                           current_datetime.month - end_datetime.month,
                           current_datetime.year - end_datetime.year]     
        time_excess = False
        range_codes = {
            "Hour": 5,
            "Day": 4,
            "Week": 3,
            "Month": 2,
            "Year": 1
        }
        for i in range(range_codes[self.periodicity]):
            if abs(time_difference[-i-1])>1:
                time_excess = True

        if time_excess:
            self.current_streak = 0
            print("Time has passed and your current streak has been reset!")
        


    def complete_habit(self) -> bool:
        """
        If during the entire period the habit developed without interruption, it is considered \'Сompleted\'
        
        No parameters."""
        if self.longest_streak == self.time_span:
            self.state = "Completed"
            return True
        else:
            return False
