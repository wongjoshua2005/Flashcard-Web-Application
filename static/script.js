document.addEventListener("DOMContentLoaded", function() 
{
    const term_list = document.querySelectorAll(".carousel-item");
    let swapped = false;

    term_list.forEach(btn => 
    {
        btn.addEventListener("click", function() 
        {
            const card = this.querySelector(".swap_card");
            const card_definition = this.querySelector(".def");
            const store_term = card.textContent;
    
            card.textContent = card_definition.textContent;
            card_definition.textContent = store_term;
        });
    });
});