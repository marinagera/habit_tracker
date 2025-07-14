import datetime
import uuid
from flask import Blueprint, current_app, render_template, request, redirect, url_for

pages = Blueprint("habits", __name__,
                  template_folder="templates", static_folder="static")


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff)
                 for diff in range(-3, 4)]
        return dates

    return {'date_range': date_range}


def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.route('/')
def index():
    date_str = request.args.get('date')
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()

    habits_on_date = current_app.db.habits.find({  # type: ignore[attr-defined]
        'added': {'$lte': selected_date}
    })

    completions = [
        habit['habit']
        for habit in current_app.db.completions.find({  # type: ignore[attr-defined]
            'date': selected_date
        })
    ]
    return render_template('index.html', habits=habits_on_date, title='Habit Tracker - Home', completions=completions, selected_date=selected_date)


@pages.route('/add', methods=['GET', 'POST'])
def add_habit():
    today = today_at_midnight()

    if request.method == 'POST':
        current_app.db.habits.insert_one({  # type: ignore[attr-defined]
            '_id': uuid.uuid4().hex,
            'added': today,
            'habit': request.form.get('habit')
        })

    return render_template('add_habit.html', title='Habit Tracker - Add Habit', selected_date=today)


@pages.route('/complete', methods=['POST'])
def complete():
    habit = request.form.get('habitId')
    date_str = request.form.get('date')

    if not habit or not date_str:
        return redirect(url_for('.index'))

    date = datetime.datetime.fromisoformat(date_str)
    current_app.db.completions.insert_one({  # type: ignore[attr-defined]
        'date': date,
        'habit': habit
    })

    return redirect(url_for('.index', date=date_str))
