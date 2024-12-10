from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import time
import psycopg2
import zipfile
from io import BytesIO

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Wait for database to be ready
def wait_for_db(max_retries=30):
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname="cvdb",
                user="postgres",
                password="password",
                host="db"
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            retries += 1
            time.sleep(1)
    return False

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)

# Initialize database and add test data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if we already have data
        if CV.query.first() is None:
            # Add some test data
            test_cvs = [
                CV(
                    name="John Doe",
                    email="john@example.com",
                    experience="5 years as Software Developer",
                    education="BS in Computer Science"
                ),
                CV(
                    name="Jane Smith",
                    email="jane@example.com",
                    experience="3 years as Data Analyst",
                    education="MS in Data Science"
                )
            ]
            
            for cv in test_cvs:
                db.session.add(cv)
            
            try:
                db.session.commit()
                print("Test data added successfully")
            except Exception as e:
                print(f"Error adding test data: {e}")
                db.session.rollback()

# Initialize the database
if wait_for_db():
    init_db()
else:
    raise Exception("Could not connect to database")

@app.route('/api/cvs', methods=['GET'])
def get_cvs():
    try:
        cvs = CV.query.all()
        return jsonify([{
            'id': cv.id,
            'name': cv.name,
            'email': cv.email,
            'experience': cv.experience,
            'education': cv.education
        } for cv in cvs])
    except Exception as e:
        print(f"Error fetching CVs: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cvs', methods=['POST'])
def create_cv():
    try:
        data = request.json
        new_cv = CV(
            name=data['name'],
            email=data['email'],
            experience=data['experience'],
            education=data['education']
        )
        db.session.add(new_cv)
        db.session.commit()
        return jsonify({'message': 'CV created successfully'}), 201
    except Exception as e:
        print(f"Error creating CV: {e}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download_app():
    # Path to the script
    script_path = os.path.join(app.root_path, 'downloadable', 'system_control.py')
    
    # Create a ZIP file in memory
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        # Add the script to the ZIP file
        zf.write(script_path, 'system_control.py')
        
        # Add a README file with instructions
        readme_content = """
System Control Script
====================

This script provides basic system control functionality for both Windows and Mac.

Requirements:
- Python 3.x installed on your system

To run:
1. Extract the contents of this ZIP file
2. Open terminal/command prompt
3. Navigate to the extracted folder
4. Run: python system_control.py

Note: Some functions may require administrator/sudo privileges.
"""
        zf.writestr('README.txt', readme_content)
    
    # Seek to the beginning of the BytesIO object
    memory_file.seek(0)
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='system_control.zip'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
