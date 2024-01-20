from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file, Response
from flask import flash
import csv
import io
import sqlite3

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'your_secret_key'


# ############### Function to connect to the SQLite database  ###############
def connect_db():
    return sqlite3.connect('database.db')

# ############### Route for the login page #######################################
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# ####################################### Route for the dashboard (requires login) #######################################
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM PersonalInformation')
    total_count = cursor.fetchone()[0]

    conn.close()

    return render_template('dashboard.html',total_count=total_count, username=session['username'])

# Route to add a new student record
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()

        # Retrieve form data
        # (Modify this part to get data from the form)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']
        emergency_contact = request.form['emergency_contact']


        # ... (retrieve other fields)
        # Insert data into AcademicInformation table

        department = request.form['department']
        Mathematics = request.form['Mathematics']
        English = request.form['English']
        Chemistry = request.form['Chemistry']
        Physics = request.form['Physics']
        Biology = request.form['Biology']
        Computer = request.form['Computer']
        Commerce = request.form['Commerce']
        Acccounting = request.form['Acccounting']
        Literature = request.form['Literature']
        Government = request.form['Government']
        Economic = request.form['Economic']
        year_grade = int(request.form['year_grade'])


        # Insert data into Administartive Information table

        admission_date = request.form['admission_date']
        advisor_guardian = request.form['advisor_guardian']
        tuition_fees = request.form['tuition_fees']
        payments = request.form['payments']
        class_attendance = request.form['class_attendance']
        absence = request.form['absence']
        tardiness = request.form['tardiness']

        

        conn.commit()  # Commit changes to the database

        # Insert new record into PersonalInformation table
        cursor.execute('''
            INSERT INTO PersonalInformation (first_name, last_name, middle_name, date_of_birth, gender, phone_number, address, emergency_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, middle_name, date_of_birth, gender, phone_number, address, emergency_contact))


        # Insert new record into  AcademicInformation table
        cursor.execute('''
            INSERT INTO AcademicInformation 
            (department, Mathematics, English, Chemistry, Physics, Biology, Computer, Commerce, Acccounting, Literature, Government, Economic, year_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (department, Mathematics, English, Chemistry, Physics, Biology, Computer, Commerce, Acccounting, Literature, Government, Economic, year_grade))


        # Insert new record into  AdministrativeInformation table

        cursor.execute('''
            INSERT INTO AdministrativeInformation 
            (admission_date, advisor_guardian, tuition_fees, payments, class_attendance, absence, tardiness)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (admission_date, advisor_guardian, tuition_fees, payments, class_attendance, absence, tardiness))


        conn.commit()
        conn.close()

         # Send the transaction message to result.html
        flash('Record successfully added to database', 'success')  # Flash success message
         # Send the transaction message to view.html
        return redirect(url_for('view_students'))

        
    return render_template('add_student.html')

# ############### Route to view Transaction result ###############
@app.route("/result")
def result():
    return render_template("result.html")

# ############### Route to search for students ###############
@app.route('/search_students', methods=['GET'])
def search_students():
    search_query = request.args.get('search_query', '')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM PersonalInformation WHERE student_id LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR middle_name LIKE ?', ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    searched_students = cursor.fetchall()

    conn.close()

    no_results_message = ""  # Initialize no_results_message with an empty string

    if not searched_students:  # If no results found
        no_results_message = "No records found for the search query."


    return render_template('search_results.html', searched_students=searched_students, search_query=search_query, no_results_message=no_results_message)

# ############### Route to download records as CSV ###############
@app.route('/download_records')
def download_records():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM PersonalInformation INNER JOIN AcademicInformation ON PersonalInformation.student_id = AcademicInformation.student_id INNER JOIN AdministrativeInformation ON PersonalInformation.student_id = AdministrativeInformation.student_id')
    data = cursor.fetchall()

    conn.close()

    # Prepare data for CSV file
    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow([i[0] for i in cursor.description])  # Write headers
    csv_writer.writerows(data)

  # Create a response object to send the CSV file
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=student_data.csv'}
    )

    # return response
# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Route to view all student records
@app.route('/view_students')
def view_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM PersonalInformation')
    students = cursor.fetchall()

    conn.close()
    return render_template('view_students.html', students=students)


# Route to edit a student record
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Retrieve updated data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']
        emergency_contact = request.form['emergency_contact']
        # Update other fields similarly

        # Update the database with the new data
        cursor.execute('''
            UPDATE PersonalInformation
            SET first_name = ?, last_name = ?, middle_name = ?, date_of_birth = ?, gender = ?, phone_number = ?, address = ?, emergency_contact = ?
            WHERE student_id = ?
        ''', (first_name, last_name, middle_name, date_of_birth, gender, phone_number, address, emergency_contact, student_id))



        conn.commit()
        conn.close()

         # Send the transaction message to result.html
        flash('Record successfully updated in database', 'success')  # Flash success message
        return redirect(url_for('view_students'))  # Redirect to the same edit page

    cursor.execute('SELECT * FROM PersonalInformation WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()

    conn.close()
    return render_template('edit_student.html', student=student)




# ##################ACADEMIC INFORMATION #######################

@app.route('/academic_Information', methods=['GET'])
def academic_Information():
    conn = connect_db()
    cursor = conn.cursor()
    # Fetch data from the database
    cursor.execute('SELECT * FROM AcademicInformation')
    records = cursor.fetchall()

    return render_template('academic_Information.html', records=records)


# Route to edit a specific student for academic information
@app.route('/edit_acadInfo/<int:student_id>', methods=['GET', 'POST'])
def edit_acadInfo(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch student data based on the ID
   
    if request.method == 'POST':
        # Update the data with the new values from the form
        department = request.form['department']
        Mathematics = request.form['Mathematics']
        English = request.form['English']
        Chemistry = request.form['Chemistry']
        Physics = request.form['Physics']
        Biology = request.form['Biology']
        Computer = request.form['Computer']
        Commerce = request.form['Commerce']
        Acccounting = request.form['Acccounting']
        Literature = request.form['Literature']
        Government = request.form['Government']
        Economic = request.form['Economic']
        
        # Update other subjects here...
        year_grade = int(request.form['year_grade'])
        # Ideally, here you would update your database with the new values

      
        cursor.execute('''
                       
            UPDATE AcademicInformation 
            SET department = ?, Mathematics = ?, English = ?, Chemistry = ?, Physics = ?,
            Biology = ?, Computer = ?, Commerce = ?, Acccounting = ?, Literature = ?,
            Government = ?, Economic = ?, year_grade = ?
            WHERE student_id = ?
        ''', (department, Mathematics, English, Chemistry, Physics, Biology, Computer, Commerce, Acccounting, Literature, Government, Economic, year_grade, student_id))

        # msg = "Record successfully Updated to database"

        conn.commit()
        conn.close()

         # Send the transaction message to result.html
        flash('Record successfully updated in database', 'success')  # Flash success message
        return redirect(url_for('academic_Information'))  # Redirect to the same edit page

    cursor.execute('SELECT * FROM AcademicInformation WHERE student_id = ?', (student_id,))
    student_data = cursor.fetchone() 
    
    conn.close()
    return render_template('edit_acadInfo.html', student_data=student_data)


# Route to display the data in Administrative Information an animated Bootstrap table
@app.route('/view_admininfo', methods=['GET'])
def view_admininfo():
    conn = connect_db()
    cursor = conn.cursor()
    # Fetch data from the database
    cursor.execute('SELECT * FROM AdministrativeInformation')
    student_data = cursor.fetchall()

    return render_template('view_admininfo.html', student_data=student_data)


# Route to edit a specific student for Adminitrative information
@app.route('/edit_adminInfo/<int:student_id>', methods=['GET', 'POST'])
def edit_adminInfo(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch student data based on the ID
   
    if request.method == 'POST':
        # Retrieve updated data from the form
        admission_date = request.form['admission_date']
        advisor_guardian = request.form['advisor_guardian']
        tuition_fees = request.form['tuition_fees']
        payments = request.form['payments']
        class_attendance = request.form['class_attendance']
        absence = request.form['absence']
        tardiness = request.form['tardiness']

        cursor.execute('''
            UPDATE AdministrativeInformation 
            SET admission_date = ?, advisor_guardian = ?, tuition_fees = ?, payments = ?, class_attendance = ?, absence = ?, tardiness = ?
            WHERE student_id  = ?
        ''', (admission_date, advisor_guardian, tuition_fees, payments, class_attendance, absence, tardiness, student_id))

        # msg = "Record successfully Updated to database"

        conn.commit()
        conn.close()
        # flash("Administrative Information Successfully Updated!", "success")
        # Send the transaction message to result.html
        flash('Student Information Successfully Updated!', 'success')  # Flash success message
        return redirect(url_for('view_admininfo'))  # Redirect to the same edit page

    cursor.execute('SELECT * FROM AdministrativeInformation WHERE student_id = ?', (student_id,))
    student_data = cursor.fetchone() 
    
    conn.close()
    return render_template('edit_adminInfo.html', student_data=student_data)

    # return render_template('edit_adminInfo.html', )


@app.route('/delete_student/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete the student from all related tables based on their primary key
    cursor.execute('DELETE FROM PersonalInformation WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM AcademicInformation WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM AdministrativeInformation WHERE student_id = ?', (student_id,))

    conn.commit()
    conn.close()

    # Send the transaction message to result.html
    flash('Record Successfully Deleted in database', 'success')  # Flash success message
    return redirect(url_for('view_students'))  # Redirect to the same edit page

    # return redirect('/')  # Redirect back to the view_students page or any appropriate page

# Render the initial HTML page with the search bar
@app.route('/view_results')
def view_results():
    return render_template('view_results.html')


def calculate_percentage(scores):
    total_score = sum(scores)  # Calculate total score from subject scores
    percentage = (total_score / 700) * 100
    return round(percentage, 2)








# Function to fetch selected columns and calculate percentage score for each student
def fetch_selected_columns_with_percentage():
    conn = connect_db()
    cursor = conn.cursor()

    # Columns you want to fetch
    selected_columns = [
        'student_id', 'department', 'Mathematics', 'English', 'Chemistry', 
        'Physics', 'Biology', 'Computer', 'Commerce', 
        'Acccounting', 'Literature', 'Government', 'Economic'
    ]

    # Constructing the SQL SELECT query
    columns_str = ', '.join(selected_columns)
    select_query = f"SELECT {columns_str} FROM AcademicInformation"

    # Executing the query
    cursor.execute(select_query)
    data = cursor.fetchall()

# Calculate percentage score for each student
    data_with_percentage = []
    for row in data:
        student_id = row[0]
        department = row[1]
        subjects_data = row[2:] 

        numeric_data = []
        for val in subjects_data:
            if isinstance(val, str) and val.strip():
                try:
                    numeric_data.append(float(val))
                except ValueError:
                    numeric_data.append(0.0)
            elif isinstance(val, int) or isinstance(val, float):
                numeric_data.append(float(val))
            else:
                numeric_data.append(0.0)

        total_score = sum(numeric_data)
        max_possible_score = 7 * 100  # Considering 10 subjects with a maximum score of 100 each

        percentage_score = 0.0  # Default to 0.0 if no valid subjects found
        if max_possible_score > 0:
            percentage_score = (total_score / max_possible_score) * 100

    # Round the percentage_score to one decimal place
        percentage_score = round(percentage_score, 1)

       # Create a new tuple including existing data and the percentage score
        row_with_percentage = (student_id, department, *subjects_data, percentage_score)
        data_with_percentage.append(row_with_percentage)
    conn.close()
    return data_with_percentage




# Route to display the selected columns
@app.route('/view-selected-columns')
def view_selected_columns():
    academic_data = fetch_selected_columns_with_percentage()
    return render_template('selected_columns.html', academic_data=academic_data)





if __name__ == '__main__':
    app.run()
