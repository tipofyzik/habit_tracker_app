from Habit import Habit



def predefine_habits() -> list[Habit]:
    """
    Returns 5 predefined habits to demonstrate to the user what it could be.

    No parametes."""

    habit1 = Habit("Brush my teeth", "Day", 7)
    habit2 = Habit("Go to the gym", "Week", 4)
    habit3 = Habit("Go to my therapist", "Month", 6)
    habit4 = Habit("Take medicines", "Hour", 6)
    habit5 = Habit("Plant trees for charity", "Year", 3)
    return [habit1, habit2, habit3, habit4, habit5] 
