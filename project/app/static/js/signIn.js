async function signIn() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    const response = await fetch('/sign-in/', {
        method: 'POST',
        body: new URLSearchParams({username: username, password: password}),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });

    const data = await response.json(); // Parsea la respuesta JSON

    if (response.ok) {
        // Éxito en la autenticación
        Swal.fire({
            position: "center",
            icon: "success",
            title: "Inicio de sesión exitoso",
            text: "¡Bienvenido!",
            showConfirmButton: false,
            timer: 1500
        });
    } else {
        // Error en la autenticación
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: data.message || 'Hubo un problema al iniciar sesión. Por favor vuelva a intentarlo nuevamente.',
            showConfirmButton: false,
            timer: 1500
        });
    }
}



async function signIn() {
    var form = document.getElementById('app_login_form');
    var formData = new FormData(form);
    var jsonData = {};

    formData.forEach(function(value, key) {
        jsonData[key] = value;
    });

    fetch('/auth/sign-in/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta del servidor aquí
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}