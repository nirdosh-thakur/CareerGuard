
import os
from sqlalchemy import create_engine, text

DB_CONNECTION_STRING = os.environ['DB_CONNECTION_STRING']

engine = create_engine(DB_CONNECTION_STRING)

#Loading all Jobs
def load_all_jobs_from_db():
  with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM jobs"))
      jobs = []
      for row in result.all():
          jobs.append(row._asdict())
      return jobs


#Loading a single Job
def load_single_job_from_db(id):
    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM jobs where id = :val"),{"val":id} )
      row = result.all()
      if(len(row) == 0):
        return {}
      else:
        return row[0]._asdict()



def add_application_to_db(job_id, data):
  query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
  with engine.connect() as conn:
      conn.execute(query, {
          "job_id": job_id, 
          "full_name": data['full_name'],
          "email": data['email'],
          "linkedin_url": data['linkedin_url'],
          "education": data['education'],
          "work_experience": data['work_experience'],
          "resume_url": data['resume_url']
      })
      conn.commit()

