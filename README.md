[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">phue-racing-flags</h3>

  <p align="center">
    Use your Philips Hue lights as Racing Flags.
    <br />
    <br />
    <a href="https://github.com/TUnbehaun/phue-racing-flags"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/TUnbehaun/phue-racing-flags/issues">Report Bug</a>
    ·
    <a href="https://github.com/TUnbehaun/phue-racing-flags/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#supported-systems-and-racing-simulators">Supported Systems and Racing Simulators</a></li>
    <li>
      <a href="#local-development">Local Development</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li><li>
        <a href="#run-the-app">Run the app</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![grafik](https://user-images.githubusercontent.com/12392728/120900824-6aaaa000-c637-11eb-8abb-c7b271e3dde7.png)

One Friday evening I thought to myself that it would be pretty sweet to use my Philips Hue lights as indicators for the racing flags inside of Assetto Corsa Competizione. As no app was available to achieve this, I decided to take matters into my own hand and create one.

### Built With

* [Python](https://www.python.org/)

## Supported Systems and Racing Simulators

The app is designed for Windows and currently only supports Assetto Corsa Competizione. Supporting other racing simulators is planned for the future.

<!-- GETTING STARTED -->
## Local Development

To get a local development copy up and running follow these simple steps.

### Prerequisites

* Python
  https://www.python.org/downloads/

### Installation

* Clone the repo
   ```sh
   git clone https://github.com/TUnbehaun/phue-racing-flags.git
   ```
### Run the app

* Start the GUI
  ```sh
   python gui.py
   ```

<!-- USAGE EXAMPLES -->
## Usage

To just use the app itself without setting up a local development copy, you can follow these simple steps:

1. Download the latest .exe file from here: https://github.com/TUnbehaun/phue-racing-flags/releases/latest/download/phue-racing-flags.exe
2. Run the .exe file

Once the app is started, you can use it the following way:

1. Enter the IP Address of your Philips Hue Bridge in the "bridge ip" input field.
(You can find the IP Address of your Bridge in the interface of your Router)
2. Press the (hardware) link button on your Philips Hue Bridge and then within 30 seconds hit the "Connect" button in the app.
(Pressing the (hardware) link button on your Philips Hue Bridge is only necessary for the very first time you connect the app to a new Bridge)
3. You should be able to choose one or multiple of your lights under "flag light" to use as the Racing Flag Light(s)
4. Test the Racing Flag Light(s) by using the buttons under "color test"
5. Adjust brightness if needed
6. To start syncing the Racing Flag Light(s) with the Assetto Corsa Competizione Race Flag click "Start" under "acc sync"
7. To stop syncing the Racing Flag Light(s) with the ACC Race Flag click "Stop" under "acc sync"

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/TUnbehaun/phue-racing-flags/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Tim Unbehaun - tim@defacto.cool

Project Link: [https://github.com/TUnbehaun/phue-racing-flags](https://github.com/TUnbehaun/phue-racing-flags)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [phue](https://github.com/studioimaginaire/phue)
* [PySimpleGui](https://github.com/PySimpleGUI/PySimpleGUI)
* [PyInstaller](http://www.pyinstaller.org/)

## Disclaimer

I am in no way affiliated with the Philips organization or Kunos Simulazioni.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[forks-shield]: https://img.shields.io/github/forks/TUnbehaun/phue-racing-flags.svg?style=for-the-badge
[forks-url]: https://github.com/TUnbehaun/phue-racing-flags/network/members
[stars-shield]: https://img.shields.io/github/stars/TUnbehaun/phue-racing-flags.svg?style=for-the-badge
[stars-url]: https://github.com/TUnbehaun/phue-racing-flags/stargazers
[issues-shield]: https://img.shields.io/github/issues/TUnbehaun/phue-racing-flags.svg?style=for-the-badge
[issues-url]: https://github.com/TUnbehaun/phue-racing-flags/issues
[license-shield]: https://img.shields.io/github/license/TUnbehaun/phue-racing-flags.svg?style=for-the-badge
[license-url]: https://github.com/TUnbehaun/phue-racing-flags/blob/master/LICENSE.txt

