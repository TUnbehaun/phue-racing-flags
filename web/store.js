const store = Vuex.createStore({
    state() {
        return {
            hueConnection: {
                ip: '',
                lights: [],
                brightness: 255,
                'sim': 'AC',
                'colors': {
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
                'auto_sync': false
            },
            connectionWorks: false,
            availableLights: [],
            liveSyncRunning: false
        }
    },
    mutations: {
        setHueConnection(state, hueConnection) {
            state.hueConnection = hueConnection;
        },
        setBridgeIp(state, bridgeIp) {
            state.hueConnection.ip = bridgeIp;
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
        },
        setColor(state, { key, value }) {
            state.hueConnection.colors[key] = value;
        },
        setLiveSyncRunning(state, isRunning) {
            state.liveSyncRunning = isRunning;
        },
        setSelectedSim(state, sim) {
            state.hueConnection.sim = sim;
        }
    }
});

export default store;