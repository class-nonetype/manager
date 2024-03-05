async function createProject() {
    const projectName = document.getElementById('project_name').value.trim();
    if (!projectName) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Por favor, introduce un nombre para el proyecto.',
            showConfirmButton: false,
            timer: 1500
        });
        return;
    }

    const response = await fetch('/create/project/', {
        method: 'POST',
        body: new URLSearchParams({project_name: projectName}),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });

    if (response.ok) {
        Swal.fire({
            position: "center",
            icon: "success",
            title: "Proyecto creado",
            text: "Se ha creado correctamente el proyecto '"+ projectName + "'.",
            showConfirmButton: false,
            timer: 1500
          });
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un problema al crear el proyecto.',
            showConfirmButton: false,
            timer: 1500
        });
    }
}



document.querySelector('.app_button_create_project').addEventListener('click', createProject);
