function showNotification(message, isSuccess) {
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');
    notificationMessage.textContent = message;
    notification.style.backgroundColor = isSuccess ? 'green' : 'red';
    notification.classList.remove('hidden');
    notification.style.display = 'block';

    // Ocultar la notificación después de 4 segundos
    setTimeout(hideNotification, 4000);
}

function hideNotification() {
    const notification = document.getElementById('notification');
    notification.classList.add('hidden');
    notification.style.display = 'none';
}

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío del formulario

    const formData = new FormData(event.target);
    fetch(event.target.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showNotification(data.message, true);
        } else {
            showNotification(data.message, false);
        }
    })
    .catch(error => {
        showNotification('Error en la solicitud', false);
    });
});
