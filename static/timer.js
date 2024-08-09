document.addEventListener("DOMContentLoaded", () =>
{
    const button = document.querySelector(".timer");
    const display_time = document.querySelector(".time");
    const progress = document.querySelector(".progress_track");
    const original_title = document.title;
    let check_distraction = false;

    const audioCtx = new AudioContext();
    let oscillatorNode;

    document.addEventListener("visibilitychange", (event) => {
        if (document.visibilityState != "visible" && check_distraction) {
            document.title = "YOU'RE DISTRACTED!!!";
            reset_timer = true;
            oscillatorNode = audioCtx.createOscillator();
            oscillatorNode.type = "sine";
            oscillatorNode.frequency.value = 1000;
            oscillatorNode.connect(audioCtx.destination);
            oscillatorNode.start();
        } else {
            document.title = original_title;
            if (oscillatorNode) {
                oscillatorNode.stop();
                oscillatorNode = null;
            }
        }
    });


    const POMO_START = 25;
    const SHORT_BREAK = 5;
    const LONG_BREAK = 10;
    const FIXED_SECS = 0;
    let reset_timer = false;

    let time = new Date();
    time.setMinutes(POMO_START);
    time.setSeconds(FIXED_SECS);
    let count_progress = 0;

    button.addEventListener("click", () =>
    {  
        check_distraction = true;
        let curr_mins = time.getMinutes();
        let curr_secs = time.getSeconds();

        setInterval(() =>
        {
            display_time.textContent = String(curr_mins).padStart(2, '0') + ":"
            + String(curr_secs).padStart(2, '0');
            progress.textContent = count_progress;

            if (curr_mins == 0 && curr_secs == 0 && count_progress != 0 &&
                count_progress % 4 == 0)
            {
                curr_mins = LONG_BREAK;
                curr_secs = FIXED_SECS;
                count_progress += 1
            }
            else if (curr_mins == 0 && curr_secs == 0)
            {
                curr_mins = SHORT_BREAK;
                curr_secs = FIXED_SECS;
                count_progress += 1
            }
            else if (reset_timer)
            {
                curr_mins = POMO_START;
                curr_secs = FIXED_SECS;
                count_progress = 0;
                reset_timer = false;
            }
            else
            {
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