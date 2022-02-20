# Alpine Ski Racing Timer

## System Architecture

<img width=750 alt="System Architecture Diagram" src="https://user-images.githubusercontent.com/90717831/153794187-3a2d924e-e8b6-44ff-8e26-b49ccfc2ff9f.png">

<img width=750 src="https://user-images.githubusercontent.com/90717831/153795193-1965a564-5203-4cbf-95af-d997cd457424.png">

## Python Code

The current python code in the GitHub repository is outdated. It is a designed to be used on a PC system, rather than an actual raspberry pi. So, it has a PyQt5 based GUI instead of the eInk display that is included in the final product. I would upload code for the eInk display, except my only copy is in the raspberry pi, which is located in Davis, California at my parent's house, and I am currently in Tempe, Arizona.

<img width=400 src="https://user-images.githubusercontent.com/90717831/154823883-bd4b637a-74dd-4a94-8b13-2cb2e4ba2b9e.jpeg" align="left">
<img width=350 src="https://user-images.githubusercontent.com/90717831/154823886-5b8f92cb-5180-482e-b38d-f11ec28e9176.png" align="left">

<br clear="left"/>
<br clear="left"/>

These are the two interfaces I developed for the timer. I used the first interface (left) for testing while developing the Python code on my personal computer. I used the second interface (right) on the final product. The main differences between the two is that the first interface took input through a mouse and keyboard, whereas the second interface took input through a numerical keyboard and four physical buttons. The first interface was also configured for a typical LCD display, but the second interface was configured for an eInk display.

The three boxes in the center represent up to three racers currently on the course. When a racer lines up to start their race, they enter in their id number into the numerical keyboard. Then, when they cross the starting line, they push aside a "baton," which presses a physical button. That physical button sends a signal to the Python code, starting the timer. The race operator can cancel any racer's time (this is useful if the racer falls) by pressing one of three physical buttons that corresponds to each racer currenly on the race course.

The bottom Raspberry Pi connects to the local wireless network hosted by the top Raspberry Pi. The Python code running on the bottom Pi automatically connects to a socket server hosted by the top Pi. Then, the bottom Pi constantly monitors a photoresistor circuit for variations and reports to the top Pi whenever the laser beam is broken. When this occurs, the top Pi ends the current racer's time.

## Node.JS Server

<img width=200 src="https://user-images.githubusercontent.com/90717831/154824057-83f8bf6b-1f40-43f2-838d-87d328c60b26.png" align="left">

The Node.JS server hosts a website on the Raspberry Pis local wireless network. It displays each racer's time, along with their name and id number. I had planned to implement a system for racers to enter in their name, so it could be automatically matched with their id number, however, I never ended up completing it. The times can be sorted most recent or the lowest time.

<br clear="left"/>

## SQL Server

The SQL server has two tables, one for times and one for users. Since I never completed the system to match racers' ids with their names, I did not complete the user table. The times table has columns: id, start_time, end_time, net_time, and racer_name. I used different query commands to sort the times by either most recent or lowest time, depending on where the information was requested from.

## Linux Configuration

Both Raspberry Pis run the Raspbian Linux distro. I configured the OS to start the Python code, SQL server, Node.JS server, and a local wireless network upon bootup.
