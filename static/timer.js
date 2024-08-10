/**
 * Joshua Wong
 * Summer 2024
 * timer.js
 */


/**
 * The DOMContentLoaded function for the event listener
 * allows the entire DOM to be modified when the user entered
 * the page. This is only done for the pomodoro timer.
 */
document.addEventListener("DOMContentLoaded", () =>
{
    // To access the button, timer, progress, and the page title
    const button = document.querySelector(".timer");
    const display_time = document.querySelector(".time");
    const progress = document.querySelector(".progress_track");
    const original_title = document.title;
    let check_distraction = false;

    // To setup the beeping noise when user is distracted
    const audioCtx = new AudioContext();
    let oscillatorNode; // To only allow one sound to play at a time

    /**
     * The visibilitychange function for the DOM warns the user
     * when they are distracted or went out of the page.
     */
    document.addEventListener("visibilitychange", (event) => 
    {

        // Checks if the user went out of the web page
        if (document.visibilityState != "visible" && check_distraction) 
        {

            // To reset progress due to user's failed ability to focus
            document.title = "YOU'RE DISTRACTED!!!";
            reset_timer = true;

            // Creates the beeping noise and starts it
            oscillatorNode = audioCtx.createOscillator();
            oscillatorNode.type = "sine";
            oscillatorNode.frequency.value = 1000;
            oscillatorNode.connect(audioCtx.destination);
            oscillatorNode.start();

        } 
        else 
        {
            
            // Makes everything go back to normal when user finally focused
            document.title = original_title;

            // To ensure that the object exists and stops to delete itself
            if (oscillatorNode) 
            {
                oscillatorNode.stop();
                oscillatorNode = null;
            }

        }

    });


    // All the constant pomodoro timer starts
    const POMO_START = 25;
    const SHORT_BREAK = 5;
    const LONG_BREAK = 10;
    const FIXED_SECS = 0;
    let reset_timer = false;

    // Sets up the timer 
    let time = new Date();
    time.setMinutes(POMO_START);
    time.setSeconds(FIXED_SECS);
    let count_progress = 0;

    /**
     * The click function starts the entire
     * pomodoro timer and counts down each second.
     */
    button.addEventListener("click", () =>
    {  
        // To modify the timer when running
        check_distraction = true;
        let curr_mins = time.getMinutes();
        let curr_secs = time.getSeconds();

        /**
         * To decreases time each second and allow the program to run
         * breaks automatically.
         */
        setInterval(() =>
        {
            // Displays the progress and the current time based on 00:00 format
            display_time.textContent = String(curr_mins).padStart(2, '0') + ":"
            + String(curr_secs).padStart(2, '0');
            progress.textContent = count_progress;

            // To allow the user earn long break for their accomplishment
            if (curr_mins == 0 && curr_secs == 0 && count_progress != 0 &&
                count_progress % 4 == 0)
            {
                curr_mins = LONG_BREAK;
                curr_secs = FIXED_SECS;
                count_progress += 1
            }
            // To allow the user to earn a short break
            else if (curr_mins == 0 && curr_secs == 0)
            {
                curr_mins = SHORT_BREAK;
                curr_secs = FIXED_SECS;
                count_progress += 1
            }
            // To restart the timer if the user got distracted
            else if (reset_timer)
            {
                curr_mins = POMO_START;
                curr_secs = FIXED_SECS;
                count_progress = 0;
                reset_timer = false;
            }
            else
            {
                // Decrease time for each second and minutes accordingly
                if (curr_secs == 0 && curr_mins != 0)
                {
                        curr_secs = 59;
                        curr_mins--;
                }
                else
                {
                    curr_secs--;
                }

                time.setMinutes(curr_mins);
                time.setSeconds(curr_secs);
            }

        }, 1000);

    });

});