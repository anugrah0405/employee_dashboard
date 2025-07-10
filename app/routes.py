from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app.services import allowed_file, process_excel_file, get_departments, get_employees_by_department
from app import db
from app.models import Employee
from app.auth import login_required

bp = Blueprint('routes', __name__)

@bp.route('/')
@login_required
def home():
    return redirect(url_for('routes.upload'))

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        if not file or file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
            
        if allowed_file(file.filename):
            result = process_excel_file(file, file.filename)
            
            if result['success']:
                res = result['results']
                if res['created'] > 0:
                    flash(f"Created {res['created']} new employees", 'success')
                if res['updated'] > 0:
                    flash(f"Updated {res['updated']} existing employees", 'info')
                for error in res['errors']:
                    flash(error, 'danger')
                return redirect(url_for('routes.search'))
            else:
                flash(f"Error: {result['error']}", 'danger')
    
    return render_template('upload.html')

@bp.route('/search', methods=['GET'])
@login_required
def search():
    departments = db.session.query(Employee.department).distinct().all()
    departments = [dept[0] for dept in departments if dept[0]]  # Filter out None values
    return render_template('search.html', departments=departments)

@bp.route('/api/employees', methods=['GET'])
@login_required
def api_employees():
    department = request.args.get('department')
    if not department:
        return jsonify({'error': 'Department parameter is required'}), 400
    
    employees = Employee.query.filter_by(department=department).order_by(Employee.name).all()
    return jsonify([{
        'id': emp.employee_id,
        'name': emp.name,
        'email': emp.email,
        'designation': emp.designation
    } for emp in employees])