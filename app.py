from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Lista fija de estudiantes (usuario: contraseña)
students = {
    "1RHM": "password1",
    "1RH2M": "password2",
    "1RH3M": "password3",
    "1OM": "password4",
    "1O2M": "password5",
    "1EM": "password6",
    "3RHM": "password7",
    "3RH2M": "password8",
    "3RH3M": "password9",
    "3OM": "password10",
    "3O2M": "password11",
    "3EM": "password12",
    "5RHM": "password13",
    "5RH2M": "password14",
    "5RH3M": "password15",
    "5OM": "password16",
    "5EM": "password17"
}

# Lista fija de profesores (usuario: contraseña)
teachers = {
    "Alejandro Reyes López": "pass1",
    "Rocío Patricia González Martínez": "pass2",
    "José Antonio Sebastián Hernández": "pass3",
    "José Félix Morales Bustamante": "pass4",
    "Claudia María Quiroa Montalván": "pass5",
    "Juana Ramos Luna": "pass6",
    "Alejandro Torres Páramo": "pass7",
    "Norma Lorena Quinteros Carrillo": "pass8",
    "Norma Elisa Ramírez Lugardo": "pass9",
    "Karen Yajaira Vargas Méndez": "pass10",
    "Lucía Carrillo Gutiérrez": "pass11",
    "Arcelia Margarita Sarmiento Ramos": "pass12",
    "Edgar Chávez Rodríguez": "pass13",
    "Patricia Pimentel Rodríguez": "pass14",
    "Miguel Ángel Benítez González": "pass15",
    "Horacio Monroy Castañeda": "pass16",
    "Aurelio Badillo Gámez": "pass17",
    "Oliva Adriana Gómez Favela": "pass18",
    "Berenice Suárez Mendoza": "pass19",
    "Arcelia Nevarez Jiménez": "pass20",
    "Irene Patricia Pimentel Rodríguez": "pass21",
    "Beronica Suárez Mendoza": "pass22",
    "María Lucía Carrillo Gutiérrez": "pass23",
    "Anastacio Rivera Lozoya": "pass24",
    "Gumercindo Velázquez Mejía": "pass25"
}

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:813102237ec20@localhost/cbtis237'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Carpeta donde se almacenarán los archivos subidos
db = SQLAlchemy(app)

# Configurar la clave secreta para manejar sesiones
app.secret_key = '5155156L'  # Reemplaza con una clave segura

# Crear modelo para Materiales y Anuncios
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200))

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el dashboard de estudiantes
@app.route('/student_dashboard')
def student_dashboard():
    student_id = session.get('student_id')  # Recupera el student_id de la sesión
    if not student_id:
        return redirect(url_for('login'))

    # Obtener todos los materiales y anuncios disponibles para el estudiante
    materials = Material.query.all()

    return render_template('student_dashboard.html', student_id=student_id, materials=materials)

# Ruta para ver el material de una materia específica
@app.route('/subject/<subject_name>')
def view_subject(subject_name):
    # Filtrar materiales por materia
    materials = Material.query.filter_by(subject=subject_name).all()
    return render_template('subject_view.html', subject=subject_name, materials=materials)

# Ruta para el dashboard de profesores
@app.route('/teacher_dashboard')
def teacher_dashboard():
    teacher_name = session.get('teacher_name')  # Recupera el nombre del profesor de la sesión
    if not teacher_name:
        return redirect(url_for('login'))

    return render_template('teacher_dashboard.html', teacher_name=teacher_name)

# Ruta para subir materiales o anuncios (solo profesores)
@app.route('/upload_material', methods=['GET', 'POST'])
def upload_material():
    if 'teacher_name' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form['subject']
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        teacher_name = session['teacher_name']

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Guardar el material en la base de datos
            new_material = Material(
                teacher_name=teacher_name,
                subject=subject,
                title=title,
                description=description,
                file_path=file_path
            )
            db.session.add(new_material)
            db.session.commit()

            flash("Material subido exitosamente.")
            return redirect(url_for('teacher_dashboard'))

    return render_template('upload_material.html')

# Ruta para el login (manejando GET y POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user')
    
        if user_type == "student" and username in students and students[username] == password:
            session['student_id'] = username
            return redirect(url_for('student_dashboard'))
        elif user_type == "teacher" and username in teachers and teachers[username] == password:
            session['teacher_name'] = username
            return redirect(url_for('teacher_dashboard'))
        else:
            error = "Credenciales incorrectas. Inténtalo de nuevo."
            return render_template('login.html', error=error)

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
        
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, host='0.0.0.0', port=5009)

