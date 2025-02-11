# MediVault

> **A full-stack medical record management system showcasing modern software engineering practices.**

## **Project Overview**
MediVault is a web-based application that provides **a seamless CRUD-based UI for managing patients, drugs, and prescriptions.** It utilizes modern web technologies like **NiceGUI, AG Grid, and Tortoise ORM** to create an efficient, asynchronous, and user-friendly experience. This project helped me understand **API design, database management, UI development, and Git workflow**.

---

## **What Makes This Project Special**
This project isn’t just another CRUD app—I designed it with **real-world software engineering principles** in mind:

- **Asynchronous Backend with Tortoise ORM & AsyncIO**: Efficient, non-blocking operations for managing patient records.
- **Dynamic UI with NiceGUI & AG Grid**: Seamless, interactive user experience with real-time updates.
- **Scalable API Design**: CRUD operations for patients, drugs, and prescriptions, with proper validation and error handling.
- **Git Workflow & Cross-Device Development**: Managed code across multiple machines, set up SSH keys, and maintained a clean commit history.
- **Database Portability**: Uses SQLite but easily adaptable to PostgreSQL for production.

> This project demonstrates my ability to **design scalable, interactive applications that integrate UI, databases, and APIs effectively.**

---

## **Tech Stack & Tools**

### **Backend**
- **Python** (AsyncIO for asynchronous programming)
- **FastAPI-style API Design** (CRUD operations)
- **Tortoise ORM** (Asynchronous database management using SQLite)

### **Frontend & UI**
- **NiceGUI** (Modern UI framework for interactive dashboards)
- **AG Grid** (Advanced table components for dynamic updates)

### **Database**
- **SQLite (for local dev, switchable to PostgreSQL)**

### **DevOps & Git**
- **Git & GitHub** (Repo management, commits, SSH key setup across devices)
- **.gitignore Best Practices** (Ignoring cache, DB files, environment files)

---

## **nstallation & Setup**

### **1) Clone the repository**
```sh
git clone https://github.com/haimiee/medi-vault.git
cd medi-vault
```

### **2️) Create a virtual environment (optional but recommended)**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\\Scripts\\activate'
```

### **3️) Install dependencies**
```sh
pip install -r requirements.txt
```

### **4️) Run the application**
```sh
python main.py
```
> Open **http://localhost:8080** in your browser.



---

## ** API Endpoints**

> **Patients API**
```http
POST /api/patient/add
GET /api/patient/all
GET /api/patient/{id}
PUT /api/patient/update/{id}
DELETE /api/patient/delete/{id}
```

> **Drugs API**
```http
POST /api/drug/add
GET /api/drug/all
GET /api/drug/{id}
PUT /api/drug/update/{id}
DELETE /api/drug/delete/{id}
```

> **Prescriptions API**
```http
POST /api/prescription/add
GET /api/prescription/all
GET /api/prescription/{id}
PUT /api/prescription/update/{id}
DELETE /api/prescription/delete/{id}
```

---

## **Future Enhancements**
- **User Authentication & Authorization** (JWT-based login system)
- **Deployment to AWS or GCP**
- **Enhanced UI with Real-time WebSockets for Live Updates**
- **Switch from SQLite to PostgreSQL for Production**

---

## **Contact**
For any issues or suggestions, feel free to **contact me** at [haimienguyen01@gmail.com](mailto:your.email@example.com).
