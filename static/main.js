
//This is the code for implementing the fruits and vegetables query
let first_input = document.querySelector("#fruitq")
first_input.addEventListener('input', async function () {
    let first_response = await fetch("/queryfruit?fruit=" + first_input.value);
    let final = await first_response.text()
    document.querySelector(".fruit_ul").innerHTML = final
});

//This is the code for implementing the meat and poultry query
let second_input = document.querySelector("#meatq")
second_input.addEventListener('input', async function () {
    let second_response = await fetch("/querymeat?meat=" + second_input.value);
    let second_final = await second_response.text()
    document.querySelector(".meat_ul").innerHTML = second_final
});

//This is the code for implementing the frozen query
let third_input = document.querySelector("#frozenq")
third_input.addEventListener('input', async function () {
    let third_response = await fetch("/queryfrozen?froze=" + third_input.value);
    let third_final = await third_response.text()
    document.querySelector(".frozen_ul").innerHTML = third_final
});

//This is the code for implementing the dairy query
let fourth_input = document.querySelector("#dairyq")
fourth_input.addEventListener('input', async function () {
    let fourth_response = await fetch("/querydairy?dairyEggs=" + fourth_input.value);
    let fourth_final = await fourth_response.text()
    document.querySelector(".dairy_ul").innerHTML = fourth_final
});

//This is the code for implementing the cupboard query
let fifth_input = document.querySelector("#cupboardq")
fifth_input.addEventListener('input', async function () {
    let fifth_response = await fetch("/querycupboard?cupb=" + fifth_input.value);
    let fifth_final = await fifth_response.text()
    document.querySelector(".cupboard_ul").innerHTML = fifth_final
});

//This is the code for implementing the snack query
let sixth_input = document.querySelector("#snacksq")
sixth_input.addEventListener('input', async function () {
    let sixth_response = await fetch("/querysnacks?snack=" + sixth_input.value);
    let sixth_final = await sixth_response.text()
    document.querySelector(".snacks_ul").innerHTML = sixth_final
});

//This is the code for implementing the beverages query

let seventh_input=document.querySelector("#beverageq")
seventh_input.addEventListener('input',async function (){
    let seventh_response=await fetch("/querybeverages?beverage=" + seventh_input.value);
    let seventh_final=await seventh_response.text()
    document.querySelector(".beverages_ul").innerHTML=seventh_final
});

//This is the code for implementing the detergent query
let eigth_input = document.querySelector("#detergentq")
eigth_input.addEventListener('input', async function () {
    let eigth_response = await fetch("/querydetergents?detergent=" + eigth_input.value);
    let eigth_final = await eigth_response.text()
    document.querySelector(".detergents_ul").innerHTML = eigth_final
});

