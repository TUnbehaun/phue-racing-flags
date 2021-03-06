export default {
    template: `
        <div>
        
            <div v-if="showNotification" class="notification is-warning custom-notification">
                <button v-on:click="closeNotification" class="delete"></button>
                <strong>Warning:</strong> No lights are selected!
            </div>
        
            <section class="section">
              <h2 class="title">Philips Hue</h2>
              <label class="label">Bridge IP</label>
              <div class="field has-addons">
                <div class="control">
                  <input v-model="bridgeIp" class="input" type="text" placeholder="192.168.178.XX">
                  <p class="help">You can find the IP address of your Philips Hue bridge in the interface of your router.</p>
                </div>
                <div class="control">
                  <a v-on:click="connect(bridgeIp)" class="button is-primary">
                    <span class="icon is-small">
                      <i class="fas fa-link"></i>
                    </span>
                    <span>Connect</span>
                  </a>
                </div>
              </div>
              <div v-if="!connectionWorks" class="notification is-warning">
                If you are connecting this app to your bridge for the first time, you have to press the pairing button on your
                bridge and then connect within 30 seconds.
              </div>
            
            
              <br>
            
            
              <div class="columns">
                <div class="column">
                  <label class="label">Lights</label>
                  <div class="field">
                    <div class="select is-multiple">
                      <select v-model="selectedLights" multiple size="5">
                        <option v-for="light in availableLights">{{ light }}</option>
                      </select>
                    </div>
                    <p class="help">You can can select multiple lights by using Ctrl + Click.</p>
                  </div>
                </div>
                <div class="column">
                  <label class="label">Brightness</label>
                  <input v-model="brightness" class="slider is-fullwidth is-large" min="1" max="255" step="1" type="range">
                  <span class="tag is-medium">{{ brightness }}</span>
                </div>
              </div>
            </section>
            
            
            <section class="section">
                <h2 class="title">Flags</h2>
                <label class="label">Flag Colors</label>
                <table class="table is-fullwidth is-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Color</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(flag, index) in Object.keys(flags)">
                            <td>{{ flag.replace('_', ' ') }}</td>
                            <td>
                                <input type="color" v-model="Object.values(flags)[index]" v-on:change="changeColor(Object.keys(flags)[index], $event.target.value)" class="is-clickable">
                            </td>
                            <td>
                                <span>&nbsp;</span>
                                <button v-on:click="testLight(Object.keys(flags)[index])" class="button">
                                    <span class="icon is-small"><i class="fas fa-lightbulb"></i></span><span>Test</span>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p class="help">You can set the color to black if you don't want your setup to light up for a certain flag.</p>
            </section>
            
            
            <section class="section">
              <h2 class="title">Startup</h2>
              <label class="label">Live Sync</label>
              <label class="checkbox">
                <input v-model="syncOnStartup" type="checkbox">
                Enable live sync on startup
              </label>
            </section>
            
            
            <section class="section">
                <h2 class="title">Disclaimer</h2>
                <p>This app is not an official product endorsed by Philips, Kunos Simulazioni or iRacing and I am in no way affiliated with them. The images used in the main screen of the app are in-game screenshots from the respective simulations and I explicitly asked for permission, before I included them.</p>
                <br>
                <p>"Hue Personal Wireless Lighting" is a trademark owned by Koninklijke Philips Electronics N.V.</p>
                <p>"Assetto Corsa" and "Assetto Corsa Competizione" are trademarks owned by Kunos Simulazioni S.r.l.</p>
                <p>"iRacing" is a trademark owned by iRacing.com Motorsport Simulations, LLC</p>
            </section>
        </div>
    `,
    data() {
        let showNotification = false;

        return { showNotification }
    },
    computed: {
        connectionWorks: {
            get() {
                return this.$store.state.connectionWorks;
            }
        },
        bridgeIp: {
            get() {
                return this.$store.state.hueConnection.ip;
            },
            set(value) {
                this.$store.commit('setBridgeIp', value);
                eel.sync_and_save_hue_connection(this.$store.state.hueConnection);
            }
        },
        availableLights: {
            get() {
                return this.$store.state.availableLights;
            }
        },
        selectedLights: {
            get() {
                return this.$store.state.hueConnection.lights;
            },
            set(value) {
                this.$store.commit('setSelectedLights', value);
                eel.sync_and_save_hue_connection(this.$store.state.hueConnection);
            }
        },
        brightness: {
            get() {
                return this.$store.state.hueConnection.brightness;
            },
            set(value) {
                this.$store.commit('setBrightness', value);
                eel.sync_and_save_hue_connection(this.$store.state.hueConnection);
            }
        },
        syncOnStartup: {
            get() {
                return this.$store.state.hueConnection.auto_sync;
            },
            set(value) {
                this.$store.commit('setAutoSync', value);
                eel.sync_and_save_hue_connection(this.$store.state.hueConnection);
            }
        },
        flags: {
            get() {
                return this.$store.state.hueConnection.colors;
            }
        }
    },
    methods: {
        connect: function () {
            eel.connect(this.bridgeIp);
        },
        changeColor: function (key, value) {
            this.$store.commit('setColor', { key, value });
            eel.sync_and_save_hue_connection(this.$store.state.hueConnection);
        },
        testLight: function (key) {
            if (this.selectedLights.length === 0) {
                this.showNotification = true;
            } else {
                eel.test_light(key);
            }
        },
        closeNotification: function () {
            this.showNotification = false;
        }
    }
}