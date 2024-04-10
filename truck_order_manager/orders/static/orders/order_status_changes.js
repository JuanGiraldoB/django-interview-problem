document.getElementById('change-order-status-form').addEventListener('submit', function (event) {
    event.preventDefault();
    let form = event.target;
    let customerName = form.getAttribute('data-customer-name');
    let restaurantId = form.getAttribute('data-restaurant-id');

    let checkedOrders = [];
    let checkboxes = document.querySelectorAll('input[name="cambiar_estado"]:checked');
    checkboxes.forEach(function(checkbox) {
        checkedOrders.push(checkbox.value);
    });

    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;


    fetch('', {
        method: 'PUT',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ order_ids: checkedOrders, status: 'preparar' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
        // Handle success
        window.location.href = `/order/${restaurantId}/${customerName}`;
        console.log('Order status updated successfully');
        } else {
        console.error('Form errors:', data.errors);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('change-order-status-form-preparacion').addEventListener('submit', function (event) {
    event.preventDefault();
    let form = event.target;
    let customerName = form.getAttribute('data-customer-name');
    let restaurantId = form.getAttribute('data-restaurant-id');
    console.log(customerName)
    console.log(restaurantId)

    let checkedOrders = [];
    let checkboxes = document.querySelectorAll('input[name="cambiar_estado_terminado"]:checked');
    checkboxes.forEach(function(checkbox) {
        checkedOrders.push(checkbox.value);
    });

    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    console.log(checkedOrders)

    fetch('', {
        method: 'PUT',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ order_ids: checkedOrders, status: 'terminar' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
        // Handle success
        window.location.href = `/order/${restaurantId}/${customerName}`;
        console.log('Order status updated successfully');
        } else {
        console.error('Form errors:', data.errors);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

