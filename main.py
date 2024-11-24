from flask import Flask, render_template, request, redirect
from models import db, EmployeeModel

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

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect('/data', 302)


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id,
                                 name=name,
                                 age=age,
                                 position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html', employees=employees)


@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id ={id} Doenst exist"


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
            employee = EmployeeModel(employee_id=id,
                                     name=name,
                                     age=age,
                                     position=position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"

    return render_template('update.html', employee=employee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if not employee:
        abort(404)

    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        return redirect('/data')

    return render_template('delete.html', employee=employee)


app.run(host='localhost', port=5000)
