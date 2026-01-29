document.addEventListener('DOMContentLoaded', function() {
    fetch('/categories/') // Llama al Blueprint de Python
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById('grid-categorias');
            grid.innerHTML = ''; // Limpiamos el cargador

            data.forEach(cat => {
                // Creamos la tarjeta usando las clases de tu CSS original
                const card = document.createElement('div');
                card.className = 'categoria-card';
                card.innerHTML = `
                    <div class="card-content">
                        <img src="/static/upload/${cat.imagen || 'default.jpg'}" alt="${cat.nombre}">
                        <h3>${cat.nombre}</h3>
                        <p>${cat.descripcion}</p>
                        <a href="/subcategorias?id=${cat.id}" class="btn-ver">Ver Especialidades</a>
                    </div>
                `;
                grid.appendChild(card);
            });
        })
        .catch(error => console.error('Error:', error));
});