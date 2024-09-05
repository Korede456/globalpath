# GlobPath

GlobPath is a job portal web application designed to connect job seekers with employers. The project is built using Django for the backend and Tailwind CSS for the frontend styling.

# Contributors

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- npm (Node Package Manager)
- Django

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/korede456/globpath.git
cd globpath
```
### 2. Create a virtual environment

```bash
python3 -m venv <environment_name>
```

### 3. Activate the environment

```bash
environment_name\Scripts\Activate
# on linux 
source <environment_name>/bin/activate
```

### 4. Install python dependencies

```bash
pip install -r requirements.txt
```

### 5. Make migrations

```bash
python3 manage.py makemigrations

# After making migration run the following code to migrate

python3 manage.py migrate
```

### 6. Install javaScript dependencies

```bash
# needed for tailwind css configuration:
npm install
```

### 7. Tailwind css compilation

```bash
# To compile the Tailwind CSS classes into output.css, run the following command in one terminal:

npm run build:css
```

### 8. Start django development server

```bash
# In another terminal, start the Django development server:

python3 manage.py runserver

# Once the server is running, open your browser and go to:
[url](http://127.0.0.1:8000)
```
