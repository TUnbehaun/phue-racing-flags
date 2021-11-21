export default {
    template: `
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
    `,
    computed: {
        connectionWorks: {
            get() {
                return this.$store.state.connectionWorks;
            }
        }
    }
}