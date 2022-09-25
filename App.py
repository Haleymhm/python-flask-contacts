from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Variables de conexion de la DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_flask_appcontact'
mysql = MySQL(app)

# settings SESSION
app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    contact = mysql.connection.cursor()
    contact.execute('SELECT * FROM contacts')
    data = contact.fetchall()
    contact.close()
    return render_template('index.html', contacts = data)

@app.route('/add', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        contact = mysql.connection.cursor()
        contact.execute(
            'INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)', 
            (fullname, phone, email)
            )
        mysql.connection.commit()
        contact.close()
        flash('EL Contacto se ha registrado satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_contact(id):
    contact = mysql.connection.cursor()
    contact.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = contact.fetchall()
    contact.close()
    return render_template('edit.html', contact=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        contact = mysql.connection.cursor()
        contact.execute('UPDATE contacts SET fullname = %s, email = %s, phone = %s WHERE id = %s', (fullname, email, phone, id))
        mysql.connection.commit()
        flash('EL Contacto se ha ACTUATUALIZADO satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
    contact = mysql.connection.cursor()
    contact.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('EL Contacto se ha ELIMINADO satisfactoriamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)