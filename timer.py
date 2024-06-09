'''
    Software timer
'''
import numpy as np

NUM_TIMERS = 4

timer_counters = np.zeros(NUM_TIMERS, dtype = int)
timer_flags = np.zeros(NUM_TIMERS, dtype = int)

for i in range(NUM_TIMERS):
    timer_flags[i] = 1
    timer_counters[i] = 0
    
def setTimer(timer_id, duration):
    """
    Sets a timer with a specified duration.
    
    Parameters:
    timer_id (int): The index of the timer to set.
    duration (int): The duration for the timer in seconds.
    """
    if timer_id >= 0 and timer_id < NUM_TIMERS:
        timer_counters[timer_id] = duration
        timer_flags[timer_id] = 0  # Reset the flag when setting the timer
    else:
        raise ValueError("Invalid timer ID. Must be within the range of defined timers.")

def timerRun():
    """
    Decrements active timers and sets flags for timers that reach zero.
    This function should be called periodically to update timers.
    """
    for i in range(NUM_TIMERS):
        if timer_counters[i] > 0:
            timer_counters[i] -= 1
            if timer_counters[i] == 0:
                timer_flags[i] = 1
