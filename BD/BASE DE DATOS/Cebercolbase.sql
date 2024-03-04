create database cebercol;
use cebercol; 
create table inmuebles(
codigo integer primary key auto_increment,
foto1 mediumblob,
foto2 mediumblob,
foto3 mediumblob,
foto4 mediumblob,
foto5 mediumblob,
bano int,
habitacion int,
patio varchar(2),
garaje varchar(2),
descripcion varchar(200),
tipo_inmueble varchar(40),
tipo_servicio varchar(10),
precio bigint,
codigo_arrendador integer, foreign key(codigo_arrendador) references personas(codigo),
codigo_barrio integer, foreign key(codigo_barrio) references barrios(codigo));

create table contratos(
codigo integer primary key auto_increment, 
plazo varchar(10), 
canon bigint, 
fecha_inicio date, 
fecha_fin date, 
codigo_inmueble varchar(40), 
codigo_arriendatario integer, foreign key(codigo_arriendatario) references personas(codigo));


create table personas(
codigo integer primary key auto_increment, 
nombre varchar(120), correo varchar(120), 
cedula varchar(10),
telefono bigint,
direccion varchar(20), 
rol varchar(15));

create table recibos(
codigo integer primary key auto_increment, 
codigo_contrato integer, foreign key(codigo_contrato) references contratos(codigo), 
fecha_pago date,
cuota integer,
enero bool,
febrero bool,
marzo bool,
abril  bool,
mayo  bool,
junio bool,
julio bool,
agosto bool,
septiembre bool,
octubre bool,
noviembre bool,
diciembre bool);


create table barrios(
codigo integer primary key auto_increment, 
codigo_comuna integer, foreign key(codigo_comuna) references comunas(codigo), 
nombre varchar(80));

create table comunas(
codigo integer primary key auto_increment, 
nombre varchar(80));

create table solicitudes(
codigo integer primary key auto_increment, 
codigo_inmueble integer, foreign key(codigo_inmueble) references inmuebles(codigo), 
nombre varchar(120), 
telefono bigint); 

create table administrador(
codigo integer primary key auto_increment,
usuario varchar(120),
contrasena varchar(30)
);

use cebercol;