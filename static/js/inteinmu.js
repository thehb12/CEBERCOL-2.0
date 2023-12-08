// Función para filtrar los inmuebles
function filtrarInmuebles() {
  var servicioSeleccionado = $("#Servicio").val();
  var tipoInmuebleSeleccionado = $("#TipoInmueble").val();
  var comunaSeleccionada = $("#Comuna").val();
  var habitacionesSeleccionadas = $("#Habitaciones").val();
  var garajeSeleccionado = $("#Garaje").val();

  // Mostrar todos los inmuebles
  $(".propiedad").show();

  // Filtrar por Servicio
  if (servicioSeleccionado !== "Todas") {
    $(".propiedad").each(function () {
      var servicioInmueble = $(this).find("input[name='servicio']").val();
      if (servicioInmueble !== servicioSeleccionado) {
        $(this).hide();
      }
    });
  }

  // Filtrar por Tipo de Inmueble
  if (tipoInmuebleSeleccionado !== "Todas") {
    $(".propiedad").each(function () {
      var tipoInmueble = $(this).find("input[name='tipo']").val();
      if (tipoInmueble !== tipoInmuebleSeleccionado) {
        $(this).hide();
      }
    });
  }

  // Filtrar por Comuna
  if (comunaSeleccionada !== "Todas") {
    $(".propiedad").each(function () {
      var comuna = $(this).find("input[name='comuna']").val();
      if (comuna !== comunaSeleccionada) {
        $(this).hide();
      }
    });
  }

  // Filtrar por Habitaciones
  if (habitacionesSeleccionadas !== "Todas") {
    $(".propiedad").each(function () {
      var habitaciones = $(this).find("input[name='habitaciones']").val();
  
      // Verifica si habitacionesSeleccionadas es igual a "4+" y habitaciones es menor a 4,
      // o si habitacionesSeleccionadas no es "4+" y habitaciones no es igual a habitacionesSeleccionadas
      if ((habitacionesSeleccionadas === "4+" && parseInt(habitaciones, 10) < 4) || 
          (habitacionesSeleccionadas !== "4+" && parseInt(habitaciones, 10) !== parseInt(habitacionesSeleccionadas, 10))) {
        // Oculta el elemento actual si alguna de las condiciones se cumple
        $(this).hide();
      }
    });
  }

  // Filtrar por Garaje
  if (garajeSeleccionado !== "Todas") {
    $(".propiedad").each(function () {
      var garaje = $(this).find("input[name='garaje']").val();
      if (garaje !== garajeSeleccionado) {
        $(this).hide();
      }
    });
  }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
