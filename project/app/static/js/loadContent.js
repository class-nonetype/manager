document.addEventListener("DOMContentLoaded", function() {
    getToken();
});

function getToken() {
    fetch("/application/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al obtener el token");
            }
            return response.json();
        })
        .then(data => {
            var token = data.token;
            console.log('Token obtenido:', token);
        })
        .catch(error => {
            console.error('Error al obtener el token:', error.message);
        });
}

function loadContent(page) {
    getToken(); // Obtener el token antes de cargar el contenido
    
    $.ajax({
        url: '/' + page, // Establece la URL del servidor que manejará la solicitud y devolverá el contenido
        method: 'GET',
        success: function(response) {
            $('#content').html(response); // Inserta el contenido recibido en el div con id="content"
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar el contenido:', error);
        }
    });
}
