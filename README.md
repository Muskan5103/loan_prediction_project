# Loan Prediction System

A Machine Learning based Loan Prediction System built using **Python, Django, HTML, CSS, JavaScript, and Scikit-Learn**. This application predicts whether a loan application is likely to be approved based on applicant details and financial information.

## Features

* User Registration and Login
* Loan Application Form
* Loan Eligibility Prediction using Machine Learning
* Profile Management
* Responsive User Interface
* Prediction History Tracking
* Secure Authentication System

## Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Backend

* Python
* Django

### Machine Learning

* Scikit-Learn
* Pandas
* NumPy
* Joblib

### Database

* SQLite3

## Project Structure

loan_prediction_project/

├── dataset/

├── loan_prediction_project/

├── predictor/

├── ml_models/

├── train_model/

├── media/

├── manage.py

├── requirements.txt

├── render.yaml

└── Procfile

## Installation

### Clone Repository

```bash
git clone https://github.com/Muskan5103/loan_prediction_project.git
cd loan_prediction_project
```

### Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Run Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## Machine Learning Model

The prediction model is trained using historical loan application data. The model analyzes factors such as:

* Applicant Income
* Co-applicant Income
* Loan Amount
* Loan Term
* Credit History
* Marital Status
* Education
* Employment Status
* Property Area

Based on these inputs, the system predicts whether the loan is likely to be approved.

## Deployment

The project is configured for deployment using:

* Render
* Gunicorn
* Procfile
* render.yaml

## Future Enhancements

* Email Notifications
* Admin Dashboard Analytics
* Loan Approval Reports
* Multiple ML Model Comparison
* PDF Report Generation
* Real-Time Prediction Statistics

## Author

Muskan Mahajan

GitHub:
https://github.com/Muskan5103
