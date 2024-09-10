document.getElementById('leerLpnBtn').addEventListener('click', function() {
    fetch('/leer-lpn/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('lpncard').textContent = data.lpn;
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('dimensionarBtn').addEventListener('click', function() {
    fetch('/dimensionar/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('largo').textContent = data.largo;
            document.getElementById('ancho').textContent = data.ancho;
            document.getElementById('altura').textContent = data.altura;
            document.getElementById('peso').textContent = data.peso;
            document.getElementById('infoAdicional').textContent = data.infoAdicional;
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('escaneoCompletoBtn').addEventListener('click', function() {
    fetch('/leer-lpn/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('lpncard').textContent = data.lpn;
        })
        .catch(error => console.error('Error:', error));

    fetch('/dimensionar/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('largo').textContent = data.largo;
            document.getElementById('ancho').textContent = data.ancho;
            document.getElementById('altura').textContent = data.altura;
            document.getElementById('peso').textContent = data.peso;
            document.getElementById('infoAdicional').textContent = data.infoAdicional;
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('limpiarBtn').addEventListener('click', function() {
    document.getElementById('lpncard').textContent = '0';
    document.getElementById('largo').textContent = '0';
    document.getElementById('ancho').textContent = '0';
    document.getElementById('altura').textContent = '0';
    document.getElementById('peso').textContent = '0';
    document.getElementById('infoAdicional').textContent = '0';
});