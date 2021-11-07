const store = Vuex.createStore({
    state() {
        return {
            hueConnection: {
                ip: '',
                lights: [],
                brightness: 255,
                'sim': 'AC',
                'colors': {
                    'AC': {
                        'No_Flag': '',
                        'Blue_Flag': '#0D47A1',
                        'Yellow_Flag': '#FFEB3B',
                        'Black_Flag': '',
                        'White_Flag': '#ffffff',
                        'Checkered_Flag': '',
                        'Penalty_Flag': '#b71c1c'
                    },
                    'ACC': {
                        'No_Flag': '',
                        'Blue_Flag': '#0D47A1',
                        'Yellow_Flag': '#FFEB3B',
                        'Black_Flag': '',
                        'White_Flag': '#FFEB3B',
                        'Checkered_Flag': '',
                        'Penalty_Flag': '#b71c1c',
                        'Green_Flag': '#388E3C',
                        'Orange_Flag': '#FF6F00'
                    },
                    'iRacing': {
                        'No_Flag': '',
                        'Blue_Flag': '#0D47A1',
                        'Yellow_Flag': '#FFEB3B',
                        'Black_Flag': '',
                        'White_Flag': '#FFEB3B',
                        'Checkered_Flag': '',
                        'Red_Flag': '#b71c1c',
                        'Green_Flag': '#388E3C',
                        'Meatball_Flag': '#FF6F00'
                    }
                },
                'auto_sync': false
            },
            connectionWorks: false,
            availableLights: []
        }
    },
    mutations: {
        setHueConnection(state, hueConnection) {
            state.hueConnection = hueConnection;
            console.log(state.hueConnection);
        },
        setBridgeIp(state, bridgeIp) {
            state.hueConnection.bridgeIp = bridgeIp;
        },
        setSelectedLights(state, selectedLights) {
            state.hueConnection.lights = selectedLights;
        },
        setBrightness(state, brightness) {
            state.hueConnection.brightness = brightness;
        },
        setAutoSync(state, autoSync) {
            state.hueConnection.auto_sync = autoSync;
        },
        setConnectionWorks(state, connectionWorks) {
            state.connectionWorks = connectionWorks;
        },
        setAvailableLights(state, availableLights) {
            state.availableLights = availableLights;
        }
    }
});

export default store;