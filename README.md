# phue-racing-flags

## What is phue-racing-flags?

phue-racing-flags is a small tool written in Python, that allows you to use your Philips Hue lights to display the current racing flag of your Assetto Corsa Competizione Race.

## What does it look like?

The design of the app tries to resemble the design of motorsport dashboards like Bosch's DDU systems.

![grafik](https://user-images.githubusercontent.com/12392728/120864997-75105f80-c58d-11eb-9492-2bbec0c6bcf8.png)

## How do I use it?

1. Download the .exe file from here: https://github.com/TUnbehaun/phue-racing-flags/releases/download/v0.1/PhilipsHueRacingFlags.exe
2. Run the .exe file
3. Enter the IP Address of your Philips Hue Bridge in the "bridge ip" input field.
(You can find the IP Address of your Bridge in the interface of your Router)
5. Press the (hardware) link button on your Philips Hue Bridge and then within 30 seconds hit the "Connect" button in the app.
(Pressing the (hardware) link button on your Philips Hue Bridge is only necessary for the very first time you connect the app to a new Bridge)
6. You should be able to choose one of your lights under "flag light" to use as the Racing Flag Light
7. Test the Racing Flag Light by using the buttons under "color test"
8. Adjust brightness if needed
9. To start syncing the Racing Flag Light with the Assetto Corsa Competizione Race Flag click "Start" under "acc sync"
10. To stop syncing the Racing Flag Light with the ACC Race Flag click "Stop" under "acc sync"

## What is the sf.json file used for?

The sf.json file is used for storing your last entries for "bridge ip", "flag light" and "brightness". This brings the convencience, that upon restart of the app, everything is just as you left it. The sf.json file has to be located in the same folder as the .exe file for this to work.

## What is planned for the future?

* Enabling a custom color mapping per flag
* Supporting other sims like iRacing, rFactor, RaceRoom, etc.
* Enabling the mapping of other racing metrics to Philips Hue lights (motor revs, time delta, etc.)
