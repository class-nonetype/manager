async function getApplication() {
    const token = localStorage.getItem('Authorization');
    if (!token) {
        console.error('No se encontró un token de autenticación en el almacenamiento local');
        return;
    }

    const url = '/application/';

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'text/html', // Esperamos una respuesta HTML
                'Authorization': token
            }
        });
        
        console.log(response);

        if (response.ok) {
            const htmlResponse = await response.text(); // Obtener el contenido HTML como texto
            // Renderizar el HTML en tu aplicación cliente
            document.body.innerHTML = htmlResponse;
        } else {
            console.error('Error al obtener la aplicación:', response.statusText);
        }
    } catch (error) {
        console.error('Error de red:', error);
    }
}


async function signIn() {
    var form = document.getElementById('app_login_form');
    var formData = new FormData(form);
    var jsonData = {};

    formData.forEach(function(value, key) {
        jsonData[key] = value;
    });

    Swal.fire({
        title: 'Iniciando sesión',
        allowOutsideClick: false,
        showCancelButton: false,
        showConfirmButton: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch('/auth/sign-in/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => {
        // Obtener el statusCode de la respuesta
        const statusCode = response.status;

        // Devolver la respuesta en formato JSON
        return response.json().then(data => ({ statusCode, data }));
    })
    .then(({ statusCode, data }) => {
        Swal.close();

        console.log(data);
        if (statusCode === 200) {
            Swal.fire({
                position: "center",
                icon: "success",
                title: "Inicio de sesión exitoso",
                text: "¡Bienvenido!",
                showConfirmButton: false,
                timer: 2500
            }).then(() => {
                console.log(data.access_token);

                localStorage.setItem('Authorization', `Bearer ${data.access_token}`);

                // Realizar la solicitud GET a la página de aplicación
                getApplication();
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error al iniciar sesión',
                text: 'Por favor, verifica tus credenciales.',
                showConfirmButton: false,
                timer: 2500
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);

        Swal.fire({
            icon: 'error',
            title: 'Error al iniciar sesión',
            text: 'Se produjo un error al intentar iniciar sesión. Por favor, inténtalo de nuevo más tarde.'
        });
    });
}

