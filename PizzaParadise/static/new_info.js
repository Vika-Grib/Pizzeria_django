function new_info(){
    let cart = document.querySelector('.cart');
    cart.innerHTML = '';
    let newDiv = document.createElement('div');
    newDiv.innerHTML = `
        <div class="New info"><h2>Ваш заказ принят! </h2>
        <h2>Номер вашего заказа: </h2>
        </div>`
    cart.appendChild(newDiv);
}