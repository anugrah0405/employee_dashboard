from http import client
import io
import os
from pathlib import Path
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Config, current_app
from app import db
from app.models import Employee
from app.utils.blob_storage import MockBlobStorage
from app.utils.key_vault import MockKeyVault

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def process_excel_file(file_storage, filename):
    """Process uploaded Excel file with blob storage integration"""
    try:
        secure_name = secure_filename(filename)
        temp_path = Path(current_app.config['UPLOAD_FOLDER']) / secure_name
        file_storage.save(str(temp_path))
        
        df = pd.read_excel(temp_path)
        required_columns = ['ID', 'Name', 'Email', 'Department', 'Designation']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in Excel file")
        
        with open(temp_path, 'rb') as f:
            blob_info = MockBlobStorage.upload_file(f, secure_name)
        
        results = {'created': 0, 'updated': 0, 'errors': []}
        
        for index, row in df.iterrows():
            try:
                emp_id = str(row['ID'])
                employee = Employee.query.filter_by(employee_id=emp_id).first()
                
                if employee:
                    employee.name = row['Name']
                    employee.email = row['Email']
                    employee.department = row['Department']
                    employee.designation = row['Designation']
                    results['updated'] += 1
                else:
                    db.session.add(Employee(
                        employee_id=emp_id,
                        name=row['Name'],
                        email=row['Email'],
                        department=row['Department'],
                        designation=row['Designation']
                    ))
                    results['created'] += 1
            except Exception as e:
                results['errors'].append(f"Row {index+2}: {str(e)}")
        
        db.session.commit()
        return {'success': True, 'results': results, 'blob_info': blob_info}
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Processing failed: {str(e)}")
        return {'success': False, 'error': str(e)}
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception as e:
                current_app.logger.warning(f"Cleanup failed: {str(e)}")
def get_departments():
    departments = db.session.query(
        Employee.department
    ).distinct().order_by(Employee.department).all()
    return [dept[0] for dept in departments]

def get_employees_by_department(department):
    employees = Employee.query.filter_by(
        department=department
    ).order_by(Employee.name).all()
    return [emp.to_dict() for emp in employees]

def test_key_vault():
    assert MockKeyVault.get_secret('api-key') is not None
    assert isinstance(MockKeyVault.get_secret('flask-secret'), str)
    
def test_blob_storage():
    test_file = io.BytesIO(b"test content")
    result = MockBlobStorage.upload_file(test_file, "test.txt")
    assert Path(Config.BLOB_STORAGE_FOLDER, result['filename']).exists()
    
def test_upload_flow():
    with open('test.xlsx', 'rb') as f:
        response = client.post('/upload', data={'file': f})
    assert b"Created" in response.data or b"Updated" in response.data