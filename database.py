import sqlite3

def create_database():

    connection = sqlite3.connect("career_analyzer.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_role TEXT NULL,
        match_percentage REAL,
        matched_skills TEXT,
        missing_skills TEXT
    )
    """)
    connection.commit()
    connection.close()

def save_analysis(job_role,match_percentage,matched_skills, missing_skills):



    connection = sqlite3.connect("career_analyzer.db")


    cursor = connection.cursor()

    cursor.execute("""
          INSERT INTO analysis_results
          (job_role, match_percentage, matched_skills, missing_skills)
          VALUES(?,?,?,?)
          """,(
              job_role,
              match_percentage,
              " , ".join(matched_skills),
              " ,".join(missing_skills)
          )
          )
    connection.commit()
    connection.close()
def get_all_analyses():

    connection = sqlite3.connect("career_analyzer.db")

    cursor = connection.cursor()
    cursor.execute("""
          SELECT * FROM analysis_results
    """)
    data = cursor.fetchall()
    connection.close()
    return data



