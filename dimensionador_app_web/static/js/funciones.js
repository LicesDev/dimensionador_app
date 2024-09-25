function limpiar() {
    document.getElementById('lpncard').value = '';
    document.getElementById('largo').textContent = '0';
    document.getElementById('ancho').textContent = '0';
    document.getElementById('altura').textContent = '0';
    document.getElementById('peso').textContent = '0';
    document.getElementById('infoAdicional').textContent = '0';
}

document.getElementById('leerLpnBtn').addEventListener('click', function() {
    limpiar();
    const url = `/leer-lpn/?t=${new Date().getTime()}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('lpncard').value = data.lpn;
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('dimensionarBtn').addEventListener('click', function() {
    limpiar();
    fetch(`/dimensionar/?t=${new Date().getTime()}`)
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
    limpiar();
    fetch(`/leer-lpn/?t=${new Date().getTime()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('lpncard').value = data.lpn;
        })
        .catch(error => console.error('Error:', error));

    fetch(`/dimensionar/?t=${new Date().getTime()}`)
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

document.getElementById('limpiarBtn').addEventListener('click', limpiar);