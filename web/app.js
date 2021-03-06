import SettingsComponent from "./components/SettingsComponent.js";
import NavigationComponent from "./components/NavigationComponent.js";
import MainComponent from "./components/MainComponent.js";
import store from './store.js';


const app = Vue.createApp({
    components: {
        'app-navigation-component': NavigationComponent,
    },
    created() {
        window.addEventListener('beforeunload', this.exitingApp)
    },
    mounted() {
        eel.init_bridge_connection();
    },
    methods: {
        exitingApp: function () {
            eel.stop_sync();
        }
    }
});

const routes = [
    { path: '/', component: MainComponent },
    { path: '/settings', component: SettingsComponent }
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes
});

app.use(router);
app.use(store);

app.mount('#app');

eel.expose(mutate_hue_connection)
function mutate_hue_connection(hueConnection) {
    store.commit('setHueConnection', hueConnection);
}

eel.expose(mutate_connection_works)
function mutate_connection_works(connectionWorks) {
    store.commit('setConnectionWorks', connectionWorks);
}

eel.expose(mutate_available_lights)
function mutate_available_lights(availableLights) {
    store.commit('setAvailableLights', availableLights);
}

eel.expose(mutate_live_sync_running)
function mutate_live_sync_running(liveSyncRunning) {
    store.commit('setLiveSyncRunning', liveSyncRunning);
}
