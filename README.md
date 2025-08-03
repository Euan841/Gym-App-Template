### Project Overview ###

This is a simple Flask web application for logging gym workouts. Currently, it only lets the user:

- View a list of recent workouts on the homepage
- Add a new workout using a basic form (currently just a string)
- Store and retrieve workouts using a SQLite database


### How it works ###

1. Example HomePage (/):

```
@main_bp.route('/')
def home():
    workouts = get_recent_workouts()
    return render_template('home.html', workouts=workouts)
```

This is the homepage of the app, it returns a list of the worksouts (currently strings). 

When you go to your running application (http://127.0.0.1:5000/) it calls this route. This does two things 
a) Calls get_recent_workouts (defined in services.py) which returns a list of items from the databsae

```
def get_recent_workouts(limit=10):
    database = db.get_db()
    return database.execute(
        'SELECT id, name, date FROM workouts ORDER BY date DESC LIMIT ?',
        (limit,)
    ).fetchall()
```

b) it calls render_template - this is a flask method that takes the html - 
this is defined in templates/home.html and passes in the workouts object we got from the call above. 

```
{% extends 'base.html' %}

{% block content %}
<h1>Recent Workouts</h1>
<ul>
    {% for workout in workouts %}
        <li>{{ workout['name'] }} - {{ workout['date'] }}</li>
    {% else %}
        <li>No workouts yet</li>
    {% endfor %}
</ul>
{% endblock %}
```

The html can render conditionally here - i.e. it is looping through the worksouts

```{% for workout in workouts %}```

2. Workouts/add

```
@main_bp.route('/workouts/add', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            create_workout(name)
            return redirect(url_for('main.home'))
    return render_template('add_workout.html')
```
This is the second route, this is triggered when you go to (http://127.0.0.1:5000/workout/add) - the methods are GET and POST,
when we go to the site this calls GET and when we submit the form it calls POST - this function checks if it's POST and then calls
create_workout (in services.py) to create the workout then sends the user back to the homepage (where it can be seen)

When we go to http://127.0.0.1:5000/workout/add it skips the POST part (as it will be a GET call) so jumps straight ot render_template(add_workout.html)

```
{% extends 'base.html' %}

{% block content %}
<h1>Add Workout</h1>
<form method="post">
    <label for="name">Workout Name</label>
    <input type="text" id="name" name="name" required>
    <button type="submit">Add</button>
</form>
{% endblock %}
```
We can see here this has a form with method="post" this means when we submit the 
form by pressing the button it will call that endpoint above but with POST. 

When you have a form with POST it will send the contents of the form to that endpoint. 
So if you wanted to add say "category" or "date" to workout you'd add to the form and
then process this in the route (e.g. add a line under name to get date)

### Folder Structure ###
```
gym_app/
│
├── app/
│   ├── __init__.py           # Setup (Ignore for now)
│   ├── db.py                 # Setup DB, to change the DB tables exit the schema in init_db() 
|                               (you will need to delete the data.db or manually drop the table to make changes)
│
│   ├── main/                 # Main feature: 
│   │   ├── __init__.py       # Setup (Ignore for now) 
│   │   ├── routes.py         # Route handlers (handles when you go to e.g. workout/add or if you add new routes)
│   │   └── services.py       # All logic and DB queries - routes call service functions to get or send data to/from DB
│
│   ├── templates/            # HTML templates
│   │   ├── base.html         #Defines the navbar at the top so you can click between pages - if you make a new page add to navbar here
│   │   ├── home.html         #Home Page
│   │   └── add_workout.html  #Page to add_workout
│
│   └── static/               # Static assets (optional CSS/JS/images)
│       └── style.css         # Basic styling applied everywhere (imported in base.html) 
|                             # You can make page specific styling files in here 
|                             e.g. home.css and import in the same way on that file
│
├── run.py                    # How to run (python or python3 run.py) 
├── data.db                   # Database - delete to delete all tables
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

### How to run / Develop ###

1. Install dependencies
```pip install -r requirements.txt``` or ```pip3 install -r requirements.txt```

2. Run code (recommended in IDE)
In VScode or Pycharm (recommended) just run - run.py

In the terminal python (or python3) run.py

Check you can access it on the url provided. 

### Tasks ###
This is a series of tasks to make the app work and improve functionality. 
After each task is complete, commit the code and push to your repo.

**Task 1 - Setup**  
First check you can run the code as above ^ then setup your git repo - this can be an new empty public repo for now.

Remove the origin (my repo)   
```git remote remove origin```

Add your repo as the new origin   
```git remote add origin https://github.com/{username}/newRepo.git```

Ensure you are on main branch   
```git branch -M main```

Push to origin (this will overwrite the empty main branch)   
```git push -u origin main --force```

Check this repo is now present in your github


**Task 2 - Update Add Workout**
Currently each workout is simply a name and a date. 
Your task here is to add some more fields here - this could be 
- type: Push / Pull / Legs ETC
- duration

**Commit with message "GymApp-2 Updated add workout"**


<details>
<summary>Hint: How to get started</summary>

You’ll need to:
- Add new fields to the DB config (db.py)
- Add new fields to the HTML form (templates/add_workout.html)
- Update the Flask route to read the new data (Look at `name = request.form.get('name')`)
- Update the `create_workout()` function to accept more than just name
- Pass them to your `create_workout()` function and ensure they go into the database
- Display this new data on the home pagetempalte , currently just name and date `<li>{{ workout['name'] }} - {{ workout['date'] }}</li>`

</details>



**Task 3 – Add Exercise**    
As each workout is made up of a number of exercises we will now need to create a way 
to store all the exercises. 

Your tasks: 
- Create a new table in the DB (this only needs an id and name)
- Create a html template /exercise/add with a simple form 
  - Use the add_workout page as example as this is very similar to how it will work
- Create a new function in services.py to create a new exercise (INSERT INTO DB etc)
- Create a new route in routes.py (/exercise/add) (GET AND POST like workouts)
  - This means when the user goes to the URL they get the template
  - When they submit the form it will call post and add the exercise

**Commit with message "GymApp-3 Add exercise"**


**Task 4 - Display exercises**    
Now we can create exercises we want to display them, so create a page to show all the exercises.

Your tasks: 
- Create a new template for exercises
- Create a function (services.py) to return all the exercises
- Create a new route (GET ONLY) for /exercises
  - The route will pass in the exercises returned from your new function into the template engine (look at home.html for example - we pass in the workouts)

**Commit with message "GymApp-4 Display exercises"**

**Task 5 - Link Workout and Exercise**   
Now we need to link the exercises to the workouts. Each workout has many exercises so this is a many to one relationship. 

Your task: 
- Create a table (workout_exercises or similar) with an id, two foreign keys (workout_id and exercise_id), sets (integer), weight(float/real)

(Remember if the DB isn't working as you expect you may need to delete the data.db and rerun run.py)

**Commit with message "GymApp-5 Create new link table for exercise and workout"**

**Task 6 - (more difficult) Link exercises to the add workout page**    
Now we need to bring together the user interfaces

Your tasks:
- In your add workout page, you must now pass in the exercises (similar to your /exercises page from task 4)
- Then loop through and display each exercise
  - For each exercise add a checkbox to say if the exercise was done
  - If the checkbox is ticked then display two other fields (sets and weight)
- Remember to include all of this inside your form so it can all be submitted.

In order to track how many sets/weight per exercise you need to set the name in the inputs here, 
otherwise when you go to process the workout you won't know which set/weight correspond to which exercise. 
```
<label>
  <input type="checkbox" name="exercise_{{ exercise.id }}">
  {{ exercise.name }}
</label>
<input type="number" name="sets_{{ exercise.id }}" placeholder="Sets">
<input type="number" name="weights_{{ exercise.id }}" placeholder="Weight">
```

**Commit with message "GymApp-6 Link together workout and exercise"**

**Task 7 - Process the exercises for each workout**    
Now we can specify which exercises we did in a workout we need to add these to the database.

Your tasks:
- Update the route to parse in all the exercises
- Update the function `def create_workout(name):`
  - to first create the workout (e.g. name, date, difficulty)
  - Take the workout ID (just created)
  - Iterate through the exercises (the ones ticked on the form) and insert into your new table (workout_exercises)

**Commit with message "GymApp-7 Process workout exercises"**

**Task 8 - View a workout**   
Now that a workout contains some useful data we need to create a page to visualise this.

Your tasks: 
- Create a new template that takes in a workout, and all related exercises and displays them
- Create a new function (services.py) that returns all exercises when given a workoutID
- Create a new function (services.py) that returns workout information when given a workoutID
- Create a new route /workout/<int:id> (find out how to parse data from the url to get the id)
  - This can be GET only
  - It should return the template, and pass in the workout and exercises list
- Update the home.html so that each workout (when clicked) links to their workout page
  - use HREF on the `<li>{{ workout['name'] }} - {{ workout['date'] }}</li>`
  - e.g. `<a href="{{ url_for('main.workout_detail', id=workout['id']) }}">`

**Commit with message "GymApp-8 View workout"**

### Further Development ###
You now have an app that has basic working functionality, below are a list of improvements you could make to make this 
app ready to be used on a public github e.g. for job applications. 

**CSS Styling**   
The app lacks any real styling right now, this can be done with the style.css or by creating page specific styling e.g. home.css

**Expanding Sets**   
You don't always do the same weight for each set so instead of passing in a number for set you could create a new table that would contain e.g. id, (weight, reps) meaning you can store more data.

**Validation**  
The app has no validation, ensure that data coming in is valid e.g. weight: 80 and not 'eighty' as this would break

**Error handling**   
If your database or any other components encounter an error it just returns status code 500 (internal server error.    
It is a much better practice to use try/catch to return meaningful codes e.g. 400 bad request (if the input data is wrong)

**More functionality**    
- Currently, you can't edit or delete workouts or exercises
- You could update the exercise page to have a graph that shows hows the weight has increased over time
- Create workout_plans (e.g. pull) which provide a template when creating a workout (instead of having to tickbox everyone)
  - You can also switch from display them to all to a +add exercises with a dropdown to select the exercise


