if (!!window.EventSource) {
    var source = new EventSource("/camara/sse");  // Asegúrate de que la ruta sea correcta
    source.onmessage = function(event) {
        document.getElementById("contenidoTarjeta").innerText = "QR encontrado: " + event.data;
    };
} else {
    console.log("Your browser does not support SSE");
}

function updateTime() {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString();
    const formattedDate = now.toLocaleDateString();
    document.getElementById('current-time').textContent = `${formattedDate} ${formattedTime}`;
    document.getElementById('fecha').value = `${formattedDate}`;
}

setInterval(updateTime, 1000);
updateTime();