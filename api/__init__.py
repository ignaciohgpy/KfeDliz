from flask import Flask, render_template, request, redirect,url_for,jsonify,flash
from . import db
from api.db import get_db
import os
import datetime
from . import db



ahora = datetime.datetime.now()
def create_app(instance_relative_config=True):
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
    static_path = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, instance_relative_config=instance_relative_config,template_folder=template_path, static_folder=static_path)
    app.secret_key = 'Mami2025*'
        
    # Ruta a la base de datos dentro de la carpeta 'instance'
    app.config['DATABASE'] = os.path.join(app.instance_path, 'flaskr.sqlite')

    # Asegúrate de que exista la carpeta 'instance'
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    db.init_app(app)
    
    @app.route('/Agregar_Nuevo_Producto', methods=['POST'])
    def agregar_producto():
         db = get_db()
         nombre = request.form['nombre']
         unidad = request.form['Unidad']
         precio = float(request.form['precio'])
         Tipo = request.form['Tipo']
         descrip = request.form['Descripcion']
         cantidad = int(request.form['cantidad'])
         precioV = float(request.form['PrecioV'])
         
         
         
         
         db.execute("""INSERT INTO productos (Nombre, Unidad, Precio, Tipo, Descripcion,Cantidad,PrecioV)VALUES (?, ?, ?, ?, ?, ?, ?)""", (nombre,unidad,precio,Tipo,descrip,cantidad,precioV))
         db.commit()

    # Aquí deberías guardar en tu base de datos o estructura
    # Por ejemplo:
    # productos.append({'nombre': nombre, 'cantidad': cantidad, 'precio': precio})

         return jsonify({'exito': True})
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
         
         
         producto = db.execute('SELECT Cantidad, Precio,id,Nombre FROM productos WHERE id = ?', (id,)).fetchone()
         if producto and producto['cantidad'] >= cantidad_vendida:
              nueva_cantidad = producto['cantidad'] - cantidad_vendida
              db.execute('UPDATE productos SET cantidad = ? WHERE id = ?', (nueva_cantidad, id))
              total=cantidad_vendida*producto['Precio']
              
              db.execute("""INSERT INTO ventas (producto_id, Nombre, Precio, Cantidad, Total, fecha)VALUES (?, ?, ?, ?, ?, ?)""", (id, producto['Nombre'], producto['Precio'], cantidad_vendida, total, ahora.date()))
              db.commit()
         return redirect('/Inventario')
    
    @app.route('/Incremento/<int:id>', methods=['POST'])
    def Incremento_producto(id):
         cantidad_vendida = int(request.form['cantidad_vendida'])
         db = get_db()

         producto = db.execute('SELECT Cantidad, Precio,id,Nombre FROM productos WHERE id = ?', (id,)).fetchone()
         
         nueva_cantidad = producto['cantidad'] + cantidad_vendida
         db.execute('UPDATE productos SET cantidad = ? WHERE id = ?', (nueva_cantidad, id))
         total=cantidad_vendida*producto['Precio']*(-1)
         db.execute("""INSERT INTO ventas (producto_id, Nombre, Precio, Cantidad, Total, fecha)VALUES (?, ?, ?, ?, ?, ?)""", (id, producto['Nombre'], producto['Precio'], cantidad_vendida, total, ahora.date()))
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
        entregado = float(request.form['entregado'])
        db = get_db()
        producto = db.execute(f'SELECT Nombre,Cantidad,Precio FROM productos WHERE id = {producto_id}').fetchall()
        
        
	    
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
            flash(f"No hay suficiente inventario. Stock disponible: {stock_actual}")
            return redirect(url_for('caja'))
	    
        total = precio * cantidad
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if entregado<total:
             flash(f'Dinero insuficiente para completar la venta, faltan {total-entregado}')
             return redirect(url_for('caja'))
			
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
        fechaI = request.args.get('fechaI')
        fechaF = request.args.get('fechaF')
	
        reporteBD=db.execute("""
    SELECT ventas.nombre,  SUM(ventas.cantidad) AS cantidad_Vendida, SUM(ventas.total) AS total_Invertido,SUM(ventas.cantidad)*productos.PrecioV as total_Vendido, SUM(ventas.cantidad)*productos.PrecioV-SUM(ventas.total) as Ganancias
    FROM ventas inner join productos on productos.nombre= ventas.nombre
    WHERE DATE(fecha) BETWEEN	?  and ? and Total>0
    GROUP BY ventas.nombre
""", (fechaI,fechaF)).fetchall()
        
        
        sumatotal=db.execute("""SELECT 
    SUM(cantidad_Vendida) AS cantidad_total,
    SUM(total_Invertido) AS invertido_total,
    SUM(total_Vendido) AS vendido_total,
    SUM(Ganancias) AS ganancias_total
FROM (
    SELECT ventas.nombre,  
           SUM(ventas.cantidad) AS cantidad_Vendida, 
           SUM(ventas.total) AS total_Invertido,
           SUM(ventas.cantidad) * productos.PrecioV AS total_Vendido, 
           SUM(ventas.cantidad) * productos.PrecioV - SUM(ventas.total) AS Ganancias
    FROM ventas 
    INNER JOIN productos ON productos.nombre = ventas.nombre
    WHERE DATE(fecha) BETWEEN	?  and ?  AND ventas.total > 0
    GROUP BY ventas.nombre	
)	""", (fechaI,fechaF)).fetchall()

        db.close()
	
        return render_template('reporte.html', reporte=reporteBD,suma_Inver=sumatotal[0][1],suma_Vend=sumatotal[0][2],suma_Ganan=sumatotal[0][3])    


    @app.route('/caja')
    def caja():
        db = get_db()
        productos = db.execute('SELECT * FROM productos').fetchall()
        db.close()
        return render_template("caja.html", productos=productos)

    # Registrar extensión db
    db.init_app(app)

    return app
