from flask import Flask, render_template, request, redirect,url_for
from . import db
from api.db import get_db
import os
import datetime
from . import db




def create_app(instance_relative_config=True):
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
    static_path = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, instance_relative_config=instance_relative_config,template_folder=template_path, static_folder=static_path)
    
        
    # Ruta a la base de datos dentro de la carpeta 'instance'
    app.config['DATABASE'] = os.path.join(app.instance_path, 'flaskr.sqlite')

    # Asegúrate de que exista la carpeta 'instance'
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    db.init_app(app)
    
    @app.route('/')
    @app.route('/index')
    def hello():
        db = get_db()
        productosA = db.execute('SELECT * FROM productos where tipo="A"').fetchall()
        productosL = db.execute('SELECT * FROM productos where tipo="L"').fetchall()
        db.close()
        return render_template('index.html', productosL=productosL,productosA=productosA)

    @app.route('/Inventario')
    def inventario():
        db = get_db()
        productos = db.execute('SELECT * FROM productos').fetchall()
        return render_template('Inventario.html', productos=productos)
    @app.route('/vender/<int:id>', methods=['POST'])
    def vender_producto(id):
         cantidad_vendida = int(request.form['cantidad_vendida'])
         db = get_db()

         producto = db.execute('SELECT cantidad FROM productos WHERE id = ?', (id,)).fetchone()
         if producto and producto['cantidad'] >= cantidad_vendida:
              nueva_cantidad = producto['cantidad'] - cantidad_vendida
              db.execute('UPDATE productos SET cantidad = ? WHERE id = ?', (nueva_cantidad, id))
              db.commit()
         return redirect('/Inventario')
    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar_producto(id):
       db = get_db()
       if request.method == 'POST':
           nombre = request.form['nombre']
           cantidad = request.form['cantidad']
           precio = request.form['precio']
           db.execute(
                'UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?',
                (nombre, cantidad, precio, id)
                )
           db.commit()
           return redirect('/inventario')
       else:
           producto = db.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
           return render_template('editar.html', producto=producto)
    @app.route('/eliminar/<int:id>')
    def eliminar_producto(id):
        db = get_db()
        db.execute('DELETE FROM productos WHERE id = ?', (id,))
        db.commit()
        return redirect('/inventario')
    

    @app.route('/registrar_venta', methods=['POST'])
    def registrar_venta():
        producto_id = request.form['producto_id']
       
        cantidad = int(request.form['cantidad'])
        db = get_db()
        producto = db.execute(f'SELECT Nombre,Cantidad,Precio FROM productos WHERE id = {producto_id}').fetchall()
        for i in producto:
            print(i)
        
	    
	    ##conn = db.connect()
	    ##conn.row_factory = sqlite3.Row
	    ##cursor = conn.cursor()
	
	    #producto = db.get("SELECT * FROM producto WHERE id = ?", (producto_id,))
	    
        if not producto:
            db.close()
            return "Producto no encontrado", 404
	    
        stock_actual = producto[0][1]
        precio = producto[0][2]
        nombre = producto[0][0]
	
        if cantidad > stock_actual:
            db.close()
            return f"No hay suficiente inventario. Stock disponible: {stock_actual}", 400
	    
        total = precio * cantidad
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	    # Registrar la venta
        db.execute("""INSERT INTO ventas (producto_id, nombre, precio, cantidad, total, fecha)VALUES (?, ?, ?, ?, ?, ?)""", (producto_id, nombre, precio, cantidad, total, fecha))
	
	    # Actualizar inventario
        nuevo_stock = stock_actual - cantidad
        db.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nuevo_stock, producto_id))
	
        db.commit()
        db.close()
	
        return redirect(url_for('caja'))
    @app.route('/reporte_ventas')
    def reporte_ventas():
        db = get_db()
        fecha = request.args.get('fecha')
        
	
        reporteBD=db.execute("""
    SELECT nombre, SUM(cantidad) AS total_cantidad, SUM(total) AS total_ventas
    FROM ventas
    WHERE DATE(fecha) = ?
    GROUP BY nombre
""", (fecha,)).fetchall()
        
        
        sumatotal=db.execute("""SELECT SUM(total) FROM ventas WHERE DATE(fecha) = ? """, (fecha,)).fetchall()

        db.close()
	
        return render_template('reporte.html', reporte=reporteBD,fecha=fecha,suma_total=sumatotal[0][0])    


    @app.route('/caja')
    def caja():
        db = get_db()
        productos = db.execute('SELECT * FROM productos').fetchall()
        db.close()
        return render_template("caja.html", productos=productos)

    # Registrar extensión db
    db.init_app(app)

    return app
