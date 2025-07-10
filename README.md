# Employee Dashboard

A Flask-based web application for uploading and managing employee data with department filtering capabilities.

---

## Features

- Session-based authentication
- Excel file upload and processing
- Department-based employee filtering
- REST API endpoint for employee data
- Mock Azure Blob Storage integration
- Mock Key Vault for secret management

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- SQLite (included with Python)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/employee-dashboard.git
   cd employee-dashboard
   ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Linux/Mac:
    source venv/bin/activate
    # Windows:
    venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Initialize the database:
    ```bash
    python create_tables.py
    ```
5. Create required directories:
    ```bash
    mkdir -p uploads/excel_files uploads/blob_storage
    ```

### Configuration
- Copy the sample environment file and edit as needed:
    ```bash
    cp .env.example .env
    ```

### Running the Application
- Start the development server:
    ```bash
    python run.py
    ```
- Access the application at: [http://localhost:5000](http://localhost:5000)

---

## Default Credentials
- Username: admin
- Password: admin123

---

## API Endpoints
1. Get Employees by Department
   ```bash
   GET /api/employees?department={department_name}
   ```
    - Example:
      ```bash
      curl "http://localhost:5000/api/employees?department=HR"
      ```
    - Response:
      ```bash
      [
        {
            "id": "1002",
            "name": "Jane Smith",
            "email": "jane@example.com",
            "designation": "Manager"
        }
      ]
      ```
2. Upload Excel File

   Post / upload

   Example:
      ```bash
      curl -X POST -F "file=@sample_data.xlsx" http://localhost:5000/upload
      ```

---

## Sample Excel File Format
   - Create an Excel file (sample_data.xlsx) with these columns:
      ```bash
      ID, Name, Email, Department, Designation
      1001, John Doe, john@example.com, IT, Developer
      1002, Jane Smith, jane@example.com, HR, Manager
      ```
      
---

## Project Structure
   ```bash
   employee_dashboard/
   ├── app/                      # Flask application
   │   ├── __init__.py           # App factory
   │   ├── auth.py               # Authentication
   │   ├── models.py             # Database models
   │   ├── routes.py             # Application routes
   │   ├── services.py           # Business logic
   │   ├── utils/                # Utility classes
   │   ├── static/               # Static files
   │   └── templates/            # HTML templates
   ├── instance/                 # Database files
   ├── uploads/                  # File uploads
   ├── requirements.txt          # Dependencies
   ├── create_tables.py          # DB initialization
   ├── sample_data.xlsx          # Sample data
   ├── config.py                 # Configuration
   ├── run.py
   └── README.md
   ```

---

## License

This project is licensed under the MIT License
