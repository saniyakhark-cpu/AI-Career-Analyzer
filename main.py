def analyze_resume(full_text, 
job_skills):
    found_skills = []

    for skill in job_skills:
        if skill.lower() in full_text.lower():
            found_skills.append(skill)

        matched_skills = found_skills

        missing_skills = []

        for skill in job_skills:
            if skill.lower() not in [s.lower() for s in found_skills]:
                missing_skills.append(skill)

        
            if len(job_skills)>0:
                match_percantage = (len(matched_skills)/ len(job_skills))*100
            else:
                match_percantage = 0

            return found_skills, missing_skills, matched_skills, match_percantage   
     
        
        