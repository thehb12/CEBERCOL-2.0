
Julian
#ICON DE LAS PAGINAS
#TITULOS
#Boton regresar
#Agregar una seccion sobre los servicios en index
#Hacer que el boton de servicios me lleve a esa seccion del index
#Acomodar footer (texto-datos-ubicacion)
#arreglar css intedetalle
#slider o carrucel arreglar o hacer otro

Juan
#Mostrar imagenes(esta en veremos)
#Enviar solicitud(facil)
#registrar en contrato y inmueble a la persona(facil)
#En inmueble agregar comuna para filtrar los barrios(ya no es necesario porque lo hace el exotiqueo que hice en clase)


MENSAJES
{% with messages = get_flashed_messages() %} {% if messages %} {% for
      message in messages %}
      <p>{{message}}</p>
      {% endfor %} {% endif %} {% endwith %}