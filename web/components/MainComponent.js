export default {
    template: `
        <div>
            <section v-if="!connectionWorks" class="hero is-danger">
              <div class="hero-body">
                <p class="title">
                  No Connection!
                </p>
                <p class="subtitle">
                  Go to <router-link to="/settings"><strong>Settings</strong></router-link> and establish a connection to your Philips Hue bridge.
                </p>
              </div>
            </section>
            <div v-else>
                <div class="container">
                  <div v-if="liveSyncRunning" class="notification is-primary">
                    <div class="columns">
                        <div class="column">
                            <div class="content is-large">Live Sync Status: <strong>Running</strong></div>      
                        </div>
                        <div class="column">
                            <button v-on:click="stopLiveSync" class="button is-medium" style="float: right;"><span class="icon is-medium"><i class="fas fa-stop"></i></span><span>Stop</span></button>
                        </div>
                    </div>
                  </div>
                  <div v-else class="notification is-danger">
                    <div class="columns">
                        <div class="column">
                            <div class="content is-large">Live Sync Status: <strong>Stopped</strong></div>
                        </div>
                        <div class="column">
                            <button v-on:click="startLiveSync" class="button is-medium" style="float: right;"><span class="icon is-medium"><i class="fas fa-play"></i></span><span>Start</span></button>
                        </div>
                    </div>
                  </div>
                </div>
                
                
                <br>
                
                
                <div class="container">
                    <div class="columns">
                        <div class="column">
                            <div :class="{ selectedCard: selectedSim === 'AC' }" v-on:click="selectSim('AC')" class="card is-clickable">
                              <div class="card-image">
                                <figure class="image">
                                  <img src="../assets/ac.jpg" alt="Placeholder image">
                                </figure>
                              </div>
                              <div class="card-content content">
                                <h2 class="is-large">Assetto Corsa</h2>
                              </div>
                            </div>
                        </div>
                        <div class="column">
                            <div :class="{ selectedCard: selectedSim === 'ACC' }" v-on:click="selectSim('ACC')" class="card is-clickable">
                              <div class="card-image">
                                <figure class="image">
                                  <img src="../assets/acc.jpg" alt="Placeholder image">
                                </figure>
                              </div>
                              <div class="card-content content">
                                <h2 class="is-large">Assetto Corsa Competizione</h2>
                              </div>
                            </div>
                        </div>
                        <div class="column">
                            <div :class="{ selectedCard: selectedSim === 'iRacing' }" v-on:click="selectSim('iRacing')" class="card is-clickable">
                              <div class="card-image">
                                <figure class="image">
                                  <img src="../assets/iracing.jpg" alt="iRacing image">
                                </figure>
                              </div>
                              <div class="card-content content">
                                <h2 class="is-large">iRacing</h2>
                              </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    computed: {
        connectionWorks: {
            get() {
                return this.$store.state.connectionWorks;
            }
        },
        liveSyncRunning: {
            get() {
                return this.$store.state.liveSyncRunning;
            }
        },
        selectedSim: {
            get() {
                return this.$store.state.hueConnection.sim;
            }
        }
    },
    methods: {
        selectSim: function (sim) {
            this.stopLiveSync();
            this.$store.commit('setSelectedSim', sim);
            eel.sync_and_save_hue_connection(this.$store.state.hueConnection);
        },
        startLiveSync: function () {
            this.$store.commit('setLiveSyncRunning', true);
            eel.start_sync();
        },
        stopLiveSync: function () {
            this.$store.commit('setLiveSyncRunning', false);
            eel.stop_sync();
        }
    }
}