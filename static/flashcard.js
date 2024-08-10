/**
 * Joshua Wong
 * Summer 2024
 * flashcard.js
 */

/**
 * The DOMContentLoaded function for the event listener
 * allows the entire DOM to be modified when the user entered
 * the page.
 */
document.addEventListener("DOMContentLoaded", function() 
{
    // To access the list of flashcards
    const term_list = document.querySelectorAll(".carousel-item");

    // Allows each flashcard in the set to be clickable 
    term_list.forEach(btn => 
    {
        /**
         * The click function allows the flashcard to be swapped
         * back and forth with the definition and the term.
         */
        btn.addEventListener("click", function() 
        {
            // To temporarily store the term and access the card text
            // to swap effectively
            const card = this.querySelector(".swap_card");
            const card_definition = this.querySelector(".def");
            const store_term = card.textContent;
    
            // Update the term and definition swaps
            card.textContent = card_definition.textContent;
            card_definition.textContent = store_term;
        });

    });

});