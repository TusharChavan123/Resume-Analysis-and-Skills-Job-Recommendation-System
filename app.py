from flask import Flask, render_template, request, redirect, url_for, session, send_file
import io
import numpy as np
import sqlite3
import spacy
import pandas as pd
import os
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load spaCy's pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Skill mapping
skill_mapping = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "ci/cd": "continuous integration/continuous deployment",
    "dbms": "database management system",
}

job_roles = [
    "Data Scientist", "Software Engineer", "DevOps Engineer", "Cybersecurity Analyst",
    "Frontend Developer", "Backend Developer", "Full Stack Developer", "AI Engineer",
    "Cloud Engineer", "Data Engineer", "Blockchain Developer", "Game Developer",
    "Mobile App Developer", "Embedded Systems Engineer", "Systems Administrator",
    "Cybersecurity Engineer", "Database Administrator", "DevSecOps Engineer",
    "Big Data Engineer", "Network Engineer", "Robotics Engineer", "IoT Developer",
    "Software Tester", "Technical Support Engineer"
]

job_skills = [
    ["machine learning", "python", "deep learning", "nlp"],
    ["java", "react", "nodejs", "sql"],
    ["ci/cd", "docker", "kubernetes", "linux"],
    ["cybersecurity", "network security", "penetration testing", "encryption"],
    ["html", "css", "javascript", "react", "vue.js"],
    ["node.js", "express", "sql", "mongodb", "rest api"],
    ["javascript", "react", "node.js", "sql", "docker"],
    ["machine learning", "deep learning", "tensorflow", "python"],
    ["aws", "azure", "google cloud", "docker", "kubernetes"],
    ["python", "sql", "apache spark", "etl", "hadoop"],
    ["solidity", "ethereum", "hyperledger", "smart contracts"],
    ["unity", "c#", "unreal engine", "game physics"],
    ["flutter", "react native", "kotlin", "swift"],
    ["c", "c++", "microcontrollers", "rtos", "iot"],
    ["linux", "windows server", "networking", "shell scripting"],
    ["ethical hacking", "ids/ips", "encryption", "kali linux"],
    ["sql", "mysql", "postgresql", "nosql", "indexing"],
    ["ci/cd", "security testing", "owasp", "docker", "kubernetes"],
    ["hadoop", "spark", "scala", "kafka", "data warehousing"],
    ["cisco", "firewalls", "routing & switching", "vpns"],
    ["ros", "python", "matlab", "slam", "motion planning"],
    ["raspberry pi", "arduino", "mqtt", "edge computing"],
    ["selenium", "test automation", "api testing", "jira"],
    ["troubleshooting", "customer support", "sql", "linux"]
]


# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    """Reads and extracts text from an uploaded PDF file."""
    pdf_data = pdf_file.read()  # Read the file into memory
    pdf_stream = io.BytesIO(pdf_data)  # Convert it into a byte stream
    return extract_text(pdf_stream)  # Extract text from the byte stream

# Function to preprocess the text
def preprocess_text(text):
    doc = nlp(text.lower())
    clean_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(clean_tokens)

# Function to extract skills from text
def extract_skills(text, skills_keywords):
    skills = [skill_mapping.get(skill, skill) for skill in skills_keywords if skill in text]
    return list(set(skills))

# Function to compute missing skills
def compute_missing_skills(resume_skills, job_skills):
    return [skill for skill in job_skills if skill not in resume_skills]

# Function to read skills from a text file
def read_skills_from_file(file_path):
    with open(file_path, 'r') as file:
        skills = [line.strip().lower() for line in file if line.strip()]
    return list(set(skills))

# Load skills list
skills_keywords = read_skills_from_file('skills.txt')

# Compute cosine similarity
def compute_cosine_similarity(job_description, resumes):
    tfidf_vectorizer = TfidfVectorizer()
    documents = [job_description] + resumes
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return similarity_scores

# Function to classify resumes using KNN
def classify_resumes_knn(similarity_scores, top_n):
    labels = []
    num_resumes = len(similarity_scores)
    
    for i in range(num_resumes):
        if i < top_n:
            labels.append("Top")
        elif i < num_resumes * 0.75:  # Next 25% as "Average"
            labels.append("Average")
        else:
            labels.append("Not Selected")

    # Convert scores into a numpy array
    X = np.array(similarity_scores).reshape(-1, 1)
    y = np.array(labels)

    # Train KNN Classifier
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    # Predict categories for resumes
    predictions = knn.predict(X)
    
    return predictions

# SQLite Database Setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Signup function
def signup(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Login function
def login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == password

# Initialize the database
init_db()

def read_skills_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please make sure the file exists.")
        return []
    with open(file_path, 'r') as file:
        skills = [line.strip().lower() for line in file if line.strip()]
    return list(set(skills))

skills_keywords = read_skills_from_file('skills.txt')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login_route'))


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html', error=None)


@app.route('/signup', methods=['GET', 'POST'])
def signup_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            if signup(username, password):
                return redirect(url_for('login_route'))

            else:
                return render_template('signup.html', error="Username already exists.")
        else:
            return render_template('signup.html', error="Passwords do not match.")
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_route'))


def recommended_jobs(extracted_skills, job_roles, job_skills):
    """Recommends job roles based on extracted skills."""
    recommended = []
    for i, role in enumerate(job_roles):
        common_skills = set(extracted_skills) & set(job_skills[i])
        if common_skills:
            recommended.append(role)
    return recommended


# Upload route to process resumes and job description
@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login_route'))

    job_description_file = request.files['job_description']
    resume_files = request.files.getlist('resumes')

    if job_description_file and resume_files:
        # Extract and preprocess job description
        job_description_text = extract_text_from_pdf(job_description_file)
        cleaned_job_description_text = preprocess_text(job_description_text)
        job_description_skills = extract_skills(cleaned_job_description_text, sum(job_skills, []))

        # Process resumes
        resume_results = []
        resume_texts = []

        for resume_file in resume_files:
            resume_text = extract_text_from_pdf(resume_file)
            cleaned_resume_text = preprocess_text(resume_text)
            extracted_skills = extract_skills(cleaned_resume_text, sum(job_skills, []))
            missing_skills = compute_missing_skills(extracted_skills, job_description_skills)

            resume_results.append({
                'name': resume_file.filename,
                'text': cleaned_resume_text,
                'extracted_skills': extracted_skills,
                'missing_skills': missing_skills
            })
            resume_texts.append(cleaned_resume_text)

        # Compute cosine similarity scores
        similarity_scores = compute_cosine_similarity(cleaned_job_description_text, resume_texts) * 1000

        # Rank resumes based on similarity scores
        for i, result in enumerate(resume_results):
            result['cosine_similarity'] = round(similarity_scores[i], 4)

        ranked_resumes = sorted(resume_results, key=lambda x: x['cosine_similarity'], reverse=True)

        # Determine top candidates
        top_n = min(int(request.form['top_n']), len(ranked_resumes))
        top_candidates = ranked_resumes[:top_n]
        not_selected_candidates = ranked_resumes[top_n:]

        # Prepare data for Excel file
        excel_data = {
            'Resume Name': [],
            'Cosine Similarity': [],
            'Missing Skills': [],
            'Recommended Jobs': []
        }
        selected_data = {
            'Resume Name': [],
            'Cosine Similarity': []
        }

        for result in not_selected_candidates:
            job_recommendations = recommended_jobs(result['extracted_skills'], job_roles, job_skills)
            excel_data['Resume Name'].append(result['name'])
            excel_data['Cosine Similarity'].append(result['cosine_similarity'])
            excel_data['Missing Skills'].append(', '.join(result['missing_skills']))
            excel_data['Recommended Jobs'].append(', '.join(job_recommendations))
        
        for result in top_candidates:
            selected_data['Resume Name'].append(result['name'])
            selected_data['Cosine Similarity'].append(result['cosine_similarity'])

        # Save Excel file to disk in 'static' folder
        output_path = os.path.join('static', 'not_selected_candidates.xlsx')
        df = pd.DataFrame(excel_data)
        df.to_excel(output_path, index=False, engine='xlsxwriter')
        selected_path = os.path.join('static', 'selected_candidates.xlsx')
        df = pd.DataFrame(selected_data)
        df.to_excel(selected_path, index=False, engine='xlsxwriter')

        return render_template('results.html', 
                               top_candidates=top_candidates, 
                               not_selected_candidates=not_selected_candidates)

    return redirect(url_for('index'))

# Download route to serve the Excel file
@app.route('/download')
def download():
    if 'username' not in session:
        return redirect(url_for('login_route'))

    file_path = os.path.join('static', 'not_selected_candidates.xlsx')

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name='not_selected_candidates.xlsx')
    else:
        return "File not found!", 404
    
@app.route('/download_selected')
def download_selected():
    if 'username' not in session:
        return redirect(url_for('login_route'))

    file_path = os.path.join('static', 'selected_candidates.xlsx')
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name='selected_candidates.xlsx')
    else:
        return "File not found!", 404

if __name__ == '__main__':
    app.run(debug=True)