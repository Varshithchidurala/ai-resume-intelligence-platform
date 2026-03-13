from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET","POST"])
def index():

    score=None
    ats=None
    role=None
    role_url=None
    skills=[]
    missing=[]
    suggestions=[]
    error=None

    if request.method=="POST":

        file=request.files["resume"]

        if not file.filename.endswith(".pdf"):
            return render_template(
                "index.html",
                error="Please upload a PDF resume file only."
            )

        filepath=os.path.join(UPLOAD_FOLDER,file.filename)
        file.save(filepath)

        reader=PdfReader(filepath)

        text=""
        for page in reader.pages:
            text+=page.extract_text()

        text=text.lower()

        skill_keywords=[
            "python","sql","machine learning","html","css",
            "javascript","flask","java","react","django"
        ]

        skills=[s for s in skill_keywords if s in text]
        missing=[s for s in skill_keywords if s not in text]

        score=min(50,len(skills)*5)
        ats=min(50,score+5)

        if "machine learning" in text:
            role="Data Scientist"
            role_url="data-scientist"

        elif "javascript" in text or "react" in text:
            role="Frontend Developer"
            role_url="frontend-developer"

        else:
            role="Software Developer"
            role_url="software-developer"

        suggestions=[
            "Add measurable achievements",
            "Include GitHub project links",
            "Add internship experience",
            "Add certifications",
            "Improve ATS keywords"
        ]

    return render_template(
        "index.html",
        score=score,
        ats=ats,
        role=role,
        role_url=role_url,
        skills=skills,
        missing=missing,
        suggestions=suggestions,
        error=error
    )


@app.route("/career/<role>")
def career(role):

    if role=="data-scientist":

        title="Data Scientist"
        description="Data Scientists analyze large datasets and build machine learning models."
        salary="₹8 LPA – ₹25 LPA"

        skills=["Python","Machine Learning","Statistics","SQL","Data Visualization"]

        tools=["TensorFlow","Scikit-Learn","Power BI","Tableau"]

        courses=[
        ("Machine Learning Course","https://www.coursera.org/learn/machine-learning"),
        ("Python Data Science","https://www.coursera.org/learn/python-data-analysis")
        ]

    elif role=="frontend-developer":

        title="Frontend Developer"
        description="Frontend developers build user interfaces and interactive web apps."
        salary="₹4 LPA – ₹15 LPA"

        skills=["HTML","CSS","JavaScript","React"]

        tools=["React","Tailwind","Bootstrap","Figma"]

        courses=[
        ("React Course","https://www.udemy.com/course/react-the-complete-guide"),
        ("HTML CSS Course","https://www.udemy.com/course/html-css-from-beginner-to-expert")
        ]

    else:

        title="Software Developer"
        description="Software developers design backend systems and applications."
        salary="₹5 LPA – ₹20 LPA"

        skills=["Programming","Data Structures","Algorithms"]

        tools=["Python","Java","Docker","AWS"]

        courses=[
        ("DSA Course","https://www.geeksforgeeks.org/data-structures"),
        ("Java Programming","https://www.udemy.com/course/java-the-complete-java-developer-course")
        ]

    return render_template(
        "career.html",
        title=title,
        description=description,
        salary=salary,
        skills=skills,
        tools=tools,
        courses=courses,
        role=role
    )


@app.route("/roadmap/<role>")
def roadmap(role):

    if role=="data-scientist":

        title="Data Scientist Roadmap"

        roadmap=[
        "Learn Python",
        "Learn Statistics",
        "Learn SQL",
        "Learn Data Visualization",
        "Learn Machine Learning",
        "Build AI Projects",
        "Apply for Data Science Jobs"
        ]

    elif role=="frontend-developer":

        title="Frontend Developer Roadmap"

        roadmap=[
        "Learn HTML",
        "Learn CSS",
        "Learn JavaScript",
        "Learn React",
        "Build Web Projects",
        "Learn Git",
        "Apply for Frontend Jobs"
        ]

    else:

        title="Software Developer Roadmap"

        roadmap=[
        "Learn Programming",
        "Learn Data Structures",
        "Learn Algorithms",
        "Build Projects",
        "Practice Coding Interviews",
        "Apply for Software Jobs"
        ]

    return render_template("roadmap.html",title=title,roadmap=roadmap)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)




