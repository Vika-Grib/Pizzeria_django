let openShopping = document.querySelector('.shopping');
let closeShopping = document.querySelector('.closeShopping');
let list = document.querySelector('.list');
let listCard = document.querySelector('.listCard');
let body = document.querySelector('body');
let total = document.querySelector('.total');
let quantity = document.querySelector('.quantity');
let menu_items = document.querySelectorAll('.item')

openShopping.addEventListener('click', ()=>{
    body.classList.add('active');
})
closeShopping.addEventListener('click', ()=>{
    body.classList.remove('active');
})

console.log(menu_items);

let listCards  = [];


function fetch_current_data(){
return fetch('/static/pizzas.json')
    .then((response) => {var j = response.json()
    return j});
    }

let products = [];

js = fetch_current_data();
console.log(js);
val = js.then(value => {var v = value
var rows = v['rows']
rows.forEach((element) => products.push(row));})
console.log(products)



function addToCard(key){
    if(listCards[key] == null){
        // копируем наш список в корзину
        console.log(JSON.stringify(menu_items[key-1]))
        console.log(menu_items[key-1])
        listCards[key-1] = JSON.parse(JSON.stringify(menu_items[key-1]));
        listCards[key-1].quantity = 1;
    }
    reloadCard();
}
function reloadCard(){
    listCard.innerHTML = '';
    let count = 0;
    let totalPrice = 0;
    listCards.forEach((value, key)=>{
        totalPrice = totalPrice + value.price;
        count = count + value.quantity;
        if(value != null){
            let newDiv = document.createElement('li');
            newDiv.innerHTML = `
                <div><img src="image/${value.image}"/></div>
                <div>${value.name}</div>
                <div>${value.price.toLocaleString()}</div>
                <div>
                    <button onclick="changeQuantity(${key}, ${value.quantity - 1})">-</button>
                    <div class="count">${value.quantity}</div>
                    <button onclick="changeQuantity(${key}, ${value.quantity + 1})">+</button>
                </div>`;
                listCard.appendChild(newDiv);
        }
    })
    total.innerText = totalPrice.toLocaleString();
    quantity.innerText = count;
}
function changeQuantity(key, quantity){
    if(quantity == 0){
        delete listCards[key];
    }else{
        listCards[key].quantity = quantity;
        listCards[key].price = quantity * products[key].price;
    }
    reloadCard();
}