window.onload = () => {
    // 1. Quitar Preloader
    setTimeout(() => {
        const loader = document.getElementById("preloader");
        if(loader) loader.classList.add("hidden");
    }, 900);

    // 2. Cargar Estadísticas Reales
    fetch('/categories/')
        .then(res => res.json())
        .then(data => {
            document.getElementById('count-categorias').innerText = data.length;
        });

    fetch('/workers/')
        .then(res => res.json())
        .then(data => {
            const activos = data.filter(w => w.estado === 'activo').length;
            document.getElementById('count-servicios').innerText = activos;
        });
};