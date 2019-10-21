Blake Emmert
HW06
10/21/19

Watch:
1.) Julia works at National Instruments
2.) PREEMT_RT is a linux kernel patch that also the schdeuler/kernel to run in real time. 
3.) Criticality is a measure of how time sensitive a task is and balancing those tasks.  
4.) Drivers can misbehave by having a long running interrupts in mainline which can prevent other critical threads from running immediately.  
5.) Delta is the time it takes from an event to occur to when the real time task actually executes.
6.) A cyclictest takes a time stamp and sleeps for a fixed duration then takes a time stamp after sleep and the total time minus the sleep time is the delta time.
7.) The figure shows the preempt and preempt_rt plots which shows that the rt system performs better. 
8.) Dispatch latency is the time it takes between the hardware firing and the scheduler being told the task needs to run. Sceduling latency is the amount of time it takes from the time 
the scheduler has been notified to the time the CPU is given the task to execute. 
9.) It is the main schedule for tasks. 
10.) External event can't be scheduled because the low priority interrupt is currently executing in the CPU 
11.) It can start sooner in RT because only small portions of code wake up handler threads to allow for threads to be scheduled immediately. 


PREEMPT_RT:
I measured the response time of the rt kernel and non rt kernel and generated the histogram. I was using a make and make clean as the load. It appears as though the RT kernel has a bounded latency
when compared to the non-RT kernel. You can see my histogram in out.png. 
