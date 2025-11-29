# Smart Projects

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd smart_projects
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # Create virtual environment
    python3 -m venv venv

    # Activate virtual environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Populate the database (Optional):**

    To load initial dummy data into the database, run:

    ```bash
    python populate_db.py
    ```

## Running the Project

1.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```

2.  **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:8000/`.
