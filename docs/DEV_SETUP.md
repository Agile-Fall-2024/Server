
# Development Setup:

Follow these steps to set up the project for local development:

### 1. Create a Virtual Environment:

- Before proceeding, create a virtual environment to isolate dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

- Install postgresql:

```bash
brew install postgresql
```

- Install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Create a .env File:

Copy the .env.example file to .env in the base directory.
Update the .env file with your environment-specific variables.

### 3. Database Setup:

If you’re not connected to the main project database (to be deployed in the cloud later):
Run the following commands to initialize the database schema:
```bash
make migrations
make migrate
```

### 4. Start the Development Server:

Run the server locally:
```bash
make run
```

Visit http://localhost:8000 to access the application.


### 5. Create a Superuser:

Create an admin user for yourself by running:
```bash
make superuser
```

Access the admin panel at http://localhost:8000/admin after starting the server again.

## 6. Package Management:

If you install any new packages, update requirements.txt.

Keeping requirements.txt updated will simplify future containerization.

## 7. Message Translateion

To update po files after adding new message:
```bash
django-admin makemessages -l fa
```

To Compile po files:

```bash
django-admin compilemessages
```

### Notes:
- Ensure you have Python 3.x and pip installed.
- Always activate the virtual environment before running commands to ensure dependencies are isolated.
