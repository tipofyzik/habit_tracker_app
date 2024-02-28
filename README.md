# Habit tracker app


# Installation
## Requirements
You need to intall Python with the version 3.11.3 and higher.
All required modules to install you can find in the file **"requirements.txt"**.
## How to install
1. Install Python from the [official site](https://www.python.org/downloads/).  
2. Install required modules:  
   2.1 [**python-dateutil**](https://pypi.org/project/python-dateutil/) - necessary for logging data.  
   2.2 [**tabulate**](https://pypi.org/project/tabulate/) - necessary for displaying data.  
   2.3 [**questionary**](https://questionary.readthedocs.io/en/stable/) - necessary for convenient user interaction.  
3. Download the folder "Habit tracker". It contains **"HabitTrackingApp.py"** file that runs the application.  


# 1. About programming design selection
For this project, I used object-oriented and functional programming because it allows to distribute required functionality between different classes clearly. For this purpose, I wrote 4 classes each of which is responsible for a certain thing:  
**·** **_Habit class_** is responsible for creating a habit object and for manipulating its attributes.  
**·** **_Database class_** writes to and reads from the application database. It also can change an already stored information in the database.  
**·** **_DatabaseAnalyzer class_** is responsible for analization of database. Upon request it reads the database and returns the corresponding habits.  
**·** **_CommandLineInterface class_** represents an interaction between user and the application.  

My project also contains 3 files more: PredefinedHabits.py, HabitTrackingApp.py, test_application.py.  
First module upon user request uploads predefined by me habits into database. Moreover, it contains a data for 4 weeks.


# 2. How to use

# 3. Further developing

# 4. Sources
[1] https://pypi.org/project/python-dateutil/
[2] https://pypi.org/project/tabulate/
[3] https://questionary.readthedocs.io/en/stable/
