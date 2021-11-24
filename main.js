const {app, BrowserWindow} = require('electron')
const path = require('path')

let mainWindow

function createWindow () {
    mainWindow = new BrowserWindow({
        width: 1440,
        height: 900,
        title: 'phue-racing-flags',
        icon: path.join(__dirname, 'icon.ico'),
        webPreferences: {
            nodeIntegration: true
        },
        autoHideMenuBar: true
    })

    mainWindow.loadURL('http://localhost:8000/index.html');

    mainWindow.on('closed', function () {
        mainWindow = null
    })
}

app.on('ready', createWindow)


app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
})

app.on('activate', function () {
    if (mainWindow === null) createWindow()
})
