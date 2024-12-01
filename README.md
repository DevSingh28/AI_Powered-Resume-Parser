# AI Powered Resume Parser

This project is an AI-powered resume parser built using Django and other relevant libraries, capable of extracting key information from resumes (in various formats like PDF, DOCX, etc.). It is deployed on Render and can be accessed through a web interface.

## Features

- Upload resumes in PDF/DOCX format.
- Parse resumes to extract structured information.
- Save the parsed information in a database.
- Simple and easy-to-use web interface for users.

## Tech Stack

- **Backend**: Django
- **Web Server**: Gunicorn
- **AI Model**: Use of pre-trained machine learning models for parsing resumes
- **Deployment**: Render.com
- **Database**: SQLite (can be switched to PostgreSQL for production)

## Installation

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual Environment (optional but recommended)

### Steps to Set Up Locally

1. **Clone the repository**:

    ```bash
    git clone https://github.com/DevSingh28/ai-powered-resume-parser.git
    cd ai-powered-resume-parser
    ```

2. **Create and activate a virtual environment** (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    You need to create a `.env` file in the project root with the following variables:

    ```bash
    DEBUG=True
    SECRET_KEY=your_secret_key
    MEDIA_ROOT=/path/to/media/folder
    DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URL for production
    ```

5. **Run migrations**:

    ```bash
    python manage.py migrate
    ```

6. **Start the development server**:

    ```bash
    python manage.py runserver
    ```

    Now you can access the application at `http://127.0.0.1:8000/` in your browser.

## Deployment on Render

Follow these steps to deploy the app on Render:

1. **Push your changes to GitHub**.

2. **Sign up for an account on Render** if you haven't already: [Render.com](https://render.com).

3. **Create a new Web Service** on Render:

    - Select your GitHub repository.
    - Set the start command as:

      ```bash
      gunicorn resume_parser.wsgi:application
      ```

    - Set the environment to Python 3.x and the branch you want to deploy from.

4. **Configure environment variables** on Render:

    - Add the same environment variables you set locally (e.g., `SECRET_KEY`, `DEBUG`, `MEDIA_ROOT`, etc.) in Render's environment variable settings.

5. **Deploy your application**.

Once the deployment is complete, Render will provide you with a live URL for your deployed application.

## File Structure

/ai-powered-resume-parser
│
├── /resume_parser              # Main Django project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...                     # Other Django files
│
├── /media                      # Folder for uploaded files (configured in settings.py)
├── /static
