from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

# path to the "database" text file
DATABASE_FILE = 'database.json'

# ensure the text file exists
def ensure_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'w') as db_file:
            json.dump([], db_file)  # initialize with an empty list

# load students from the text file
def load_students():
    with open(DATABASE_FILE, 'r') as db_file:
        return json.load(db_file)

# save students to the text file
def save_students(students):
    with open(DATABASE_FILE, 'w') as db_file:
        json.dump(students, db_file)

# home page to display the form and data
@app.route('/', methods=['GET', 'POST'])
def index():
    ensure_database()  # ensure the database file exists

    if request.method == 'POST':
        students = load_students()

        if 'add' in request.form:
            # add new student
            name = request.form['name']
            grade = int(request.form['grade'])
            student_id = max([student['id'] for student in students], default=0) + 1
            students.append({'id': student_id, 'name': name, 'grade': grade})

        elif 'update' in request.form:
            # update student data
            student_id = int(request.form['student_id'])
            new_grade = int(request.form['new_grade'])
            for student in students:
                if student['id'] == student_id:
                    student['grade'] = new_grade
                    break

        elif 'delete' in request.form:
            # delete student data
            student_id = int(request.form['student_id'])
            students = [student for student in students if student['id'] != student_id]

        save_students(students)

    # auery all students
    students = load_students()
    return render_template('Theindex.html', students=students)



if __name__ == '__main__':
    app.run(debug=True)
