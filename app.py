from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Diccionarios de usuarios
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

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el dashboard de estudiantes
@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')

# Ruta para el dashboard de profesores
@app.route('/teacher_dashboard')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

# Ruta para el login (manejando GET y POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        username = request.form['username']
        password = request.form['password']

        # Validar credenciales en estudiantes
        if username in students and students[username] == password:
            return redirect(url_for('student_dashboard'))  # Redirigir al dashboard de estudiantes

        # Validar credenciales en profesores
        elif username in teachers and teachers[username] == password:
            return redirect(url_for('teacher_dashboard'))  # Redirigir al dashboard de profesores

        else:
            # Si las credenciales son incorrectas, mostrar el formulario con un mensaje de error
            error = "Credenciales incorrectas. Inténtalo de nuevo."
            return render_template('login.html', error=error)

    # Si es una solicitud GET, mostrar el formulario sin mensaje de error
    return render_template('login.html')
    # Ruta para el dashboard de estudiantes
    @app.route('/student_dashboard')
    def student_dashboard():
        return render_template('student_dashboard.html')
    
    # Ruta para el dashboard de profesores
    @app.route('/teacher_dashboard')
    def teacher_dashboard():
        return render_template('teacher_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5009)

