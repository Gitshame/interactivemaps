<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Interactive Maps
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Essential Links
        </q-item-label>

        <MapSidebarLink
          v-for="map in mapsStore.maps"
          :key="map.name"
          v-bind="map"
          :caption="map.caption"
          :title="map.name"
          :link="`/maps/${map.id}`"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import MapSidebarLink from 'components/MapSidebarLink.vue';
import { useInteractiveMapStore } from 'stores/map-store'
import {APIClient} from 'assets/js/api_client'


export default defineComponent({
  name: 'MapLayout',

  components: {
    MapSidebarLink
  },

  setup () {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)
    backendClient.loadAllMaps()

    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      mapsStore
    }
  }
});
</script>
