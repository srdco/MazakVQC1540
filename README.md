# MazakVQC1540

***USE ALL FILES, SUGGESTIONS, ETC AT YOUR OWN RISK, AND INDEPENDENTLY VERIFY EVERYTHING***
***YOU ALONE ARE RESPONSIBLE FOR ENSURING ACCURACY & SAFETY OF YOURSELF, YOUR MACHINE, AND ALL INVOLVED***
***THESE NOTES, FILES, ETC ARE OFFERED SOLELY AS AN ASSISTANCE, ARE NOT ENTIRELY ACCURATE, ARE NOT INTENDED TO BE IMPLEMENTED AS PRESENTED WITHOUT CORRECTION & MODIFICATION, AND CARRY NO WARRANTY OR GUARANTEE OF ANY KIND!***

***YOU HAVE BEEN WARNED!***

GENERAL NOTES
1. Go to Mitsubishi Automation's website, create a free login and search for TRA-30 (and TRA), the Meldas controller, & the FREQROL spindle controller - the manuals are all free for download for your own use (which is why I can't send them to you). They are LONG, and *somewhat* text-searchable, but invaluable if you spend time poring over them.

2. If you don't have the electronics manual for your mill, see if you can order it - even at a few hundred, it is worth it. We had a full electronics manual for our Mazak, and it made it possible. 

NOTES ON THE DIAGRAMS:
1. Main document is the wiring diagram PDF. This is a line-by-line connection. Some of them need to be updated. Shout if you have questions, I have handwritten notes I haven't updated to the main PDF.

2. Second most important document is the VQC Retrofit spreadsheet, and the Inputs-Outputs list. Really explore the Retrofit spreadsheet.

3. We used an internal PLC, and rewrote the ladder logic to fit the LinuxCNC retrofit (my brother has had some experience with PLC programming). That code is included. There was a minor error in the toolchange ladder logic. When you get to that, email me and I'll send you the updates.

4. You'll need to tune your own servos. Use GNIPSEL's tutorials to start with - they are good. Email me when you get to that and I'll try to find the step-by-step I compiled that works pretty well. It's a long, arduous process - especially your first time.
You may also have to adjust 1 set of potentiometers on each of your servo drives (assuming you keep the original ones, which we did). It is not obvious which ones to adjust, but I think I have notes on those somewhere. If you have the Mits manual for the drives (again, free from the website), then you can identify what the various potentiometers are ... but the descriptions sometimes suffer in clarity after translation from Japanese... Also, Mitsubishi does offer limited phone support on those controllers. Not too helpful, but that is how we found out about the free manuals.

5. We didn't actually wire directly into the ZP1 connector. We made our own 'board' by taking a piece of metal, de-soldering the appropriate connectors from the Meldas control boards, mounting them to our 'board', and soldering (painstakingly!) the various wires from those connectors to the Mesa boards. It was tedious, but worked VERY well. The only possible improvement would be to use more common connectors, and replace the heads on the cables. Keeping the existing (properly shielded, tinned-wire!) cables is invaluable.

6. We used LinuxCNC 2.7 (whatever the latest stable branch was at the time we recontrolled) setup on Debian 9, with the latest stable kernel + userspace (USPACE) realtime patch. LinuxCNC was setup as run-in-place (RIP), which is very handy for updates, etc. Much easier to maintain than pre-built.

7. Our basic computer build is included on the VQC Retrofit Sheet somewhere. I don't remember if it had the latest details. We built the computer for about $250ish, and it works amazingly well. Very snappy, with good latency. Specifically, we used a dual-core (more cores is not better) modern processor (for higher clock speed, but without extra features that can interfere with realtime use), a SSD (very helpful!), a good motherboard, an extra NIC (so we could use the onboard ethernet for the Mesa cards, and the extra ethernet for connecting to our internal network), and a low-cost video card (takes a load off the processor to allow it to be more devoted to realtime, and allows modern hardware to work better with Debian 9 (which at the time had some issues with the Skylake and Kaby Lake processors).

8. We love Gmoccapy. We did add a tweak to allow ignore-limits to be activated from the touchscreen checkbox, which was not incorporated into the main branch due to some misunderstanding of what the change was (they thought it already existed...). It is important to make the interface work easily with the hardwired relay configuration of the Meldas control. The file is included - just replace it in your RIP installation.
We found a used Kiosk touchscreen. It works well, but when we do it again, we would buy a new touchscreen for reliability and greater sensitivity. There was one available from Monoprice for $100 that looked really good about 6months to a year ago, not sure about now.
Even if you use mouse and keyboard, Gmoccapy is still more 'controller-like' and is a little easier to see than Axis (which is good in its own right).

9. Toolchanger/automatic-tool-changer/ATC: The ATC programming, toolchange routine (the python code), and the PLC rungs related to toolchanging I believe are highly specific to the Mazak (a side-mounted, fixed, oval-shaped 16-tool chain toolchanger driven by a hydraulic motor with a Geneva cam). You will likely have to make significant adjustments to make that work. I would recommend getting the mill working first, start making cuts, then integrate the toolchanger. If nothing else, you will be much more familiar with the intricacies by then.

10. Note on HAL (hardware abstraction layer): It seems overwhelming at first, but it's not that bad. If you can think of it like a nested tree: The main hal file (whatever the name of the machine is - in ours it is VQC1540.hal) is the 'master' file. It links specific, physical inputs and outputs (basically all on the MESA boards), to virtual 'signals' which are linked to the various virtual 'boards' in LinuxCNC (the motion control section, input-output control section, etc, etc). We commented ours prolifically to help debugging and reverse-engineering.
For ease of programming and maintenance, not all connections are in the master HAL file. Specific functions are broken out into the atc.hal (toolchanger), the spindle.hal, the plc.hal (all the signals connected to the virtual PLC), etc. These are referenced back to the master HAL file (either in the master hal file or in the VQC1540.ini file, I don't remember which).
The VQC1540.ini file is simply a variable initialization file that LinuxCNC scans at startup to load the various parameters - where machine zero-point is in relation to the limit switches, what direction to home, what parameters to use when driving the servo motors, etc, etc. 
