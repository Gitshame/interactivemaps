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

        <div>
          <ClickToLoginDiscord/>
        </div>
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
      <q-btn rounded
             color="primary"
             class="full-width"
             label="Create New Map"
             v-if="this.isAdmin"
             @click="createNewMapDialogOpen=true"
      />
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>
    <CreateNewMapDialog :visible="createNewMapDialogOpen"
                        :api_client="backendClient"
                        @close="createNewMapDialogOpen=false"/>
  </q-layout>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import MapSidebarLink from 'components/MapSidebarLink.vue';
import {useInteractiveMapStore} from 'stores/map-store'
import {APIClient} from 'assets/js/api_client'
import ClickToLoginDiscord from "components/ClickToLoginDiscord.vue";
import CreateNewMapDialog from "components/CreateNewMapDialog.vue";


export default defineComponent({
  name: 'MapLayout',

  components: {
    CreateNewMapDialog,
    ClickToLoginDiscord,
    MapSidebarLink
  },

  setup() {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)
    backendClient.loadAllMaps()

    const isAdmin = ref(backendClient.userInfo)

    const leftDrawerOpen = ref(false)
    const createNewMapDialogOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      mapsStore,
      createNewMapDialogOpen,
      backendClient,
      isAdmin
    }
  },
  // computed: {
  //   isAdmin() {
  //     console.log(this.backendClient.userInfo.value)
  //     return this.backendClient.userInfo.is_admin
  //   }
  // }
});
</script>
