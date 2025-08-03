from flask import render_template, request, redirect, url_for

from . import main_bp
from .services import get_recent_workouts, create_workout


@main_bp.route('/')
def home():
    workouts = get_recent_workouts()
    return render_template('home.html', workouts=workouts)


@main_bp.route('/workouts/add', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            create_workout(name)
            return redirect(url_for('main.home'))
    return render_template('add_workout.html')
