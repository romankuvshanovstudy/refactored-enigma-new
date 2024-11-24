from flask import Flask, render_template, request, redirect, abort
from models import db, EmployeeModel, DepartmentModel, ProjectModel, SkillModel

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://myDb_smilestone:89a1bff7435bc21fb5156513a010cb90e27b4d7f@31jj0.h.filess.io:3305/myDb_smilestone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MYSQL_SSL_DISABLED'] = True
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 1,
    'max_overflow': 0,
    'connect_args': {
        'ssl': {
            'ssl_disabled': True
        }
    }
}
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        departments = DepartmentModel.query.all()
        projects = ProjectModel.query.all()
        skills = SkillModel.query.all()
        return render_template('createpage.html',
                               departments=departments,
                               projects=projects,
                               skills=skills)

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        salary = request.form['salary']
        department_id = request.form['department_id']
        project_id = request.form['project_id']
        skill_ids = request.form.getlist('skills')

        employee = EmployeeModel(employee_id=employee_id,
                                 name=name,
                                 age=age,
                                 position=position,
                                 salary=salary,
                                 department_id=department_id,
                                 project_id=project_id)

        # Добавляем выбранные навыки
        skills = SkillModel.query.filter(SkillModel.id.in_(skill_ids)).all()
        employee.skills.extend(skills)

        db.session.add(employee)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.order_by(EmployeeModel.employee_id).all()
    return render_template('datalist.html', employees=employees)


@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id ={id} Doesn't exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()

            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            salary = request.form['salary']
            department_id = request.form['department_id']
            project_id = request.form['project_id']
            skill_ids = request.form.getlist('skills')

            employee = EmployeeModel(employee_id=id,
                                     name=name,
                                     age=age,
                                     position=position,
                                     salary=salary,
                                     department_id=department_id,
                                     project_id=project_id)

            skills = SkillModel.query.filter(
                SkillModel.id.in_(skill_ids)).all()
            employee.skills.extend(skills)

            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does not exist"

    departments = DepartmentModel.query.all()
    projects = ProjectModel.query.all()
    skills = SkillModel.query.all()
    return render_template('update.html',
                           employee=employee,
                           departments=departments,
                           projects=projects,
                           skills=skills)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
