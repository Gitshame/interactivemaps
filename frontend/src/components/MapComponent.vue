<template>
  <div>
    <l-map ref="map" :v-model:zoom="zoom" :center="[0,0]" crs=L.CRS.Simple>
      <l-image-overlay url=mapsStore.getMap(props.map_id).image bounds=mapsStore.getMapBounds(props.map_id)></l-image-overlay>
    </l-map>
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
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

import { Todo, Meta } from './models';
import { api } from 'boot/axios';
import { useInteractiveMapStore } from 'stores/map-store'

export default defineComponent({
  name: 'MapComponent',
  props: {
    map_id: Number
  },
  setup (props) {
    const mapsStore = useInteractiveMapStore()
    api.get("/maps")
      .then((response) => {
        mapsStore.loadMaps(response.data)
      })
    return { mapsStore, props };
  },
});
</script>
