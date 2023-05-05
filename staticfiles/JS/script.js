
function myfunction(){
    let a = document.getElementById('modal');
    a.style.visibility = 'hidden';
}

function myfunction1(){
    let a = document.getElementById('modal');
    a.style.visibility = 'visible';
}


function driver_modal(){
    let a = document.getElementById('driver_data1');
    a.style.visibility = 'hidden';
}

function driver_modal1(){
    let a = document.getElementById('driver_data1');
    a.style.visibility = 'visible';
}


function order_funcktions(a){
    document.getElementById('lol1').style.visibility = 'visible'
    document.getElementById('customer').textContent = document.getElementById(a+'customer1').textContent;
    document.getElementById('phone_number').textContent = document.getElementById(a+'phone_number1').textContent;
    document.getElementById('type').textContent ='Type: ' + document.getElementById(a+'type1').textContent;
    document.getElementById('weight').textContent ='Weight: ' + document.getElementById(a+'weight1').textContent;
    document.getElementById('start_location').textContent ='Start location: ' + document.getElementById(a+'start_location1').textContent;
    document.getElementById('finished_location').textContent ='Fnished location: ' + document.getElementById(a+'finished_location1').textContent;
    document.getElementById('price').textContent ='Delivery fee: ' + document.getElementById(a+'price1').textContent;
    document.getElementById('period').textContent ='Period: ' + document.getElementById(a+'period1').textContent;
    document.getElementById('urlcha').value = a;
}   

function remove_true(){
    console.log(11111111111);
    document.getElementById('remove_modal').style.display = 'block';
}