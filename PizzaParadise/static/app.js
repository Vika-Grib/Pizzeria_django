let openShopping = document.querySelector('.shopping');
let closeShopping = document.querySelector('.closeShopping');
let list = document.querySelector('.list');
let listCard = document.querySelector('.listCard');
let body = document.querySelector('body');
let total = document.querySelector('.total');
let quantity = document.querySelector('.quantity');

openShopping.addEventListener('click', ()=>{
    body.classList.add('active');
})
closeShopping.addEventListener('click', ()=>{
    body.classList.remove('active');
})

let listCards  = [];  //эта переменная отвечает за продукты, добавленные в корзину когда кликаешь

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
rows.forEach((element) => products.push(element));})
console.log(products)

let max_key = 0


function addToCard(key, price, size){
    max_key = reloadCard();
    if(listCards[max_key] == null){
        // копируем наш список в корзину
        console.log(products[key-1])
        listCards[max_key] = JSON.parse(JSON.stringify(products[key-1]));
        listCards[max_key].price = price;  // чтобы цена каждого размера пиццы считалось
        listCards[max_key].quantity = 1;
        if (size == 2){
        listCards[max_key].size = 'большая'
        } else if (size == 3){
        listCards[max_key].size = 'стандартная'
        } else if (size == 4){
        listCards[max_key].size = 'тонкое тесто'
        }
        listCards[max_key].default_price = size
    }
    max_key = reloadCard();
}

let max_key_1 = 0
function reloadCard(){
    listCard.innerHTML = '';
    let count = 0;
    let totalPrice = 0;
    let default_price = 0
    listCards.forEach((value, key)=>{
        default_price = products[key][value.default_price]
        totalPrice = totalPrice + value.price;
        count = count + value.quantity;
        if(value != null){
            console.log(key, listCards.length)
            if (key == listCards.length-1){
            max_key_1 = key+1
            }
            let newDiv = document.createElement('li');
            newDiv.innerHTML = `
                <div><img src=${value[6]}></div>
                <div>${value[1]}</div>
                <div>${value.price.toLocaleString()}0</div>
                <div>${value.size}</div>
                <div>
                    <button onclick="changeQuantity(${key}, ${value.quantity - 1}, ${default_price})">-</button>
                    <div class="count">${value.quantity}</div>
                    <button onclick="changeQuantity(${key}, ${value.quantity + 1}, ${default_price})">+</button>
                </div>`;
                listCard.appendChild(newDiv); //listCard - отвечает за то, что хранит в себе часть кода от корзины и мы можем +- пиццы
        }
    })
    total.innerText = totalPrice.toLocaleString() + '0';
    quantity.innerText = count;
    return max_key_1
}

function changeQuantity(key, quantity, price){   // если мы ум количество одного продукта до 0, то он удаляется
    if(quantity == 0){
        delete listCards[key];
    }else{
        listCards[key].quantity = quantity;
        listCards[key].price = quantity * price;
    }
    reloadCard();
}