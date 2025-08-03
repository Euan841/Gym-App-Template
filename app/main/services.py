from .. import db


def get_recent_workouts(limit=10):
    database = db.get_db()
    return database.execute(
        'SELECT id, name, date FROM workouts ORDER BY date DESC LIMIT ?',
        (limit,)
    ).fetchall()


def create_workout(name):
    database = db.get_db()
    database.execute(
        'INSERT INTO workouts (name) VALUES (?)',
        (name,)
    )
    database.commit()
