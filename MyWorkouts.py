import sqlite3
import json




conn = sqlite3.connect('MyWorkouts.db')

c = conn.cursor()




def opening_screen():
    print("Workout Inventory System")
    print("1. Add a new exercise")
    print("2. View all exercises")
    print("3. Update exercise details")
    print("4. Delete an exercise")
    print("6. Exit")
    valid = False
    while not valid:
        choice = input('>')
        if choice.isdigit():
            choice = int(choice)
            if choice < 1 or choice > 6:
                print('Invalid number chose again')
            else:
                valid = True
    return choice



def exercse_checker(name):
    with open("data.json", "r") as f:
        data = json.loads(f.read())

    exercises = data["exercises"]

    for exercise in exercises:
        if exercise["name"] == name:
            return exercise["muscle_group"]

    return None

def equipment_getter(name):
    with open("data.json", "r") as f:
        data = json.loads(f.read())

    exercises = data["exercises"]

    for exercise in exercises:
        if exercise["name"] == name:
            return exercise["equipment"]

    return []


def info_checker(info):
    val = False
    while not val:
        print(f'You entered {info}.')
        print('Does this look right (Y/N)')
        yn = input('>')
        if yn.upper() == 'Y' or yn.upper() == 'N':
            val = True
    if yn.upper() == 'N':
        print('Enter what you meant')
        info = input('>').upper()
        return info_checker(info)

    return info


def add_exercise(num):
    if num == 1:
        name = input('What is the name of the exercise you would like to add').upper()
        name = info_checker(name)
        muscle = exercse_checker(name)
        if muscle is None:
            print(f'We do not have {name} on file yet.')
            muscle = input('What is the primary mover in the exercise')
            equipment = input('Enter the equipment used for this exercise').upper()
            equipment = info_checker(equipment)
        else:
            print(f'Great we have {name} on file.')
            print(f'The muscle worked is {muscle}')

            val = False
            while not val:
                print('Does that muscle worked look right?(Y/N)')
                yn = input('>')
                if yn.upper() == 'Y' or yn.upper() == 'N':
                    val = True
            if yn.upper() == 'N':
                print('What is the primary mover in the exercise')
                muscle = input('>')
                muscle = info_checker(muscle)

            print('Which equipment did you use:')
            stuffs = equipment_getter(name)

            i = 1
            for stuff in stuffs:
                print(f"{i}.{stuff}", end=' ')
                i = i + 1

            val = False
            while not val:
                print('\nDid you use any of the equipment listed above (Y/N)?')
                yn = input('>')
                if yn.upper() == 'Y' or yn.upper() == 'N':
                    val = True

            if yn.upper() == 'N':
                print('What equipment did you use?')
                equipment = input('>')
                equipment = info_checker(muscle)
            else:

                valid = False
                while not valid:
                    eq = input('Enter the number beside the equipment you used')
                    if eq.isdigit():
                        eq= int(eq)
                        if eq < 1 or eq > len(stuffs):
                            print('Invalid number chose again')
                        else:
                            valid = True
                            equipment = stuffs[eq - 1]

        valid = False
        while not valid:
            rating = input('How would you rate your experience with the movement? Ratings between 1-5')
            if rating.isdigit():
                rating = int(rating)
                if rating < 1 or rating > 5:
                    print('Invalid rating chose again')
                else:
                    valid = True
        weight = input('What is the most recent weight you have lifter with this movement')
        weight = info_checker(weight)


        c.execute("INSERT INTO workouts VALUES(?,?,?,?,?)", (name.upper(),muscle.upper(),rating,weight, equipment.upper()))
        conn.commit()


        print('You have succesfully added',name.upper(),'to your workout list')




def view_all(num):
    if num == 2:
        val = False
        while not val:
            print('Would you like to filter your results (Y/N)')
            yn = input('>')
            if yn.upper() == 'Y' or yn.upper() == 'N':
                val = True

        if yn.upper() == 'Y':
            print('Filter by:')
            print('1.Muscle group')
            print('2.Rating')
            print('3.Equipment used')
            print('4.Go Back')
            sel = input('>')
            if int(sel) == 1:
                print('Enter the name of the muscle group you would like to filter by.')
                x = input('>')
                x = x.upper()
                c.execute("SELECT * FROM workouts WHERE muscle_worked =?", (x,))
                items = c.fetchall()
                print(f'             Here are your workouts ({x.upper()} only):                  ')



                print("-" * 70)
                print(f"{'Exercise':<25}{'Muscle Group':<15}{'Rating':<10}{'Weight':<10}{'Equipment'}")
                print("-" * 70)

                # Data Rows
                for item in items:
                    print(f"{item[0]:<25}{item[1]:<15}{item[2]} stars   {item[3]}lbs  {item[4]}")


            elif int(sel) == 2:
                print('Enter the rating you are searching for (1-5)')
                x = input('>')
                x = int(x)
                c.execute("SELECT * FROM workouts WHERE rating = ?", (x,))
                items = c.fetchall()
                print(f'             Here are your workouts ({x} stars only):                  ')


                # Header

                print("-" * 70)
                print(f"{'Exercise':<25}{'Muscle Group':<15}{'Rating':<10}{'Weight':<10}{'Equipment'}")
                print("-" * 70)

                # Data Rows
                for item in items:
                    print(f"{item[0]:<25}{item[1]:<15}{item[2]} stars   {item[3]}lbs  {item[4]}")

            elif int(sel) == 3:
                print('Enter the equipment you would like to filter by')
                x = input('>')
                x = x.upper()
                c.execute("SELECT * FROM workouts WHERE equipment = ?", (x,))
                items = c.fetchall()
                print(f'             Here are your workouts ({x} only):                  ')


                # Header

                print("-" * 70)
                print(f"{'Exercise':<25}{'Muscle Group':<15}{'Rating':<10}{'Weight':<10}{'Equipment'}")
                print("-" * 70)

                # Data Rows
                for item in items:
                    print(f"{item[0]:<25}{item[1]:<15}{item[2]} stars   {item[3]}lbs  {item[4]}")

        elif yn.upper() ==  'N':
            c.execute("SELECT * FROM workouts")
            items = c.fetchall()


            # Header
            print("\n                  Here are all your workouts:")
            print("-" * 70)
            print(f"{'Exercise':<25}{'Muscle Group':<15}{'Rating':<10}{'Weight':<10}{'Equipment'}")
            print("-" * 70)

            # Data Rows
            for item in items:
                print(f"{item[0]:<25}{item[1]:<15}{item[2]} stars   {item[3]}lbs  {item[4]}")

def delete_exercise(num):
    if num == 4:
        c.execute("SELECT * FROM workouts")
        items = c.fetchall()
        print("\n                  Here are all your workouts:")
        print("-" * 70)
        print(f"{'Exercise':<25}{'Muscle Group':<15}{'Rating':<10}{'Weight':<10}{'Equipment'}")
        print("-" * 70)

        # Data Rows
        for item in items:
            print(f"{item[0]:<25}{item[1]:<15}{item[2]} stars   {item[3]}lbs  {item[4]}")

        print('Enter the name of the exercise you would like to delete.')
        ans  = input('>')
        ans = ans.upper()
        print('Enter the name of the equipment you used for this exercise.')
        eq = input('>')
        eq = eq.upper()
        c.execute("SELECT * FROM workouts WHERE exercise_name = ? AND equipment = ? ", (ans,eq))

        if len(c.fetchall()) == 0:
            print(f'{ans} is not in your inventory')
        else:
            c.execute("DELETE from workouts WHERE exercise_name = ? AND equipment = ? ", (ans,eq))
            print(f'{eq} {ans} has been deleted from your inventory')


def update_details(num):
    if num == 3:
        isvalid = False

        while not isvalid:
            c.execute("SELECT * FROM workouts")
            items = c.fetchall()
            print("\n                  Here are all your workouts:")
            print("-" * 70)
            print(f"{'Exercise':<25}{'Muscle Group':<15}{'Rating':<10}{'Weight':<10}{'Equipment'}")
            print("-" * 70)

            # Data Rows
            for item in items:
                print(f"{item[0]:<25}{item[1]:<15}{item[2]} stars   {item[3]}lbs  {item[4]}")

            print('Enter the name exercise you would like to update')
            ex = input('>').upper()
            info_checker(ex)
            print('Enter the equipment used for this exercise')
            eq = input('>').upper()
            info_checker(eq)

            c.execute("SELECT * FROM workouts WHERE exercise_name = ? AND equipment = ?",(ex,eq))
            items = c.fetchall()

            if len(items) == 1:
                isvalid = True
                for item in items:
                    print(f'You have selected {item[4]} {item[0]}')

                    upd = {'Name': 'exercise_name', 'muscle worked': 'muscle_worked', 'rating': 'rating',
                           'weight lifted': 'weight', 'equipment used': 'equipment'}

                    i = 1
                    for value in upd:
                        print(f'{i}. {value}', end=' ')
                        i = i + 1

                    choice = input('\n>')
                    choice = int(choice)

                    values = list(upd.values())
                    keys = list(upd.keys())


                    print(f'What would you like to change the {keys[choice - 1]} to ?')
                    change = input(">").upper()
                    info_checker(change)

                    c.execute(f"UPDATE workouts SET {values[choice - 1]} = ? WHERE exercise_name = ? AND equipment = ?",
                              (change, ex, eq))

                    print(f'You have successfully changed the {keys[choice -1]} to {change}')

            else:
                print('The exercise you entered does not exist.')
                print('Would you like to exit and add it to inventory or try again?')
                print('Enter X to exit or any other key to try again.')
                inu = input('>').upper()
                if inu == 'X':
                    break





def main():
    on = True
    while on:
        num = opening_screen()
        add_exercise(num)
        view_all(num)
        delete_exercise(num)
        update_details(num)


        if num == 6:
            print("Exiting Workout Inventory System...")
            on = False

        if num !=6:
            input('Press any key to go back to the menu')

        conn.commit()

main()
conn.close()