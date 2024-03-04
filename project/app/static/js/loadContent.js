function loadContent(page) {
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
