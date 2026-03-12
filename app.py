from flask import Flask, render_template, request
import PyPDF2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

skills_list = [
"python","java","c++","sql","machine learning",
"data science","deep learning","html","css",
"javascript","react","node","flask","django"
]

job_roles = {
"Data Scientist":["python","machine learning","data science","deep learning"],
"Web Developer":["html","css","javascript","react"],
"Backend Developer":["python","flask","django","sql"],
"Software Developer":["java","c++","sql"]
}

def extract_text(path):

    reader = PyPDF2.PdfReader(path)

    text=""

    for page in reader.pages:

        if page.extract_text():
            text += page.extract_text()

    return text.lower()


def get_india_job_links(role):

    role = role.replace(" ", "%20")

    jobs=[

    {
    "title":"LinkedIn Jobs",
    "company":"Search "+role+" jobs",
    "url":f"https://www.linkedin.com/jobs/search/?keywords={role}&location=India"
    },

    {
    "title":"Indeed India",
    "company":"Find "+role+" roles",
    "url":f"https://in.indeed.com/jobs?q={role}"
    },

    {
    "title":"Naukri Jobs",
    "company":"Top Indian jobs",
    "url":f"https://www.naukri.com/{role}-jobs"
    },

    {
    "title":"Glassdoor Jobs",
    "company":"Company listings",
    "url":f"https://www.glassdoor.co.in/Job/india-{role}-jobs-SRCH_IL.0,5_IN115_KO6,20.htm"
    },

    {
    "title":"Startup Jobs",
    "company":"Startup opportunities",
    "url":f"https://wellfound.com/jobs?query={role}"
    }

    ]

    return jobs


def analyze_resume(text):

    detected=[]

    for skill in skills_list:

        if skill in text:
            detected.append(skill)

    missing=list(set(skills_list)-set(detected))

    score=int((len(detected)/len(skills_list))*100)

    role_scores={}

    for role,skills in job_roles.items():

        role_scores[role]=len(set(skills) & set(detected))

    best_role=max(role_scores,key=role_scores.get)

    ats=min(100,score+15)

    suggestions=[]

    if score < 40:
        suggestions.append("Add more technical skills")

    if "project" not in text:
        suggestions.append("Add project experience")

    if "internship" not in text:
        suggestions.append("Add internship experience")

    if "github" not in text:
        suggestions.append("Add GitHub profile")

    jobs=get_india_job_links(best_role)

    return detected,missing,score,ats,best_role,jobs,suggestions


@app.route("/",methods=["GET","POST"])

def index():

    skills=[]
    missing=[]
    score=None
    ats=None
    role=None
    jobs=[]
    suggestions=[]

    if request.method=="POST":

        file=request.files["resume"]

        if file:

            path=os.path.join(app.config["UPLOAD_FOLDER"],file.filename)

            file.save(path)

            text=extract_text(path)

            skills,missing,score,ats,role,jobs,suggestions=analyze_resume(text)

    return render_template(
        "index.html",
        skills=skills,
        missing=missing,
        score=score,
        ats=ats,
        role=role,
        jobs=jobs,
        suggestions=suggestions
    )


if __name__=="__main__":
    app.run(debug=True)