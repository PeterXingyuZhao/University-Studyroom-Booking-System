# Run a local demo

[← Project overview](../README.md)

These instructions are derived from the checked-in settings, models, migrations, and URL configuration. The source was created with **Django 5.0.6**. The setup below uses that historical version with Python 3.11 to reproduce the course project locally; a fresh installation has not yet been runtime-verified.

## 1. Prepare the environment

The shell commands below use macOS/Linux syntax.

```bash
git clone https://github.com/PeterXingyuZhao/University-Studyroom-Booking-System.git
cd University-Studyroom-Booking-System
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install Django==5.0.6 django-formtools==2.5.1 django-extensions==3.2.3
cd Studyroom_Booking_Code
export PYTHONPATH="$PWD/dj-booking-main${PYTHONPATH:+:$PYTHONPATH}"
```

The last line exposes the bundled `booking` package, which the project settings and URL configuration import. Run it from `Studyroom_Booking_Code/` again when starting a new terminal session. The bundled package's own `requirements.txt` belongs to that third-party package and is not an application dependency lockfile.

## 2. Create a fresh database

Work in a disposable local copy. **Preserve the included `db.sqlite3` in a backup location outside the working `Studyroom_Booking_Code/` directory before continuing.** Once the working directory has no database file, the migrations below create a fresh database; no existing accounts or records are needed.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

Open **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)** and sign in with the superuser account you just created.

## 3. Add a small example

1. Add a **Student** with a demo student ID, name, password, and major. Saving the record creates its Django user; the student ID is the login name. Use disposable demo credentials: the original `Student` model retains a password field separately from Django's hashed authentication password.
2. Add a **Profile** for that newly created user and select the `Student` user type. Profiles are not created automatically, and the room listing requires one.
3. Add a **Classroom**, such as `A101`, with a floor, capacity, and a JSON equipment list such as `["projector", "whiteboard"]`. Leave its meeting-room flag unset for the student example.
4. Add a **Time** with a date and a time-slot label such as `09:00–10:00`. A room–time availability record is created automatically by the application's model signals.
5. Sign out of the admin account. Open **[http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)** and sign in with the demo student ID.

Follow **Go Booking! → View Details → Make Reservation**. Check **My Bookings**, cancel the reservation, and return to the time slot to see the room available again. Searching for `projector, whiteboard` requires both equipment items, with exact, case-sensitive names.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `No module named 'booking'` | Set `PYTHONPATH` as above from the directory containing `manage.py`. |
| Missing `Profile` when opening a time slot | Create a `Profile` in Django Admin for the student's linked user. |
| No rooms appear | Add a classroom and time; check the corresponding room–time availability record. Student profiles do not see meeting rooms. |
| A 404 at the root URL | Start at `/login/` or `/admin/`; `/` has no route. |
| A faculty account cannot book | The current booking/profile views still require a `Student` record; profile types alone do not provide a separate faculty account flow. |

The original project uses development settings and a mutable availability flag. It is intended for a local course demonstration; see [project scope](../README.md#project-scope) for the implementation's current limits.
