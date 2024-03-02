# Habit tracker app


# Installation
## Requirements
You need to intall Python with the version 3.11.3 and higher.
All required modules to install you can find in the file **"requirements.txt"**.
## How to install
1. Install Python from the [official site](https://www.python.org/downloads/).  
2. Install required modules (follow the links):  
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
**PredefinedHabits.py:** Upon user request, the first module uploads pre-defined template habits, specified by me, into the database. Also it upload history of these habits. The purpose is to show how habits can be defined and developed.  
**HabitTrackingApp.py:** Runs the application.  
**test_application.py:** Tests core application funcitonality (inserting data to/extracting data from database, updating habit characteristics and database, etc.).  

# 2. Implementation specifics



# 3. How to use
To run the application you should accomplish the following steps:  
1. Download the folder "Habit tracker" and put it wherever you want. Don't forget to install required libraries!
2. Open the command-line interface and specify the path to directory where "HabitTrackingApp.py" file is located. Do so by writing:
**cd Your/path/to/file**
Example: cd C:\Users\user\Downloads\Habit tracker
3. Now, write the following to run the application:
**python HabitTrackingApp.py**


Once you run the appliation, you will see the greeting message and the menu. The menu contains 6 options:  
**·** Add, update, or delete habit - suggest you to create new and update/delete existing habit  
**·** Check-off habit - suggest you to complete habit for specified period. For example, you have daily habit "Brush my teeth". By this option, you mark this habit as completed for "today".  
**·** View habit history - you can look at "checking-off" history of a certain habit. For example, you should accomplish you habit day for 20 days and let's say you'd done 17/20 days. This option will show you last 10 succesful completions of the habit.  
**·** Analyze habits - suggest you to analyze existing habits. You can look at all developed habits or ask for the longest streak of a certain habit.  
**·** Additional options - here you can upload/delete predefined habits or delete all your habits at all.  
**·** Quit - terminates the applicaiton.  


## Examples of usage



# 4. Further developing
My project has cases which can be developed.  
Firstly, the option of 'upcoming events' can be added. If the user would like to look at the events that they have to accomplish this day/week/month/etc., the program would dispay these events accordingly. This feature would make it more convenient to track one's habits.  
Secondly,  

# 5. Sources
[1] https://pypi.org/project/python-dateutil/  
[2] https://pypi.org/project/tabulate/  
[3] https://questionary.readthedocs.io/en/stable/  
