
import os
import hashlib
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


DB_CONNECTION_STRING = os.environ['DB_CONNECTION_STRING']
SESSION_SECRET_KEY = os.environ['SESSION_SECRET_KEY']

engine = create_engine(DB_CONNECTION_STRING)


##############################################################
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





def check_user_in_db(username, password):
    query = text("SELECT * FROM users WHERE username = :username")
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username})
        row = result.fetchone()
        if row:
            user_data = row._asdict()
            salt = user_data["salt"]
            hashed_pwd = user_data["password"]  
            if verify_password(salt, hashed_pwd, password):  
                return ['SUCCESS', user_data]
    return ['FAIL', {'id': 0}]







#Create salt and return salt and hashed password
def hash_password(password):
    salt = os.urandom(16) 
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)  
    return salt.hex(), salt.hex() + ":" + hashed.hex()


#Verfying salt and return salt and hashed password
def verify_password(salt, stored_hashed_password, entered_password):
    salt_hex, stored_hash_hex = stored_hashed_password.split(":")
    salt = bytes.fromhex(salt_hex)  
    entered_hash = hashlib.pbkdf2_hmac('sha256', entered_password.encode(), salt, 100000)
    #print("Stored salt:", salt)
    #print("Stored hash of pwd and salt:", stored_hashed_password)
    #print("New generated hash:", entered_hash.hex())
    return entered_hash.hex() == stored_hash_hex




#Insert new user into DB
def insert_user_in_db(first_name, last_name, username, email, gender, password):
    query = text("INSERT INTO users (first_name, last_name, username, email, gender, password, salt) VALUES (:fn, :ln, :un, :eml, :gndr, :pwd, :salt)")
    salt, hashed_pwd = hash_password(password)
    try:
        with engine.connect() as conn:
            conn.execute(query, {
                "fn": first_name,
                "ln": last_name,
                "un": username,
                "eml": email,
                "gndr" : gender,
                "pwd": hashed_pwd,
                "salt": salt
            })
            conn.commit()  # Commit changes
            return {"status": "SUCCESS", "message": "User inserted successfully"}

    except IntegrityError as e:
        return {"status": e, "code": "DUPLICATE_ENTRY", "message": "Please enter correct value"}

    except Exception as e:
        return {"status": "ERROR", "code": "DB_ERROR", "message": str(e)}



def send_community_message(userid, userfname, message):
    print("Send communtiy message function started")
    try:
        query = text("INSERT INTO community_messages (userid, username, message) VALUES (:userid, :username, :message)")
        with engine.connect() as conn:
            print("Database connection successful.")
            print(userid)
            print(userfname)
            print(message)
            conn.execute(query, {"userid": userid,
                                 "username": userfname,
                                 "message": message}) 
            print("Query executed successfully.")
            conn.commit()
            return True
    except SQLAlchemyError:
        print("Query failed.")
        return False

def g_fetch_all_community_message():
    return ['Fail']

def fetch_all_community_message():
    try:
        query = text("SELECT userid, username, message, timestamp FROM community_messages ORDER BY timestamp ASC")
        with engine.connect() as conn:
            result = conn.execute(query)
            print("Query executed successfully.Db")
            messages = [{'userId': row[0],'userfname': row[1], 'message': row[2], 'timestamp': row[3]} for row in result.fetchall()] 
            return ['Success', messages]
    except SQLAlchemyError:
        print("Query failed.")
        return ['Fail']