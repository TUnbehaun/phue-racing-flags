# phue-racing-flags

## What is phue-racing-flags?

phue-racing-flags is a small tool written in Python, that allows you to use your Philips Hue lights to display the current racing flag of your Assetto Corsa Competizione Race.

## What does it look like?

The design of the app tries to resemble the design of motorsport dashboards like Bosch's DDU systems.

![grafik](https://user-images.githubusercontent.com/12392728/120900824-6aaaa000-c637-11eb-8abb-c7b271e3dde7.png)

## How do I use it?

1. Download the .exe file from here: https://github.com/TUnbehaun/phue-racing-flags/releases/latest/download/phue-racing-flags.exe
2. Run the .exe file
3. Enter the IP Address of your Philips Hue Bridge in the "bridge ip" input field.
(You can find the IP Address of your Bridge in the interface of your Router)
5. Press the (hardware) link button on your Philips Hue Bridge and then within 30 seconds hit the "Connect" button in the app.
(Pressing the (hardware) link button on your Philips Hue Bridge is only necessary for the very first time you connect the app to a new Bridge)
6. You should be able to choose one or multiple of your lights under "flag light" to use as the Racing Flag Light(s)
7. Test the Racing Flag Light(s) by using the buttons under "color test"
8. Adjust brightness if needed
9. To start syncing the Racing Flag Light(s) with the Assetto Corsa Competizione Race Flag click "Start" under "acc sync"
10. To stop syncing the Racing Flag Light(s) with the ACC Race Flag click "Stop" under "acc sync"

## What is the phue-rf-save.json file used for?

The phue-rf-save file is used for storing your last entries for "bridge ip", "lights" and "brightness". This brings the convencience, that upon restart of the app, everything is just as you left it. The phue-rf-save file has to be located in the same folder as the .exe file for this to work.

## What is planned for the future?

* Enabling a custom color mapping per flag
* Supporting other sims like iRacing, rFactor, RaceRoom, etc.
* Enabling the mapping of other racing metrics to Philips Hue lights (motor revs, time delta, etc.)
