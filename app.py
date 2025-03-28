from flask import Flask, render_template, jsonify
from database import load_all_jobs_from_db, load_single_job_from_db


app = Flask(__name__)


@app.route("/")
def hello_jovian():
    JOBS = load_all_jobs_from_db()
    return render_template('home.html', 
                           jobs = JOBS, 
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
  JOB = load_single_job_from_db(id)
  if not JOB:
    return "Not Found", 404
  return render_template('jobPage.html', 
                         job=JOB)







if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

#Cloud Web Serivces - AWS, Azure, GCP, Render.com(good for Python)