# Project Dashboard App
Remote assignment backend of DevSecurity

## Run the project locally

Stack requirements:<br>
<li>Python3+</li>
<li>PostgreSQL</li><br>

**1** - Clone the repository
```bash
    git clone git@github.com:Edmond22-prog/project-dashboard-app.git
```

**2** - Enter to the repository, create and activate the virtual environment
```bash
    cd project-dashboard-app/

    python -m venv .venv

    # Linux
    source .venv/bin/activate

    # Windows
    source .venv/Scripts/activate
```

**3** - Install the requirements
```bash
    pip install -r requirements.txt
```

**4** - Create a .env in the root directory, from the .env.example and fill information about your created database
```text
    # Postgres db config
    DATABASE_ENGINE=django.db.backends.postgresql
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    DATABASE_NAME=<your_database_name>
    DATABASE_USER=<your_database_user>
    DATABASE_USER_PASSWORD=<your_database_user_password>
```

**5** - Migrate the database
```bash
    python manage.py migrate
```

**6** - Load test data to the database
```bash
    python load_test_data.py
```

**7** - Run the server
```bash
    python manage.py runserver
```

**8** - Go to the link http://127.0.0.1:8000/api/v1/docs in your browser.<br>
You can create a new user, or login with credentials:

**username**: john_dev<br>
**password**: password123


## Run the project with docker compose

Stack requirements:<br>
<li>Docker</li>
<li>Docker Compose</li><br>

**1** - Clone the repository
```bash
    git clone git@github.com:Edmond22-prog/project-dashboard-app.git
```

**2** - Enter to the repository
```bash
    cd project-dashboard-app/
```

**3** - Run docker command
```bash
    docker compose up --build
```

**4** - Go to the link http://127.0.0.1:8000/api/v1/docs in your browser.<br>
You can create a new user, or login with credentials:

**username**: john_dev<br>
**password**: password123


## How much time you spent on this assignment and what you did/didn't like?
```text
    It took me almost 5 days to fully complete the rendering.
```

## What would you have done differently if you had had more time?
```text
    If I had more time, I would have configured user access differently so that they could or could not perform actions on objects that do not belong to them (projects, tasks)
```

## With which parts of your application are you satisfied?
```text
    I am satisfied with the project architecture, as it separates the core business from the Framework, thus facilitating migration. But I am also satisfied with the security of my APIs, particularly with the verification of the user making the requests.
```

## Which parts would need improvement?
```text
    There should be an improvement at the task level. It would be necessary to change the status of a task when starting or stopping the timer for a task. It will also be necessary to allow each user to see all projects and tasks, without being able to modify them.
```