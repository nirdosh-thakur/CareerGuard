from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
        'id' : 1,
        'title' : 'Data Analyst',
        'location' :'Thane, Maharashtra',
        'salary' : 'Rs. 1,00,000'
    },
    {
        'id' : 2,
        'title' : 'HR',
        'location' :'Thane, Maharashtra',
        'salary' : 'Rs. 1,00,000'
    },
    {
        'id' : 3,
        'title' : 'Backend Engineer',
        'location' :'Banglore, India',
        'salary' : 'Rs. 1,30,000'
    },
    {
        'id' : 4,
        'title' : 'AI Engineer',
        'location' :'Delhi, India',
        'salary' : 'Rs. 1,10,000'
    }
]





@app.route("/")
def hello_jovian():
    return render_template('home.html', jobs=JOBS, company_name='Jovian Careers')



# Commented out code
# In /api/jobs  api is used to differentiate between html pasge and page carrying structured inforamtion.
@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)





if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)





#Cloud Web Serivces - AWS, Azure, GCP, Render.com(good for Python)