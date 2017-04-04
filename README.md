# VitReous

## Overview
VitReous is an eye-based gesture system for virtual and augmented reality devices! Using EOG, it allows the user to perform actions such as taking pictures and looking through emails without needing to use their hands.

## TODO:
1. Code Review!!
2. Fix multithreading issues.
3. Integrate with Hololens, Google Cardboard, etc

## Code
Code: Contains our code for the mind-controlled bot.

----**OpenBCIPy/src**: Code base

--------*main.py*: Main program; syncs with OpenBCI and runs plugins that can do whatever you want them to do.

--------*open_bci_v3.py*: OpenBCI communications/parsing

--------**plugins**: Contains plugins the main function can use. We want to use 'packets-to-csv' for data collection

--------**biosignals**: Classes with each type of biosignal and its operations

------------*EOG.py*: EOG class. Receives data from OpenBCI, filters noise, and analyzes data to determine eye gestures.

--------*kivy_app.py*: Program that controls GUI

--------**view**: Classes for maintaining graph coordinates

--------**graph**: Kivy graphing package (external)

--------**biosppy**: BioSPPy; biosignals filtering package (external)

#### OpenBCI Signal Acquisition
The original OpenBCI code uses a system of Yapsy plugins you can make to do what you want with the data it obtains. It used to have a command-line interface through which you could add plugins you wanted to use and run. We will keep the system of plugins to keep things modular (and not to break any of their code), but plugins can only be added and started/stopped by the main function itself.

However, we had some problems with using certain packages in the plugins, so we made a plugin currently called 'packets-to-csv' that accepts an array of Biosignals objects and utilizes the Observable-Observer design pattern to update objects with data values from the OpenBCI in real time. (This is a very 'hacky' solution and needs to be fixed).
