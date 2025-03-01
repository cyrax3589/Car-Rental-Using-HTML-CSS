// Fetch available cars
fetch('/cars')
    .then(response => response.json())
    .then(data => {
        const carList = document.getElementById('car-list');
        carList.innerHTML = '';

        if (Array.isArray(data) && data.length > 0) {
            data.forEach(car => {
                carList.innerHTML += `
                    <div class="car-card">
                        <h3>${car.make} ${car.model} (${car.year})</h3>
                        <p>Price: $${car.price_per_day}/day</p>
                        <p>Registration: ${car.registration_number}</p>
                    </div>
                `;
            });
        } else {
            carList.innerHTML = '<p>No cars available right now.</p>';
        }
    })
    .catch(error => {
        console.error('Error fetching cars:', error);
        document.getElementById('car-list').innerHTML = '<p style="color: red;">Failed to load cars. Check your server connection.</p>';
    });

// Add a new customer
document.getElementById('customer-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const customerData = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value
    };

    fetch('/customers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customerData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('customer-form').reset();
    });
});