from flask import Flask, render_template, request
import PyPDF2
import os
from urllib.parse import quote, unquote

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

career_data = {

"Data Scientist":{
"description":"Data Scientists analyze large datasets and build machine learning models.",
"skills":["Python","Machine Learning","SQL","Statistics"],
"roadmap":[
"Learn Python programming",
"Learn statistics and probability",
"Learn machine learning algorithms",
"Practice data analysis projects",
"Learn deep learning",
"Build AI projects"
],
"salary":"₹6 LPA – ₹25 LPA"
},

"Web Developer":{
"description":"Web developers design and build modern websites.",
"skills":["HTML","CSS","JavaScript","React"],
"roadmap":[
"Learn HTML and CSS",
"Learn JavaScript",
"Learn React",
"Build frontend projects",
"Learn APIs",
"Deploy websites"
],
"salary":"₹4 LPA – ₹15 LPA"
}

}

def extract_text(path):

    reader = PyPDF2.PdfReader(path)
    text=""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()


def analyze_resume(text):

    detected=[]

    for skill in skills_list:
        if skill in text:
            detected.append(skill)

    missing=list(set(skills_list)-set(detected))

    score=int((len(detected)/len(skills_list))*50)

    ats=min(50,score+5)

    role_scores={}

    for role,skills in job_roles.items():
        role_scores[role]=len(set(skills) & set(detected))

    best_role=max(role_scores,key=role_scores.get)

    suggestions=[]

    if "python" not in detected:
        suggestions.append("Learn Python for AI roles")

    if "machine learning" not in detected:
        suggestions.append("Add Machine Learning projects")

    if "sql" not in detected:
        suggestions.append("Add SQL database knowledge")

    suggestions.append("Add internship experience")
    suggestions.append("Add GitHub portfolio")

    return detected,missing,score,ats,best_role,suggestions


@app.route("/",methods=["GET","POST"])
def index():

    skills=[]
    missing=[]
    score=None
    ats=None
    role=None
    suggestions=[]
    role_url=None

    if request.method=="POST":

        file=request.files["resume"]

        if file:

            path=os.path.join(app.config["UPLOAD_FOLDER"],file.filename)
            file.save(path)

            text=extract_text(path)

            skills,missing,score,ats,role,suggestions=analyze_resume(text)

            role_url=quote(role)

    return render_template(
        "index.html",
        skills=skills,
        missing=missing,
        score=score,
        ats=ats,
        role=role,
        role_url=role_url,
        suggestions=suggestions
    )


@app.route("/career/<role>")
def career(role):

    role=unquote(role)

    data=career_data.get(role)

    return render_template("career.html",role=role,data=data)


@app.route("/roadmap/<role>")
def roadmap(role):

    role=unquote(role)

    data=career_data.get(role)

    return render_template("roadmap.html",role=role,data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


