from flask import Flask, render_template, jsonify
from database import load_jobs_from_db


app = Flask(__name__)


@app.route("/")
def hello_jovian():
    JOBS = load_jobs_from_db()
    return render_template('home.html', 
                           jobs = JOBS, 
                           company_name='Jovian Careers')




# In /api/jobs  api is used to differentiate between html pasge and page carrying structured inforamtion.
@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)


@app.route("/api/<id>")
def single_job(id):
    job = load_jobs_from_db(id)
    return jsonify(job)








if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

#Cloud Web Serivces - AWS, Azure, GCP, Render.com(good for Python)