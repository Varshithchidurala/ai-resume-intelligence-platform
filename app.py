from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    score = None
    ats = None
    role = None
    role_url = None
    skills = []
    missing = []
    suggestions = []

    if request.method == "POST":

        file = request.files["resume"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        reader = PdfReader(filepath)

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        text = text.lower()

        skill_keywords = [
            "python","sql","machine learning","html","css",
            "javascript","flask","java","deep learning",
            "react","django"
        ]

        skills = [s for s in skill_keywords if s in text]
        missing = [s for s in skill_keywords if s not in text]

        score = min(50, len(skills) * 5)
        ats = min(50, score + 5)

        if "machine learning" in text or "deep learning" in text:
            role = "Data Scientist"
            role_url = "data-scientist"

        elif "javascript" in text or "react" in text:
            role = "Frontend Developer"
            role_url = "frontend-developer"

        else:
            role = "Software Developer"
            role_url = "software-developer"

        suggestions = [
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
        suggestions=suggestions
    )


@app.route("/career/<role>")
def career(role):

    if role == "data-scientist":

        title = "Data Scientist"

        description = "Data Scientists analyze data and build machine learning models."

        roadmap = [
            "Learn Python",
            "Learn Statistics",
            "Learn SQL",
            "Learn Data Visualization",
            "Learn Machine Learning",
            "Build AI Projects",
            "Apply for Data Science Jobs"
        ]

    elif role == "frontend-developer":

        title = "Frontend Developer"

        description = "Frontend Developers build user interfaces and web experiences."

        roadmap = [
            "Learn HTML",
            "Learn CSS",
            "Learn JavaScript",
            "Learn React",
            "Build Web Projects",
            "Learn Git and GitHub",
            "Apply for Frontend Developer Jobs"
        ]

    else:

        title = "Software Developer"

        description = "Software Developers build applications and backend systems."

        roadmap = [
            "Learn Programming (Python or Java)",
            "Learn Data Structures",
            "Learn Algorithms",
            "Learn Databases",
            "Build Real Projects",
            "Practice Coding Interviews",
            "Apply for Software Developer Jobs"
        ]

    return render_template(
        "career.html",
        title=title,
        description=description,
        roadmap=roadmap
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



