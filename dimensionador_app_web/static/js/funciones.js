document.getElementById('leerLpnBtn').addEventListener('click', function() {
    const url = `/leer-lpn/?t=${new Date().getTime()}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('lpncard').value = data.lpn;
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('dimensionarBtn').addEventListener('click', function() {
    fetch(`/dimensionar/?t=${new Date().getTime()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('largo').value = data.largo ;
            document.getElementById('ancho').value = data.ancho;
            document.getElementById('altura').value = data.altura;
        })
        .catch(error => console.error('Error:', error));
});
document.getElementById('escaneoCompletoBtn').addEventListener('click', function() {
    fetch(`/leer-lpn/?t=${new Date().getTime()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('lpncard').value = data.lpn;
            return fetch(`/dimensionar/?t=${new Date().getTime()}`);
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('largo').value = data.largo;
            document.getElementById('ancho').value = data.ancho;
            document.getElementById('altura').value = data.altura;
        })
        .catch(error => console.error('Error:', error));
});


function showNotification(message, isSuccess) {
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');
    notificationMessage.textContent = message;
    notification.style.backgroundColor = isSuccess ? 'green' : 'red';
    notification.classList.remove('hidden');
    notification.style.display = 'block';

    setTimeout(hideNotification, 4000);
}

function hideNotification() {
    const notification = document.getElementById('notification');
    notification.classList.add('hidden');
    notification.style.display = 'none';
}

document.getElementById('limpiarBtn').addEventListener('click', function() {
    document.getElementById('lpncard').value = '';
    document.getElementById('largo').value = '0';
    document.getElementById('ancho').value = '0';
    document.getElementById('altura').value = '0';

});