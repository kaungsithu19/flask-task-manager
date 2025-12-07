# Flask Task Manager  
A simple, modern, fully responsive **Task Manager Web Application** built with **Python Flask**, **Bootstrap 5**, and **JSON-based storage**.  
The app supports adding, editing, marking tasks as done, deleting, searching, pagination, dark mode, confirmation modals, and more.

Hosted on PythonAnywhere.

## 🚀 Features

### Core Features
- Add new tasks  
- Edit task titles  
- Delete tasks (with confirmation modal)  
- Mark tasks as done  
- Automatic task ID renumbering after deletion  
- Persistent storage using a JSON file  

### UI/UX Features
- Fully responsive Bootstrap 5 UI  
- Light/Dark mode toggle (saved in localStorage)  
- Search bar (real-time filtering)  
- Pagination (client-side)  
- Bootstrap Toast notifications  
- Clean card layout  
- Styled Pending/Done badges  

### Backend
- Flask routes for CRUD  
- JSON file as storage  
- Clean separation of logic (`task_logic.py`) and routing (`app.py`)  

### Deployment
- Fully deployable on PythonAnywhere  

## 🗂 Project Structure

```
project/
├── app.py
├── task_logic.py
├── tasks.json
└── templates/
    ├── index.html
    └── edit.html
```

## 🔧 Installation & Running Locally

### 1. Clone the repo
```
git clone https://github.com/kaungsithu19/flask-task-manager.git
cd task-manager
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run app
```
python app.py
```

### 4. Visit
```
http://127.0.0.1:5000
```

## 🌐 Deployment (PythonAnywhere)

1. Upload files  
2. Configure WSGI  
3. Install Flask  
4. Reload app  

## 🧠 Task ID Renumbering
After deletion, IDs reset to 1..N automatically.

## 📄 Requirements
```
Flask
```

## 🛠 Future Features
- SQLite support  
- Login system  
- REST API  

## 📜 License
MIT License  
