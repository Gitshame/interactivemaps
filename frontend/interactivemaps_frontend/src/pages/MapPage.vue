<template>
    <q-page class="row items-center" v-if="!mapsStore.loading">
      <map-display class="col-10" :map_id=mapId :centerInput="mapCenter" :backendClient="backendClient"/>
      <layer-list-card
        class="col-2"
        :layers="mapsStore.getMapLayers(mapId)"
        :map_id="mapId"
        style="height: 50pc"
        :focusMapHandler="focusMapHandler"
        @createNewLayer="createNewLayerDialogVisible=true"

      />
    </q-page>
  <CreateNewLayerDialog :map_id="mapId"
                        :api_client="backendClient"
                        @close="createNewLayerDialogVisible=false"
                        :visible="createNewLayerDialogVisible" />
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import MapDisplay from "components/MapDisplay.vue";
import {useRoute} from "vue-router";
import LayerListCard from "components/LayerListCard.vue";
import {useInteractiveMapStore} from "stores/map-store";
import {APIClient} from "assets/js/api_client";
import CreateNewLayerDialog from "components/CreateNewLayerDialog.vue";


export default defineComponent({
  name: 'MapPage',
  components: {CreateNewLayerDialog, LayerListCard, MapDisplay},
  props: {
  },
  setup () {
    const route = useRoute();
    const mapId = parseInt(route.params.map_id, 10)
    const createNewLayerDialogVisible = ref(false)

    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)

    const mapBounds = computed(() => mapsStore.getMapBounds(mapId))

    const mapCenter = computed(() => {
      const mapBoundsData = mapBounds.value
      const mapSize = [mapBoundsData[1][0] - mapBoundsData[0][0],
                        mapBoundsData[1][1] - mapBoundsData[0][1]]
      const mapCenterOffset = [mapSize[0] / 2, mapSize[1] / 2]
      return [mapBoundsData[0][0] + mapCenterOffset[0], mapBoundsData[0][1] + mapCenterOffset[1]]
    })

    const focusMapHandler = (center: number[]) => {
      mapCenter.value = [center[1], center[0]]
    }

    backendClient.loadMapLayers(mapId)

    return { mapId, mapsStore, mapCenter, focusMapHandler, backendClient, createNewLayerDialogVisible }
  }
});
</script>
