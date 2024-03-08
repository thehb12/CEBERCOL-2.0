
from flask import Flask, render_template, request, url_for, redirect, flash, Response,  jsonify, send_file
from flask_mysqldb import MySQL
from openpyxl import Workbook
from io import BytesIO
import pymysql
import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
app = Flask(__name__)

# CONEXION MYSQL


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cebercol'
mysql = MySQL(app)

# SESION


app.secret_key = 'mysecretkey'

# VER CONTRATOS


@app.route('/contratos')
def contratos():
    # Obtener el número de página de la URL, por defecto es 1
    page = request.args.get('page', 1, type=int)
    items_per_page = 5  # Número máximo de contratos por página

    # Calcular el desplazamiento en la base de datos
    offset = (page - 1) * items_per_page

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contratos')
    total_contratos = len(cur.fetchall())
    # Calcular el número total de páginas
    total_pages = (total_contratos + items_per_page - 1) // items_per_page

    cur.execute("""
                SELECT contratos.*,
                personas.nombre AS nombre_inquilino
                FROM contratos
                INNER JOIN personas ON contratos.codigo_arriendatario=personas.codigo
                LIMIT %s OFFSET %s
    """, (items_per_page, offset))
    contratos = cur.fetchall()

    cur.execute("SELECT * FROM personas WHERE rol='Inquilino'")
    personas = cur.fetchall()

    cur.execute("""
                SELECT inmuebles.*,
                barrios.nombre AS nombre_barrio
                FROM inmuebles
                INNER JOIN barrios ON inmuebles.codigo_barrio=barrios.codigo
                LIMIT %s OFFSET %s
    """, (items_per_page, offset))
    inmuebles = cur.fetchall()

    return render_template('adminc.html', contratos=contratos, personas=personas, inmuebles=inmuebles, current_page=page, total_pages=total_pages)

# AGREGAR CONTRATOS


@app.route('/add_contrato', methods=['POST'])
def add_contrato():
    if request.method == 'POST':
        Codigo_inmueble = request.form['CodigoInmueble']
        Codigo_arrendatario = request.form['CodigoArrendatario']
        Plazo = request.form['Plazo']
        Fecha_inicio = request.form['FechaInicio']
        Fecha_fin = request.form['FechaFin']
        Canon = request.form['Canon']
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO contratos(plazo,canon,fecha_inicio,fecha_fin,codigo_inmueble,codigo_arriendatario) VALUES (%s,%s,%s,%s,%s,%s)', (
                Plazo, Canon, Fecha_inicio, Fecha_fin, Codigo_inmueble, Codigo_arrendatario))
        cur.execute("SELECT * FROM personas WHERE rol='Inquilino'")
        personas = cur.fetchall()
        mysql.connection.commit()
        flash('Se Agrego Correctamente')
        return redirect(url_for('contratos'))

# AGREGAR CONTRATO DIRECTO


@app.route('/add_contratod/<codigo>')
def get_contratod(codigo):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personas WHERE rol='Inquilino'")
    personas = cur.fetchall()
    cur.execute('SELECT * FROM inmuebles WHERE codigo=%s', (codigo,))
    data = cur.fetchall()
    return render_template('adminc-directo.html', inmueble=data[0], personas=personas)


@app.route('/add_contratodi/<codigo>', methods=['POST'])
def add_contratodi(codigo):
    if request.method == 'POST':
        Codigo_inmueble = request.form['CodigoInmueble']
        Codigo_arrendatario = request.form['CodigoArrendatario']
        Plazo = request.form['Plazo']
        Fecha_inicio = request.form['FechaInicio']
        Fecha_fin = request.form['FechaFin']
        Canon = request.form['Canon']
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO contratos(plazo,canon,fecha_inicio,fecha_fin,codigo_inmueble,codigo_arriendatario) VALUES (%s,%s,%s,%s,%s,%s)', (
                Plazo, Canon, Fecha_inicio, Fecha_fin, Codigo_inmueble, Codigo_arrendatario))
        mysql.connection.commit()
        flash('Se Agrego Correctamente')
        return redirect(url_for('contratos'))

# ELIMINAR CONTRATOS


@app.route('/deletec/<string:codigo>')
def delete_contrato(codigo):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contratos WHERE codigo={0}'.format(codigo))
    mysql.connection.commit()
    flash('Se Elimino Correctamente')
    return redirect(url_for('contratos'))

# EDITAR CONTRATOS


@app.route('/editc/<codigo>')
def get_contrato(codigo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contratos WHERE codigo=%s', (codigo))
    data = cur.fetchall()
    return render_template('adminc-edit.html', contrato=data[0])


@app.route('/updatec/<codigo>', methods=['POST'])
def edit_contrato(codigo):
    if request.method == 'POST':
        Codigo_inmueble = request.form['CodigoInmueble']
        Codigo_arrendatario = request.form['CodigoArrendatario']
        Plazo = request.form['Plazo']
        Fecha_inicio = request.form['FechaInicio']
        Fecha_fin = request.form['FechaFin']
        Canon = request.form['Canon']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contratos
            SET plazo=%s,
                canon=%s,
                fecha_inicio=%s,
                fecha_fin=%s,
                codigo_inmueble=%s,
                codigo_arriendatario=%s
            WHERE codigo=%s
        """, (Plazo, Canon, Fecha_inicio, Fecha_fin, Codigo_inmueble, Codigo_arrendatario, codigo))
        mysql.connection.commit()
        flash('Se Edito Correctamente')
        return redirect(url_for('contratos'))

# VER RECIBOS


@app.route('/recibos')
def recibos():
    # Obtener el número de página de la URL, por defecto es 1
    page = request.args.get('page', 1, type=int)
    items_per_page = 5  # Número máximo de recibos por página

    # Calcular el desplazamiento en la base de datos
    offset = (page - 1) * items_per_page

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM recibos LIMIT %s OFFSET %s',
                (items_per_page, offset))
    recibos = cur.fetchall()

    # Obtener el número total de recibos (sin paginación)
    cur.execute("SELECT COUNT(*) FROM recibos")
    total_recibos = cur.fetchone()[0]

    # Calcular el número total de páginas
    total_pages = (total_recibos + items_per_page - 1) // items_per_page

    cur.execute('SELECT * FROM contratos')
    contratos = cur.fetchall()

    return render_template('adminr.html', recibos=recibos, contratos=contratos, current_page=page, total_pages=total_pages)


@app.route('/obtener_contrato/<codigo_contrato>')
def obtener_contrato(codigo_contrato):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT plazo, canon FROM contratos WHERE codigo = %s', (codigo_contrato,))
    contrato_info = cur.fetchone()
    cur.close()

    return jsonify({'plazo': contrato_info[0], 'canon': contrato_info[1]})


# AGREGAR RECIBO


@app.route('/add_recibo', methods=['POST'])
def add_recibo():
    if request.method == 'POST':
        codigo_contrato = request.form['codigoContrato']
        fecha_pago = request.form['CurrentDate']
        cuota = request.form['Cuota']

        # Obtén los valores booleanos de los meses del formulario
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        meses_bool = {mes: request.form.get(mes) == 'on' for mes in meses}

        # Configuración de la base de datos y cursor (puedes ajustar esto según tu lógica)
        cur = mysql.connection.cursor()

        # Genera la cadena de nombres de campos y valores para la consulta SQL
        campos = ', '.join(meses_bool.keys())
        valores = ', '.join(['%s' for _ in meses_bool])

        valores_tuple = (codigo_contrato, fecha_pago, cuota) + \
            tuple(meses_bool.values())
        valores_tuple += (False,) * (len(meses) - len(meses_bool))

        cur.execute(
            f'INSERT INTO recibos(codigo_contrato, fecha_pago, cuota, {campos}) VALUES (%s, %s, %s, {valores})',
            valores_tuple
        )

        mysql.connection.commit()
        flash('Se Agregó Correctamente')
        return redirect(url_for('recibos'))


# ELIMINAR RECIBO


@app.route('/deleter/<string:codigo>')
def delete_recibo(codigo):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM recibos WHERE codigo={0}'.format(codigo))
    mysql.connection.commit()
    flash('Se Elimino Correctamente')
    return redirect(url_for('recibos'))

# EDITAR RECIBO


# VER PERSONAS


@app.route('/personas')
def personas():
    # Obtener el número de página de la URL, por defecto es 1
    page = request.args.get('page', 1, type=int)
    items_per_page = 5  # Número máximo de personas por página

    # Calcular el desplazamiento en la base de datos
    offset = (page - 1) * items_per_page

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas LIMIT %s OFFSET %s',
                (items_per_page, offset))
    personas = cur.fetchall()

    # Obtener el número total de personas (sin paginación)
    cur.execute("SELECT COUNT(*) FROM personas")
    total_personas = cur.fetchone()[0]

    # Calcular el número total de páginas
    total_pages = (total_personas + items_per_page - 1) // items_per_page

    return render_template('adminp.html', personas=personas, current_page=page, total_pages=total_pages)

# AGREGAR PERSONAS


@app.route('/add_persona', methods=['POST'])
def add_persona():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Correo = request.form['Correo']
        Cedula = request.form['Cedula']
        Telefono = request.form['Telefono']
        Direccion = request.form['Direccion']
        Rol = request.form['Rol']
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO personas(nombre, correo, cedula, telefono, direccion, rol) VALUES (%s,%s,%s,%s,%s,%s)', (Nombre, Correo, Cedula, Telefono, Direccion, Rol))
        mysql.connection.commit()
        flash('Se Agrego Correctamente')
        return redirect(url_for('personas'))

# ELIMINAR PERSONAS


@app.route('/deletep/<string:codigo>')
def delete_persona(codigo):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM personas WHERE codigo={0}'.format(codigo))
    mysql.connection.commit()
    flash('Se Elimino Correctamente')
    return redirect(url_for('personas'))

# EDITAR PERSONAS


@app.route('/editp/<codigo>')
def get_persona(codigo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas WHERE codigo=%s', (codigo))
    data = cur.fetchall()
    return render_template('adminp-edit.html', persona=data[0])


@app.route('/updatep/<codigo>', methods=['POST'])
def edit_persona(codigo):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Correo = request.form['Correo']
        Cedula = request.form['Cedula']
        Telefono = request.form['Telefono']
        Direccion = request.form['Direccion']
        Rol = request.form['Rol']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE personas
            SET nombre=%s,
                correo=%s,
                cedula=%s,
                telefono=%s,
                direccion=%s,
                rol=%s
            WHERE codigo=%s
        """, (Nombre, Correo, Cedula, Telefono, Direccion, Rol, codigo))
        mysql.connection.commit()
        flash('Se Edito Correctamente')
        return redirect(url_for('personas'))
# VER INMUEBLES


@app.route('/admini')
def admini():
    # Obtener el número de página de la URL, por defecto es 1
    page = request.args.get('page', 1, type=int)
    items_per_page = 5  # Número máximo de inmuebles por página

    # Calcular el desplazamiento en la base de datos
    offset = (page - 1) * items_per_page

    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT inmuebles.*, barrios.codigo_comuna,
                barrios.nombre AS nombre_barrio,
                personas.nombre AS nombre_arrendador
                FROM inmuebles
                INNER JOIN barrios ON inmuebles.codigo_barrio=barrios.codigo
                INNER JOIN personas ON inmuebles.codigo_arrendador=personas.codigo
                LIMIT %s OFFSET %s
    """, (items_per_page, offset))

    inmuebles = cur.fetchall()

    # Obtener el número total de inmuebles
    cur.execute("SELECT COUNT(*) FROM inmuebles")
    total_inmuebles = cur.fetchone()[0]
    cur.execute("SELECT * FROM personas WHERE rol='Propietario'")
    personas = cur.fetchall()

    cur.execute("SELECT * FROM barrios")
    barrios = cur.fetchall()
    # Calcular el número total de páginas
    total_pages = (total_inmuebles + items_per_page - 1) // items_per_page

    return render_template('admin.html', barrios=barrios, inmuebles=inmuebles, current_page=page, total_pages=total_pages, personas=personas)


# AGREGAR INMUEBLES


@app.route('/add_inmueble', methods=['POST'])
def add_inmueble():
    if request.method == 'POST':
        Descripcion = request.form['Descripcion']
        Tipo_inmueble = request.form['Tipo']
        Ubicacion = request.form['Ubicacion']
        Habitaciones = request.form['Habitaciones']
        Banos = request.form['Banos']
        Garaje = request.form['Garaje']
        Precio = request.form['Precio']
        Arrendador = request.form['Arrendador']
        Servicio = request.form['Servicio']
        Patio = request.form['Patio']

        fotos = []  # Lista para almacenar los datos de las imágenes

        for foto in request.files.getlist('Foto'):
            if foto:
                img_data = foto.read()  # Leer los datos binarios de la imagen
                # Agregar los datos de la imagen a la lista
                fotos.append(img_data)
            else:
                # Si no se proporciona una imagen, almacenar None
                fotos.append(None)

        # Verificar que haya al menos 5 imágenes
        while len(fotos) < 5:
            # Rellenar con None si no se proporcionan suficientes imágenes
            fotos.append(None)

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO inmuebles(foto1,foto2,foto3,foto4,foto5,descripcion,patio,tipo_servicio,tipo_inmueble,codigo_barrio,habitacion,bano,garaje,precio,codigo_arrendador) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (fotos[0], fotos[1], fotos[2], fotos[3], fotos[4], Descripcion, Patio, Servicio, Tipo_inmueble, Ubicacion, Habitaciones, Banos, Garaje, Precio, Arrendador))
        mysql.connection.commit()
        flash('Se Agregó Correctamente')
        return redirect(url_for('admini'))

# EDITAR INMUEBLES


@app.route('/edit/<codigo>')
def get_inmueble(codigo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inmuebles WHERE codigo=%s', (codigo,))
    data = cur.fetchall()
    cur.execute("SELECT * FROM personas WHERE rol='Propietario'")
    personas = cur.fetchall()
    return render_template('admin-edit.html', inmueble=data[0], personas=personas)


@app.route('/update/<codigo>', methods=['POST'])
def edit_inmueble(codigo):
    if request.method == 'POST':
        Descripcion = request.form['Descripcion']
        Tipo_inmueble = request.form['Tipo']
        Ubicacion = request.form['Ubicacion']
        Habitaciones = request.form['Habitaciones']
        Banos = request.form['Banos']
        Garaje = request.form['Garaje']
        Precio = request.form['Precio']
        Arrendador = request.form['Arrendador']
        Servicio = request.form['Servicio']
        Patio = request.form['Patio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE inmuebles
            SET descripcion=%s,
                patio=%s,
                tipo_servicio=%s,
                tipo_inmueble=%s,
                codigo_barrio=%s,
                habitacion=%s,
                bano=%s,
                garaje=%s,
                precio=%s,
                codigo_arrendador=%s
            WHERE codigo=%s
        """, (Descripcion, Patio, Servicio, Tipo_inmueble, Ubicacion, Habitaciones, Banos, Garaje, Precio, Arrendador, codigo))
        mysql.connection.commit()
        flash('Se Edito Correctamente')
        return redirect(url_for('admini'))

# ELIMINAR INMUEBLES


@app.route('/delete/<string:codigo>')
def delete_inmueble(codigo):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inmuebles WHERE codigo={0}'.format(codigo))
    mysql.connection.commit()
    flash('Se Elimino Correctamente')
    return redirect(url_for('admini'))

# Descargar reporte
# pip install openpyxl


@app.route('/descargar_excel', methods=['GET'])
def descargar_excel():
    cur = mysql.connection.cursor()
    cur.execute('''
                SELECT 
                p.nombre AS Nombre, 
                p.correo AS Correo, 
                p.cedula AS Cedula, 
                p.telefono AS Telefono, 
                i.tipo_inmueble AS Tipo, 
                b.nombre AS Barrio, 
                c.codigo AS 'ID Contrato', 
                c.plazo AS Plazo, 
                c.canon AS Canon
                FROM 
                personas p
                INNER JOIN contratos c
                INNER JOIN inmuebles i ON c.codigo_inmueble = i.codigo
                INNER JOIN barrios b ON i.codigo_barrio = b.codigo
                WHERE Rol="Inquilino";
                ''')
    reportes = cur.fetchall()

    # Crear un libro de trabajo de Excel y seleccionar la hoja activa
    wb = Workbook()
    ws = wb.active

    # Agregar los encabezados de las columnas
    ws.append(['Nombre', 'Correo', 'Cedula', 'Telefono', 'Tipo',
              'Barrio', 'ID Contrato', 'Plazo', 'Canon'])

    # Agregar los datos de los reportes a las filas
    for reporte in reportes:
        ws.append(reporte)

    # Guardar el libro de trabajo en un objeto BytesIO
    excel_io = BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)

    # Devolver el archivo Excel como una respuesta para descargar
    return Response(
        excel_io.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            "Content-disposition": "attachment; filename=reporte.xlsx"
        }
    )


@app.route('/descargar_excel2', methods=['GET'])
def descargar_excel2():
    cur = mysql.connection.cursor()
    cur.execute('''
                SELECT 
                r.fecha_pago AS Fecha, 
                i.tipo_inmueble AS Inmueble, 
                p.cedula AS Cedula, 
                p.nombre AS Nombre, 
                r.codigo AS 'ID Recibo', 
                c.canon AS Valor
                FROM 
                personas p
                INNER JOIN contratos c
                INNER JOIN inmuebles i ON c.codigo_inmueble = i.codigo
                INNER JOIN recibos r
                WHERE 
                r.marzo = "1" AND p.rol = "Inquilino";
                ''')
    reportes = cur.fetchall()

    # Crear un libro de trabajo de Excel y seleccionar la hoja activa
    wb = Workbook()
    ws = wb.active

    # Agregar los encabezados de las columnas
    ws.append(['Fecha', 'Inmueble', 'Cedula', 'Nombre', 'ID recibo',
              'Valor'])

    # Agregar los datos de los reportes a las filas
    for reporte in reportes:
        ws.append(reporte)

    # Guardar el libro de trabajo en un objeto BytesIO
    excel_io = BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)

    # Devolver el archivo Excel como una respuesta para descargar
    return Response(
        excel_io.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            "Content-disposition": "attachment; filename=reportepagos.xlsx"
        }
    )


# NAVEGACION


@app.route('/')
def inicio():
    return render_template('inteindex.html')


@app.route('/reporteI')
def reporteI():
    cur = mysql.connection.cursor()
    cur.execute('''
                SELECT 
                p.nombre AS Nombre, 
                p.correo AS Correo, 
                p.cedula AS Cedula, 
                p.telefono AS Telefono, 
                i.tipo_inmueble AS Tipo, 
                b.nombre AS Barrio, 
                c.codigo AS 'ID Contrato', 
                c.plazo AS Plazo, 
                c.canon AS Canon
                FROM 
                personas p
                INNER JOIN contratos c
                INNER JOIN inmuebles i ON c.codigo_inmueble = i.codigo
                INNER JOIN barrios b ON i.codigo_barrio = b.codigo
                WHERE Rol="Inquilino";
                ''')
    reportes = cur.fetchall()
    return render_template('reportesinquilino.html', reportes=reportes)


@app.route('/reporteP')
def reporteP():
    cur = mysql.connection.cursor()
    cur.execute('''
                SELECT 
                r.fecha_pago AS Fecha, 
                i.tipo_inmueble AS Inmueble, 
                p.cedula AS Cedula, 
                p.nombre AS Nombre, 
                r.codigo AS 'ID Recibo', 
                c.canon AS Valor
                FROM 
                personas p
                INNER JOIN contratos c
                INNER JOIN inmuebles i ON c.codigo_inmueble = i.codigo
                INNER JOIN recibos r
                WHERE 
                r.marzo = "1" AND p.rol = "Inquilino";;
                ''')
    reportes = cur.fetchall()
    return render_template('reportespagos.html', reportes=reportes)


@app.route('/login')
def intelogin():
    return render_template('intelogin.html')


@app.route('/index')
def inteindex():
    return render_template('inteindex.html')


@app.route('/detalles/<codigo>')
def intedetalle(codigo):
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT inmuebles.*, barrios.codigo_comuna,
                barrios.nombre AS nombre_barrio
                FROM inmuebles
                INNER JOIN barrios ON inmuebles.codigo_barrio = barrios.codigo
                WHERE inmuebles.codigo = %s
    """, (codigo,))
    inmuebles = cur.fetchall()
    return render_template('intedetalle.html', inmuebles=inmuebles)


@app.route('/consultar')
def consultar():
    return render_template('consultar.html')


@app.route('/inmuebles')
def inteinmu():
    # Obtener el número de página de la URL, por defecto es 1
    page = request.args.get('page', 1, type=int)
    items_per_page = 8  # Número máximo de inmuebles por página

    # Calcular el desplazamiento en la base de datos
    offset = (page - 1) * items_per_page

    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT inmuebles.*,barrios.codigo_comuna,
                barrios.nombre AS nombre_barrio
                FROM inmuebles
                INNER JOIN barrios ON inmuebles.codigo_barrio=barrios.codigo
                LIMIT %s OFFSET %s
    """, (items_per_page, offset))
    inmuebles = cur.fetchall()

    # Obtener el número total de inmuebles
    cur.execute("SELECT COUNT(*) FROM inmuebles")
    total_inmuebles = cur.fetchone()[0]

    # Calcular el número total de páginas
    total_pages = (total_inmuebles + items_per_page - 1) // items_per_page

    return render_template('inteinmu.html', inmuebles=inmuebles, current_page=page, total_pages=total_pages)


@app.route('/contratod')
def contratod():
    return render_template('adminc-directo.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
