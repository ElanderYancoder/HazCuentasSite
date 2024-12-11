if (userId) {
    // Asegúrate de que la URL del WebSocket esté correctamente configurada
    const ws_url = `ws://${window.location.host}/ws/notificaciones/`;  // Cambia la URL según sea necesario
    const notificationSocket = new WebSocket(ws_url);

    notificationSocket.onopen = function() {
        console.log("Conexión WebSocket abierta.");
    };

    notificationSocket.onmessage = function(e) {
        // Asegúrate de que el mensaje recibido tenga el formato adecuado
        const data = JSON.parse(e.data);
        const message = data.message;

        // Muestra la notificación (ejemplo: alert o insertar HTML)
        alert(`Nueva notificación: ${message}`);
    };

    notificationSocket.onclose = function(e) {
        console.error('WebSocket cerrado inesperadamente');
        // Intentar reconectar después de 3 segundos si la conexión se cierra inesperadamente
        setTimeout(function() {
            console.log("Intentando reconectar...");
            notificationSocket = new WebSocket(ws_url); // Reabre la conexión
        }, 3000);  // 3 segundos para intentar reconectar
    };

    notificationSocket.onerror = function(e) {
        console.error("Error en la conexión WebSocket", e);
    };
}
