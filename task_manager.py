# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#=====Defining required functions=====
def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    while True:
        print(border)
        new_username = input("New Username: ")
        if new_username.lower() not in username_password:
            # - Request input of a new password
            new_password = input("New Password: ")

            # - Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                print("New user added")
                username_password[new_username] = new_password
                
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))

            # - Otherwise you present a relevant message.
            else:
                print("\nPasswords do not match.")
            break

        else:
             print("\nInvalid - Username already in use.")


def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''
    while True:
        print(border)
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        break


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print(f"{border}\n\nTask successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''

    for t in task_list:
        disp_str = f"{border}\n\n"
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task Completed: \t{t['completed']}\n\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    view_mine_tasks = []
    for t_index, t in enumerate(task_list):
        if t['username'] == curr_user and t['completed'] is False:
            disp_str = f"{border}\n\n"
            disp_str += f"Task Number: \t {t_index}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            view_mine_tasks.append(task_list[t_index])
            print(disp_str)

 
    edit_tasks(view_mine_tasks)


def edit_tasks(view_mine_tasks):
    '''Allows user to edit their tasks. Tasks list created in view_mine() as argument
    '''

    if view_mine_tasks:
        while True:

            # User makes their selections
            edit_task = input("Please enter Task Number of task you would like to edit, or -1 to return to main menu: ")
            if edit_task.isnumeric():
                edit_task = int(edit_task)

            if edit_task in range(len(task_list)):
                edit_choice = input("To mark task complete, enter: y\nTo edit task, enter: e\n")

                # Update task_list dictionary value
                if edit_choice.lower() == "y":
                    task_list[edit_task]['completed'] = "Yes"

                elif edit_choice.lower() == "e":
                    while True:
                        new_user = input("Please enter user you would like to assign this task to: ")
                        if new_user not in username_password.keys():
                            print("User not recognised")
                        else:
                            # print(task_list[edit_task]['username'])
                            task_list[edit_task]['username'] = new_user
                            print(task_list[edit_task]['username'])
                            break

            elif edit_task == "-1":
                break
            else:
                print("Invalid input!")
    else:
        print("\nNo tasks available!\n")           


def generate_results():
    """Process data to determine task statistics and write results to task_overview.txt"""

    # The total number of tasks that have been generated and tracked using the task_manager.py.
    total_tasks = len(task_list)

    # The total number of completed tasks.
    completed_tasks = 0
    for i in task_list:
        if i['completed'] == "Yes":
            completed_tasks += 1

    # The total number of uncompleted tasks.
    uncompleted_tasks = total_tasks - completed_tasks

    # The total number of tasks that haven’t been completed and that are overdue.
    overdue_tasks = 0
    # today = datetime.today()
    for i in task_list:
        if i['completed'] != "Yes" and i['due_date'] < today:
            overdue_tasks += 1

    # The percentage of tasks that are incomplete.
    incomplete_percentage = int((uncompleted_tasks/total_tasks)*100)

    # The percentage of tasks that are overdue.
    overdue_percentage = int((overdue_tasks/total_tasks)*100)

    # Write to text file task_overview.txt to display the results in a user friendly way.
    with open('task_overview.txt', 'w') as file:
        file.write(f"Total tasks:  {total_tasks}\n")
        file.write(f"Completed tasks:  {completed_tasks}\n")
        file.write(f"Uncompleted tasks:  {uncompleted_tasks}\n")
        file.write(f"Overdue tasks:  {overdue_tasks}\n")
        file.write(f"Percentage of uncompleted tasks:  {incomplete_percentage}%\n")
        file.write(f"Percentage of overdue tasks:  {overdue_percentage}%\n")
        
    # The total number of users registered with task_manager.py.
    users_registered = len(username_password)

    user_stats(curr_user)


def user_stats(name):
    """Processes data specific to user and write it to user_overview.txt"""

    # The total number of users registered with task_manager.py.
    users_registered = len(username_password)

    # The total number of tasks assigned to that user.
    number_of_tasks = 0
    if name in username_password:
        for i in task_list:
            if i['username'] == name:
                number_of_tasks += 1

    # The percentage of the total number of tasks that have been assigned to that user
    total_tasks = len(task_list)
    user_task_percentage = int((number_of_tasks/total_tasks)*100)

    # The percentage of the tasks assigned to that user that have been completed
    num_of_completed_tasks = 0
    for i in task_list:
            if i['username'] == name and i['completed'] is True:
                num_of_completed_tasks += 1
    user_tasks_completed_percentage = int((num_of_completed_tasks/number_of_tasks)*100)

    # The percentage of the tasks assigned to that user that must still be completed
    tasks_to_complete_percentage = 100 - user_tasks_completed_percentage

    # The percentage of the tasks assigned to that user that has not yet been completed and are overdue
    user_overdue_tasks = 0
    for i in task_list:
        if i['username'] == name and i['completed'] is False and i['due_date'] < today:
            user_overdue_tasks += 1

    user_overdue_percentage = int((user_overdue_tasks/number_of_tasks)*100)

    # Write to text file user_overview.txt to display the results in a user friendly way.
    with open('user_overview.txt', 'w') as file:
        file.write(f"Number of users registered: {users_registered}\n")
        file.write(f"Username: {name}\n")
        file.write(f"Number of assigned tasks: {number_of_tasks}\n")
        file.write(f"Percentage of tasks assigned to user: {user_task_percentage}%\n")
        file.write(f"Percentage of completed assigned tasks: {user_tasks_completed_percentage}%\n")
        file.write(f"Percentage of uncompleted assigned tasks: {tasks_to_complete_percentage}%\n")
        file.write(f"Percentage of overdue uncompleted assigned tasks: {user_overdue_percentage}%\n")


def display_statistics():
    '''Modify the menu option that allows the admin to display statistics so that the reports 
    generated are read from tasks.txt and user.txt and displayed on the screen in a user-friendly manner. 
    If these text files don’t exist (because the user hasn’t selected to generate them yet), 
    first call the code to generate the text files.'''

    # The objective to display contents of tasks.py is the same as the view_all function. 
    # If the file exists it will call view_all(), else create the text file.
    if os.path.exists('tasks.txt'):
        view_all()
    else:
        with open ('tasks.txt', 'w') as default_file:
            pass
    
    # Create user.txt file if it does not already exist. 
    """I am confused by this task objective as only an admin can access the ds option from the menu 
    and calling the display_statisics function. Therefore user.txt has to already exist in order for the 
    option to be accessed and the function called.

    I wonder if I am misunderstanding this task objective, and this function should actually 
    read from task_overview.txt and user_overview.txt, not task.txt and user.txt"""

    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    else:
        print(f"{border}\nUsername \t:\t Password\n{border}")
        for key, item in username_password.items():
            print(f"{key} \t\t:\t {item}")


# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


# A couple of global variables called several times throughout code.
border = "-"*50 # To separate text and improve readability of the code. 
today = datetime.today()

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print(f"{border}\nLOGIN\n{border}")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("\nUser does not exist.")
        continue
    elif username_password[curr_user] != curr_pass:
        print("\nIncorrect password.")
        continue
    else:
        print("\nLogin Successful!")
        logged_in = True

while True:
    # Presenting the menu to the user and making sure that the user input is converted to lower case.
    print(f"\n{border}")
    menu = input('''Select one of the following Options below:
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e  - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_results()
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

        display_statistics()

    # Displays to user why they are unable to select this option if they are not admin.
    elif menu == 'ds' and curr_user != 'admin': 
        print("\nOption only accessable to admin! Please select another.")

    elif menu == 'e':
        print(f'{border}\nGoodbye!!!\n{border}')
        exit()

    else:
        print("\nInvalid selection, please try again!")