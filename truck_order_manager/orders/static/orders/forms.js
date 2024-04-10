document.getElementById('order-item-form').addEventListener('submit', function (event) {
    event.preventDefault();
    let formData = new FormData(this);

    fetch('', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('order-item-form').reset();
                document.getElementById('create-order-form').style.display = 'block';
                // Add the saved form item details to the DOM
                let productsInOrderDiv = document.getElementById('div-products-in-order');
                let productDetails = data.order_item; // Assuming the form item details are returned as JSON
                console.log(productDetails)
                addProduct(productDetails, productsInOrderDiv)
                
            } else {
                // Handle form errors
                console.error('Form errors:', data.errors);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

function addProduct(productDetails, productsInOrderDiv){
    let productInfo = document.createElement('p');
    productInfo.textContent = productDetails.name + ' - cantidad: ' + productDetails.quantity + ' - instrucciones: ' + productDetails.details;
    productsInOrderDiv.appendChild(productInfo);
}