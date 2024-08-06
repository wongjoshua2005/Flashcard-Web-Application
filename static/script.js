document.addEventListener("DOMContentLoaded", function() 
{
    const card_btn = document.querySelector(".create_card");

    card_btn.addEventListener("click", function() 
    {
        const card_container = document.querySelector(".card-container");
        const title_input = document.querySelector(".user_input");
        const title_value = title_input.value;
    
        const card = document.createElement("div");
        card.setAttribute("class", "card text-center mb-3");
        card.style.width = "18rem";
        const card_body = document.createElement("div");
        card_body.setAttribute("class", "card-body");
        const card_title = document.createElement("h3");
        card_title.style.padding = "20px";
        card_title.setAttribute("class", "card-title");
        card_title.textContent = title_value;
        const submit_btn = document.createElement("a");
        submit_btn.setAttribute("class", "btn btn-primary");
        submit_btn.textContent = "Start studying!";
    
        card_container.appendChild(card);
        card.appendChild(card_body);
        card_body.appendChild(card_title);
        card_body.appendChild(submit_btn);
    });
});