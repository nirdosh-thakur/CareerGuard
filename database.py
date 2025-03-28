#import sqlalchemy
#import psycopg2

#your_user = 'postgres.ioygetmsqnbejcrtsuer'
#your_password ='Supabase%400868'
#your_host = 'aws-0-ap-south-1.pooler.supabase.com'
#your_port = 5432 
#your_database = 'postgres'

#DATABASE_URL = "postgresql://your_user:your_password@your_host:your_port/your_database"
#Direct Connection ::  postgresql://postgres:Supabase%400868@db.ioygetmsqnbejcrtsuer.supabase.co:5432/postgres
#Pooler Connection ::  postgresql://postgres.ioygetmsqnbejcrtsuer:Supabase%400868@aws-0-ap-south-1.pooler.supabase.com:5432/postgres

#Use %40 to replace @
import os
from sqlalchemy import create_engine, text

#DB_CONNECTION_STRING='postgresql://postgres.ioygetmsqnbejcrtsuer:Supabase%400868@aws-0-ap-south-1.pooler.supabase.com:5432/postgres'
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
        return None
      else:
        return row[0]._asdict()