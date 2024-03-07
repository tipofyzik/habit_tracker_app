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

# 2. How to use
To run the application you should accomplish the following steps:
1. Download the folder "Habit tracker" and put it wherever you want. Don't forget to install required libraries!
2. Open the command-line interface and specify the path to directory where "HabitTrackingApp.py" file is located. Do so by writing:  
**cd Your/path/to/file**  
Example: cd C:\Users\user\Downloads\Habit tracker
3. Now, write the following to run the application:  
**python HabitTrackingApp.py**  

_**Note:**_ To run tests for the project perform step 2 and then write:
**python test_application.py**

Once you run the appliation, you will see the greeting message and the menu. The menu contains 6 options:  
**·** Add, update, or delete habit - suggest you to create new and update/delete existing habit  
**·** Check-off habit - suggest you to complete habit for specified period. For example, you have daily habit "Brush my teeth". By this option, you mark this habit as completed for "today".  
**·** View habit history - you can look at "checking-off" history of a certain habit. For example, you should accomplish you habit day for 20 days and let's say you'd done 17/20 days. This option will show you last 10 succesful completions of the habit.  
**·** Analyze habits - suggest you to analyze existing habits. You can look at all developed habits or ask for the longest streak of a certain habit.  
**·** Additional options - here you can upload/delete predefined habits or delete all your habits at all.  
**·** Quit - terminates the applicaiton.  


## Examples of usage
This video shows how you can add, update and delete habit. Here, I create new habit, show that it's tracked with the help of analitics module, change habit characteristics and show that they have been changed.  
https://github.com/tipofyzik/habit_tracker_app/assets/84290230/a2338131-976a-4b35-85b1-ae1f373ce689  



# 3. Implementation specifics
You can note that my project on github doesn't contain any database files for the application to work. This is because it will be created once you run the program.  

My project has 2 possible databases: "AppDatabase.db" and "TestDatabase.db". The first one creates once you run "HabitTrackingApp.py" file and the other one creates when you run "test_application.py" file. These databases don't affect each other and serve for the application to work and to test the application, respectively.  

The "PredefinedHabits.py" module contains the functions that create habit objects and their history (an example how these habits could be developed). This is important to note that history varies a little bit each time you upload predefined_habits. This is because history creation contains random functions to make it more 'live' (like people don't always follow the shedule and make something earlier or later a little bit). It's important to note that since the history for all predefined habits is created, they all are marked as 'completed. To look at them choose 'Analyze habits' -> 'Show me all already developed habits'.  

**Here, I explain when the application counts habit completion as 'successful' and when not**.  
Let's say the user defines their daily habit on the 2nd of January (red cell). Suppose the user wants to develop this habit for a week and begins to accomplish it on the 4th of January. If the user succesfully completes (green cell) the habit  completes the habit every day for the entire week, without any breaks, we say the habit to be developed and the user has achived their goal (image below). With each consecutive successful completion of the habit the streak counter increases, e.g., if there are 5 consecutive completions, habit streak would be 5.  
![image](https://github.com/tipofyzik/habit_tracker_app/assets/84290230/a89270d9-91c4-47d2-8b59-8c617b78cbdc)  

However, if we the user skips a habit for one day (yellow cell) the streak is reset to zero. This process will repeat until the user accomplishes habit for the required duration. In our example, the user should perform the habit for 7 consecutive days (image below). Once the user develop the habit we say that the habit is 'completed'.    
![image](https://github.com/tipofyzik/habit_tracker_app/assets/84290230/ea74a920-e354-48c6-9522-2a88b85d2f10)  

Summing up, the streak is reset when the user doesn't accomplish habit during required period. In our example, the habit is daily. My application analyze it according to the following rule:  
Let's assume again that the habit has started on the 2nd of January and performed it in the first time on this day at 11:57:24 (24-hour clock), i.e., the streak is 1. The streak will be reset to zero if the the time of a next check-off later than thhe 3rd of January, 23:59:59. This is important to note that even if the user exceeds alloted time the streak would be equal to 1. This is because every time when the user checks-off the habit the streak increases by 1. So, firstly, streak resets and then 1 is added to it.  
**This is similar to other periods, such as hour, week, etc.**  


# 4. Further developing
My project has cases which can be further developed:  
1. The option of 'upcoming events' can be added. If the user would like to look at the events that they have to accomplish this day/week/month/etc., the program would dispay these events accordingly. This feature would make it more convenient to track one's habits.  
2. The GUI can be added.

# 5. Sources
[1] https://www.python.org/  
[2] https://pypi.org/project/python-dateutil/  
[3] https://pypi.org/project/tabulate/  
[4] https://questionary.readthedocs.io/en/stable/  
