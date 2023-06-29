<template>
  <div>
    <q-list>
      <q-item-label header>
        Maps
      </q-item-label>
      <MapSidebarLinkGroup
        v-for="game in games"
        v-bind:key="game"
        :groupName="game"
        :maps="maps_for_game(game)"/>
    </q-list>
  </div>
</template>

<script lang="ts">

import {defineComponent} from "vue";
import {InteractiveMap} from "stores/map-store";
import MapSidebarLinkGroup from "components/MapSidebarLinkGroup.vue";

export default defineComponent({
  name: 'MapSidebar',
  components: {
    MapSidebarLinkGroup
  },
  props: {
    maps: {
      type: Array<InteractiveMap>,
      required: true
    }
  },
  computed: {
    games() {
      const all_games = this.maps.map(i => i.game);
      return [...new Set(all_games)]
    }
  },
  methods: {
    maps_for_game(game_name: string) {
      return this.maps.filter(i => i.game == game_name)
    }
  }
})
</script>
