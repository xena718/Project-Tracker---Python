"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project-tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    # row = db_cursor.fetchone() #row is tuple with three.
    first_name, last_name, github = db_cursor.fetchone()

    print(f"Student: {first_name} {last_name}\nGitHub account: {github}")


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO students (first_name, last_name, github)
          VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})
    db.session.commit()

    print(f"Successfully added student: {first_name} {last_name}")


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT *
        FROM projects
        where title = :title
        """

    db_cursor = db.session.execute(QUERY, { 'title' : title })

    id, title, description, max_grade = db_cursor.fetchone()

    db.session.execute(QUERY, {'title': title })

    print(f"Project info: id is {id}, title is {title}, description is {description}, max grade is {max_grade}")



def get_grade_by_github_title(student_github, project_title):
    """Print grade student received for a project."""
    # jhacks	Markov	10
    QUERY = """
        SELECT project_title, grade
        FROM grades
        WHERE student_github = :student_github
        AND project_title = :project_title
        """

    # db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})
    db_cursor = db.session.execute(QUERY, {'student_github': student_github, 'project_title': project_title})

    # row = db_cursor.fetchone() #row is tuple with three.
    project_title, grade = db_cursor.fetchone()

    print(f"The student with project of {project_title} has a a grade of {grade}")


def assign_grade(student_github, project_title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    # jhacks	Markov	10

    QUERY = """
        INSERT INTO grades (student_github, project_title, grade)
        VALUES (:student_github, :project_title, :grade)
          """

    db_cursor = db.session.execute(QUERY, {'student_github': student_github,
                                        'project_title': project_title,
                                        'grade': grade})

    db.session.commit()


    project_title, student_github, grade = db_cursor.fetchone()

    print(f"""Confirming that the student with github id of {student_github} 
    has been assigned with a grade of {grade} for project {project_title}""")



def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    # handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
