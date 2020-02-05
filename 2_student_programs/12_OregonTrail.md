# Oregon Trail

|||
|---|---|
|Goal|Using variables, functions, and conditionals in Python, students will create an Oregon Trail game.|
|Required Reading| 0_python\00_variables.py|
||0_python\02_casting.py|
||0_python\03_comparison.py|
||0_python\04_input.py|
||0_python\05_if.py|
||0_python\06_while.py|
||0_python\07_for.py|
||0_python\08_list.py|
||0_python\09_dictionary.py*|
||0_python\10_functions.py|
||0_python\12_modules.py|
<sub>* = optional</sub>

## Details
We will be recreating Oregon Trail! The goal is to travel from NYC to Oregon (2000 miles) by Dec 31st. However, the trail is arduous. Each day costs you food and health. You can hunt and rest, but you have to get there before winter!

### Behavior
- Player starts in NYC on 03/01 with 2,000 miles to go, 500lbs of food, and 5 health.
- The player must get to Oregon by 12/31
- At the beginning of the game, user is asked their name.
- Each turn, the player is asked what action they choose, where the player can type in the following: travel, rest, hunt, status, help, quit
- Every day that passes, there should be a 5% chance that the player loses 1 health.
- The player eats 5lbs of food a day.
- Commands program accepts
    - travel: moves you randomly between 30-60 miles and takes 3-7 days (random).
    - rest: increases health 1 level (up to 5 maximum) and takes 2-5 days (random).
    - hunt: adds 100 lbs of food and takes 2-5 days (random).
    - status: lists food, health, distance traveled, and day.
    - help: lists all the commands.
    - quit: will end the game.
    - Any unknown command defaults to help

### Implementation Details
- Create functions for all options a player can take
- Use globals to keep track of player health, food pounds, miles to go, current day, current month
- Create a function add_day which updates the day
- Use global list to keep track of which months have 31 days and use this in the add_day function (i.e.: MONTHS_WITH_31_DAYS = [1, 3, 5, 7, 8, 10, 12])
- Here is one function that might be useful to you. You do not need to use it if you can figure out a workaround for it, but this will allow you to execute your add_day function a random number of times. Note that you need to have the add_day function created in order for this function to work, as it uses it.
```python
    def update_days(low_range, high_range):
        '''
            Adds a random number of days to your game.
            The number of days will be between the 
            two values specificed in the arguments.

            Inputs are the range you wan the random number of days to fall between.

            Output is the number of days that passed as an int.
        '''
        days = random.randint(low_range, high_range)
        for i in range(0, days):
            add_day()
        return days
```
- You will need to calculate a 5% chance that the health drops on a daily basis. You can accomplish this by creating another funciton that just takes a random number between 0-100 (for all percentage opportunities) and see if it's less than or equal to 5. 
```python
    def isHealthDecreased():
    '''
        The game rules state that:

        Every day that passes, there should be a 5% chance that the player loses 1 health, so get a random number between 1-100 and see if it's
        less than or equal to 5.

        Return true if health should decrease.
    '''
    return random.randint(1,100) <= 5
```
- The data you need to store for your application can be done in many ways. You could use individial variables.<br><br> Consider the scope of a global variable and that it needs to be declared in a funciton with the global keyword. <br><br>Using individual variables means you need to declare anything you would change.  <br>For example:
```python
total_trip_mileage = 2000
player_name =""
player_food = 500
player_health = 5
player_distance = 0

'''
    Using it in a function
'''
def travel():
    global total_trip_mileage
    global player_name
    global player_food
    global player_health
    global player_distance
    global player_info
```

- Using a dictionary, your code becmoes more compact and easier to use.<br><br>The dictionary structure allows you to contain all of the user information into one variable making it easier to gain access to it in a function. <br>For example:
```python
total_trip_mileage = 2000
player_info = {
    "name" : "",
    "food" : 500,
    "health" : 5,
    "distance" : 0
}

'''
    Using it in a function
'''
def travel():
    global player_info
```

- In the end, the choice is yours on how you want to proceed. If dictionary is just one more thing that confuses you, use individual variables. 
