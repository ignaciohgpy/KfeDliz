BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "post" (
	"id"	INTEGER,
	"author_id"	INTEGER NOT NULL,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"title"	TEXT NOT NULL,
	"body"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("author_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "ventas" (
	"id"	INTEGER UNIQUE,
	"producto_id"	INTEGER NOT NULL,
	"Nombre"	TEXT NOT NULL,
	"Cantidad"	REAL NOT NULL,
	"Precio"	REAL NOT NULL,
	"fecha"	TEXT NOT NULL,
	"Total"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "productos" (
	"Nombre"	TEXT NOT NULL UNIQUE,
	"id"	INTEGER NOT NULL UNIQUE,
	"Cantidad"	NUMERIC NOT NULL,
	"Unidad"	TEXT NOT NULL,
	"Precio"	NUMERIC,
	"figura"	TEXT,
	"Tipo"	TEXT,
	"Descripcion"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "ventas" ("id","producto_id","Nombre","Cantidad","Precio","fecha","Total") VALUES (1,2,'Jamon Embuchado',5.0,150.0,'2025-07-15 00:13:03',750.0);
INSERT INTO "ventas" ("id","producto_id","Nombre","Cantidad","Precio","fecha","Total") VALUES (2,1,'Cervezas Un Laguer',3.0,250.0,'2025-07-17',750.0);
INSERT INTO "ventas" ("id","producto_id","Nombre","Cantidad","Precio","fecha","Total") VALUES (3,3,'Maltas',5.0,300.0,'2025-07-16 00:22:17',1500.0);
INSERT INTO "ventas" ("id","producto_id","Nombre","Cantidad","Precio","fecha","Total") VALUES (4,3,'Maltas',5.0,300.0,'2025-07-17 00:24:52',1500.0);
INSERT INTO "ventas" ("id","producto_id","Nombre","Cantidad","Precio","fecha","Total") VALUES (5,1,'Cervezas Un Laguer',10.0,250.0,'2025-07-17 23:27:02',2500.0);
INSERT INTO "productos" ("Nombre","id","Cantidad","Unidad","Precio","figura","Tipo","Descripcion") VALUES ('Cervezas Un Laguer',1,86,'U',250,'Unlaguer.png','L','Fria cerveza, para el verano');
INSERT INTO "productos" ("Nombre","id","Cantidad","Unidad","Precio","figura","Tipo","Descripcion") VALUES ('Jamon Embuchado',2,40,'LBR',150,'JamonE.png','A','Jamon de cerdo Importado');
INSERT INTO "productos" ("Nombre","id","Cantidad","Unidad","Precio","figura","Tipo","Descripcion") VALUES ('Maltas',3,170,'U',300,'Malta.png','L','Fria malta Cubana');
INSERT INTO "productos" ("Nombre","id","Cantidad","Unidad","Precio","figura","Tipo","Descripcion") VALUES ('Picadillo',4,200,'LBR',100,'Picadillo.png','A','Delicioso picadillo de Pollo');
COMMIT;
