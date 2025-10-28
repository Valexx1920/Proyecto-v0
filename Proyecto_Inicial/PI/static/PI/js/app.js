const map = L.map('map').setView([-33.45, -70.66], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos => {
        L.marker([pos.coords.latitude, pos.coords.longitude])
            .addTo(map)
            .bindPopup('Tu ubicación');
    });
}

const prendas = [
  { nombre: 'Polera Negra', talla: 'M' },
  { nombre: 'Jeans Azul', talla: '38' },
];

const cards = document.getElementById('cards');
prendas.forEach(p => {
    const div = document.createElement('div');
    div.className = 'card';
    div.textContent = p.nombre + ' - Talla ' + p.talla;
    cards.appendChild(div);
});
