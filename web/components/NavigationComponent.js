export default {
    template: `
        <div class="tabs is-centered is-medium">
          <ul>
            <router-link custom v-slot="{ isActive, href }" to="/"><li :class="isActive && 'is-active'"><a :href="href">Main</a></li></router-link>
            <router-link custom v-slot="{ isActive, href }" to="/assetto-corsa"><li :class="isActive && 'is-active'"><a :href="href">Assetto Corsa</a></li></router-link>
            <router-link custom v-slot="{ isActive, href }" to="/assetto-corsa-competizione"><li :class="isActive && 'is-active'"><a :href="href">Assetto Corsa Competizione</a></li></router-link>
            <router-link custom v-slot="{ isActive, href }" to="/iracing"><li :class="isActive && 'is-active'"><a :href="href">iRacing</a></li></router-link>
            <router-link custom v-slot="{ isActive, href }" to="/settings"><li :class="isActive && 'is-active'"><a :href="href">Settings</a></li></router-link>
          </ul>
        </div>
    `
}