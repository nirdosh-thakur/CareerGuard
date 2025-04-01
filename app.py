from flask import Flask, render_template, jsonify, request, url_for, redirect, session, flash
from database import load_all_jobs_from_db, load_single_job_from_db, add_application_to_db,check_user_in_db, SESSION_SECRET_KEY, insert_user_in_db,send_community_message,receive_community_message

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY


@app.route("/")
def hello_jovian():
    JOBS = load_all_jobs_from_db()
    user_id = session.get('user_id')
    logged_in = session.get('logged_in')
    return render_template('home.html',
                           id = user_id,
                           logged_in = logged_in,
                           jobs=JOBS,
                           company_name='Jovian Careers')


# Fetch all jobs in json api
@app.route("/api/jobs")
def list_jobs():
    jobs = load_all_jobs_from_db()
    return jsonify(jobs)


#fetch single job in json api
@app.route("/api/<id>")
def single_job(id):
    job = load_single_job_from_db(id)
    return jsonify(job)


@app.route("/jobs/<id>")
def show_job(id):
    if not session.get("logged_in"):  
        flash("Login to Apply", "danger")
        return redirect(url_for('hello_jovian'))
    JOB = load_single_job_from_db(id)
    if not JOB:
        return "Not Found", 404
    return render_template('jobPage.html', 
                           job=JOB)


#Methods = Post : tell us that it expect somehtign to be post
@app.route("/jobs/<id>/apply", methods=['post'])
def apply_to_job(id):
    #data = request.args  // Contain the inforamtion from the URL
    data = request.form  # Contain the inforamtion from the form
    JOB = load_single_job_from_db(id)
    add_application_to_db(id, data)
    return render_template('appSubmitted.html',
                    application = data,
                    job = JOB)

@app.route("/login")
def login():
    #session.clear() 
    return render_template('login.html',
                           #jobs=JOBS,
                           company_name='Jovian Careers')

@app.route("/logout")
def logout():
     # Clear the session data
    session.clear()
    
    # Expire the session cookie by setting its expiry to a past time
    response = make_response(redirect(url_for("login")))  # Redirect to the login page
    response.set_cookie('sessionid', '', expires=datetime.now() - timedelta(days=1))  # Expire the session cookie
    
    flash("You have been logged out successfully!", "success")
    return response

# Login check user authentication
@app.route("/login/check", methods=['post'])
def logged_user():
    username = request.form['username']
    password = request.form['password']
    
    # Check if user exists in DB
    result_dict = check_user_in_db(username, password)
    if(result_dict[0]=='SUCCESS'):
        flash("Login successful!", "success")
        session['logged_in'] = True
        session['user_id'] = result_dict[1]['id']
        session['first_name'] = result_dict[1]['first_name']
        session['last_name'] = result_dict[1]['last_name']
        session['email'] = result_dict[1]['email']
        return redirect(url_for('hello_jovian'))
    else:
        flash("Invalid Username/password!", "danger")
        return redirect(url_for('login'))

@app.route("/signup")
def signup():
    #JOBS = load_all_jobs_from_db()
    return render_template('signup.html',
                           #jobs=JOBS,
                           company_name='Jovian Careers')

@app.route("/signup/check", methods=['post'])
def create_new_user():
    #form_data = request.form.to_dict()
    #return jsonify(request.form)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    email = request.form['email']
    gender = request.form['gender']
    password = request.form['password']
    re_password = request.form['re_password']

    # Validate input fields
    #if not (username and password and first_name and last_name and email and gender):
    #    flash("All fields are required!", "danger")
    #    return redirect(url_for('signup'))  # Stay on the sign-up page

    # Check if user exists in DB
    if(password != re_password):
        flash("Password didn't match", "danger")
        return redirect(url_for('signup'))
        
    result_dict = check_user_in_db(username, password)
    
    if( result_dict[0] == "FAIL" ):
        #return jsonify(result_dict[1])
        query_status = insert_user_in_db(first_name, last_name, username, email, gender, password)
        if ( query_status['status'] == "SUCCESS" ):
            flash("User Account Created Successfully!", "success")
            return redirect(url_for('login'))
        else:
            flash(query_status['status']+" "+query_status['code']+" "+query_status['message'], "danger")
            return redirect(url_for('signup'))
    else:
        flash("Username already exists!", "danger")
        return redirect(url_for('signup'))


#Community Page
@app.route("/community")
def community():
    return render_template('community_msges.html')




@app.route('/community/send_message', methods=['POST'])
def send_message():
    #if 'first_name' not in session or 'user_id' not in session:
    #    return jsonify({'error': 'Unauthorized'}), 401

    username = session.get('first_name')
    message = request.form['cmnty_message']

    # Store message in DB
    send_community_message(username, session['user_id'], message)

    return jsonify({'status': 'Message sent'}), 200

@app.route('/community/send_message/api', methods=['POST'])
def send_api_message():
    username = session.get('first_name')
    message = request.form['message']
    send_community_message(username, session['user_id'], message)
    return jsonify({'status': 'Message sent'}), 200


@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = receive_community_message()
    return jsonify({'messages': messages})







if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
    #SocketIO.run(app, debug=True)

#Cloud Web Serivces - AWS, Azure, GCP, Render.com(good for Python)
