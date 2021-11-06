const app = Vue.createApp({});

app.component('app-navigation-wrapper', {
    template: `
        <div class="tabs is-centered is-medium">
          <ul>
            <li><router-link to="/">Main</router-link></li>
            <li><router-link to="/assetto-corsa">Assetto Corsa</router-link></li>
            <li><router-link to="/assetto-corsa-competizione">Assetto Corsa Competizione</router-link></li>
            <li><router-link to="/iracing">iRacing</router-link></li>
            <li><router-link to="/settings">Settings</router-link></li>
          </ul>
        </div>
    `
});
const NavigationWrapperComponent = app.component('app-navigation-wrapper');

app.component('app-main', {
    template: `
        <section class="hero is-danger">
          <div class="hero-body">
            <p class="title">
              No Connection!
            </p>
            <p class="subtitle">
              Go to <router-link to="/settings"><strong>Settings</strong></router-link> and establish a connection to your Philips Hue bridge.
            </p>
          </div>
        </section>
    `
});
const MainComponent = app.component('app-main');

app.component('app-settings', {
    template: `
        <div>
            <section class="section">
              <h1 class="title">Philips Hue</h1>
              <label class="label">Bridge IP</label>
              <div class="field has-addons">
                <div class="control">
                  <input class="input" type="text" placeholder="192.168.178.XX">
                  <p class="help">You can find the IP address of your Philips Hue bridge in the interface of your router.</p>
                </div>
                <div class="control">
                  <a class="button is-primary" @click="test">
                    <span class="icon is-small">
                      <i class="fas fa-link"></i>
                    </span>
                    <span>Connect</span>
                  </a>
                </div>
              </div>
              <div class="notification is-warning">
                If you are connecting this app to your bridge for the first time, you have to press the pairing button on your
                bridge and then connect within 30 seconds.
              </div>
            
            
              <br>
            
            
              <div class="columns">
                <div class="column">
                  <label class="label">Lights</label>
                  <div class="field">
                    <div class="select is-multiple">
                      <select multiple size="5">
                        <option value="Light1">Light 1</option>
                        <option value="Light2">Light 2</option>
                        <option value="Light3">Light 3</option>
                        <option value="Light4">Light 4</option>
                        <option value="Light5">Light 5</option>
                        <option value="Light6">Light 6</option>
                      </select>
                    </div>
                    <p class="help">You can can select multiple lights by using Ctrl + Click.</p>
                  </div>
                </div>
                <div class="column">
                  <label class="label">Brightness</label>
                  <input class="slider is-fullwidth is-large" min="1" max="255" step="1" type="range" v-model="brightness">
                  <span class="tag is-medium">{{ brightness }}</span>
                </div>
              </div>
            </section>
            
            
            <section class="section">
              <h1 class="title">Startup</h1>
              <label class="label">Live Sync</label>
              <label class="checkbox">
                <input type="checkbox">
                Enable live sync on startup
              </label>
            </section>
        </div>
    `,
    data() {
        return {
            brightness: 255
        }
    },
    methods: {
        test() {
            eel.test_python_function();
        }
    }
});
const SettingsComponent = app.component('app-settings');

const routes = [
    { path: '/', component: MainComponent },
    { path: '/assetto-corsa', component: MainComponent },
    { path: '/assetto-corsa-competizione', component: MainComponent },
    { path: '/iracing', component: MainComponent },
    { path: '/settings', component: SettingsComponent }
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes
});

eel.expose(test_js_function)
function test_js_function() {
    alert('Coming back from python');
}

app.use(router);

app.mount('#app');
