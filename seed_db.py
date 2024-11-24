from faker import Faker
from models import db, EmployeeModel, DepartmentModel, ProjectModel, SkillModel
from datetime import datetime, timedelta
import random

fake = Faker()


def seed_database():
    # Создаем отделы
    department_names = [
        'IT Department', 'Human Resources', 'Marketing', 'Sales',
        'Research & Development', 'Finance', 'Operations', 'Customer Support'
    ]

    departments = []
    for dept_name in department_names:
        dept = DepartmentModel(name=dept_name,
                               location=fake.city(),
                               budget=random.uniform(100000, 1000000))
        db.session.add(dept)
        departments.append(dept)

    # Создаем проекты
    projects = []
    for _ in range(10):
        start_date = fake.date_time_between(start_date='-2y', end_date='now')
        project = ProjectModel(name=fake.catch_phrase(),
                               description=fake.text(),
                               start_date=start_date,
                               end_date=start_date +
                               timedelta(days=random.randint(30, 365)),
                               budget=random.uniform(10000, 500000))
        db.session.add(project)
        projects.append(project)

    # Создаем навыки
    skills = []
    skill_data = [('Python', 'Technical'), ('Java', 'Technical'),
                  ('SQL', 'Technical'), ('Leadership', 'Soft Skills'),
                  ('Communication', 'Soft Skills'),
                  ('Project Management', 'Management'),
                  ('English', 'Languages'), ('Spanish', 'Languages'),
                  ('Data Analysis', 'Technical'),
                  ('Machine Learning', 'Technical'),
                  ('Team Building', 'Management'), ('Agile', 'Management'),
                  ('JavaScript', 'Technical'),
                  ('Public Speaking', 'Soft Skills'),
                  ('Problem Solving', 'Soft Skills')]

    for skill_name, category in skill_data:
        skill = SkillModel(name=skill_name,
                           category=category,
                           description=fake.sentence())
        db.session.add(skill)
        skills.append(skill)

    # Commit первую партию чтобы получить ID
    db.session.commit()

    # Создаем сотрудников
    positions = [
        'Software Engineer', 'Project Manager', 'HR Specialist',
        'Marketing Manager', 'Sales Representative', 'Data Analyst',
        'Team Lead', 'Business Analyst', 'Product Manager', 'QA Engineer'
    ]

    for i in range(100):
        employee = EmployeeModel(employee_id=i + 1,
                                 name=fake.name(),
                                 age=random.randint(22, 65),
                                 position=random.choice(positions),
                                 salary=random.uniform(30000, 150000),
                                 department_id=random.choice(departments).id,
                                 project_id=random.choice(projects).id
                                 if random.random() > 0.2 else None)
        # Добавляем случайные навыки (от 2 до 5)
        random_skills = random.sample(skills, random.randint(2, 5))
        employee.skills.extend(random_skills)

        db.session.add(employee)

    db.session.commit()
    print("Database seeded successfully!")


if __name__ == "__main__":
    from main import app
    with app.app_context():
        db.create_all()
        seed_database()
