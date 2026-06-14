from flask import Flask, render_template, request
import pdfplumber
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def scan():

    uploaded_files = request.files.getlist('resume')

    # Minimum 1 file required
    if len(uploaded_files) < 1:
        return "Please upload at least 1 resume"

    # Job role selected
    job_role = request.form['job_role']

    # Predefined skill sets
    job_skills = {

        "python_developer": [
            "python",
            "flask",
            "sql",
            "html",
            "css",
            "api",
            "mysql"
        ],

        "frontend_developer": [
            "html",
            "css",
            "javascript",
            "react",
            "bootstrap"
        ],

        "data_scientist": [
            "python",
            "machine learning",
            "pandas",
            "numpy",
            "tensorflow",
            "sql"
        ],

        "java_developer": [
            "java",
            "spring",
            "hibernate",
            "sql",
            "jdbc"
        ]

    }

    skills = job_skills.get(job_role, [])

    results = []

    allowed_extensions = ['pdf', 'txt']

    for file in uploaded_files:

        if file.filename == '':
            continue

        extension = file.filename.rsplit('.', 1)[1].lower()

        # Allow only PDF and TXT
        if extension not in allowed_extensions:
            continue

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        text = ""

        # PDF Extraction
        if extension == 'pdf':

            with pdfplumber.open(filepath) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text.lower()

        # TXT Extraction
        elif extension == 'txt':

            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read().lower()

        # Match Skills (Exact Match)

        matched_skills = []
        missing_skills = []

        for skill in skills:

            # Exact word matching
            pattern = r'\b' + re.escape(skill) + r'\b'

            if re.search(pattern, text):

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)

        # IMPORTANT SKILLS
        # First 3 skills are important

        important_skills = skills[:3]

        important_count = 0

        for imp_skill in important_skills:

            if imp_skill in matched_skills:
                important_count += 1

        # ATS Score

        ats_score = 0

        if len(skills) > 0:

            ats_score = int(
                (len(matched_skills) / len(skills)) * 100
            )

        # STRICT SCORING

        if important_count < 2 and ats_score > 85:

            ats_score = 85

        # CATEGORY

        if ats_score >= 90:

            category = "Priority List"

        elif ats_score >= 70:

            category = "Short Listed"

        else:

            category = "Rejected"

        # Extract Email

        email = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        # Extract Phone Number

        phone = re.findall(
            r"\+?\d[\d -]{8,12}\d",
            text
        )

        # Highlight Skills

        highlighted_text = text

        for skill in matched_skills:

            pattern = r'\b' + re.escape(skill) + r'\b'

            highlighted_text = re.sub(
                pattern,
                f"<mark>{skill}</mark>",
                highlighted_text,
                flags=re.IGNORECASE
            )

        results.append({

            'filename': file.filename,

            'required_skills': skills,

            'matched_skills': matched_skills,

            'missing_skills': missing_skills,

            'ats_score': ats_score,

            'category': category,

            'resume_text': highlighted_text,

            'email': email,

            'phone': phone

        })

    return render_template(
        "result.html",
        results=results
    )


@app.route("/resume_data", methods=['POST'])
def resume_data():

    text = request.form['resume_text']

    return render_template(
        "resume_data.html",
        resume_text=text
    )


if __name__ == '__main__':

    os.makedirs('uploads', exist_ok=True)

    app.run(debug=True)