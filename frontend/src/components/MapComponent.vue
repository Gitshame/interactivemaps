<template>
  <div style="height: 100%">
    <div v-if=!mapsStore.loading>
      <l-map
        v-model:zoom="zoom" ref="map" :zoom=1 :center="[500,500]" :crs=crs
        style="height: 100pc; width: 100pc;">
        <l-image-overlay
          :url=mapsStore.getMap(mapId).image
          :bounds=mapsStore.getMapBounds(mapId)
        >
        </l-image-overlay>
        <l-marker
          :lat-lng=marker
        ><l-popup>Test</l-popup></l-marker>
      </l-map>
    </div>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  computed,
  ref,
  toRef,
  Ref,
} from 'vue';

import "leaflet/dist/leaflet.css";
import {LImageOverlay, LMap, LMarker, LPopup, LTileLayer} from "@vue-leaflet/vue-leaflet";

import { Todo, Meta } from './models';
import { api } from 'boot/axios';
import { useInteractiveMapStore } from 'stores/map-store'
import { CRS } from 'leaflet'

export default defineComponent({
  name: 'MapComponent',
  components: {LPopup, LMarker, LImageOverlay, LMap},
  props: {
    map_id: Number
  },
  setup (props) {
    console.log(props);
    const mapsStore = useInteractiveMapStore()
    const mapId = ref(props.map_id)
    api.get("/maps")
      .then((response) => {
        mapsStore.loadMaps(response.data)
        mapsStore.loading = false
      })

    const crs = CRS.Simple
    const marker = {
      lat: 500,
      lng: 500
    }

    const zoom = 1
    return { mapsStore, mapId, crs, marker, zoom};
  },
});
</script>
