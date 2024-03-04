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
                window.location.href = '/application/';

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



// test

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
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}` // Agrega el token al encabezado de autorización
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
                localStorage.setItem('token', data.access_token);

                const token = localStorage.getItem('token');
                console.log(token);


                window.location.href = '/application/';

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
