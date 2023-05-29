<template>
  <div>
    <q-card v-if=!mapsStore.loading class="items-stretch">
      <l-map
        v-model:zoom="zoom" ref="map" :zoom=1 :center="this.centerInput" :crs=crs
        style="height: 50pc;" @ready="mapClickHandler">
        <l-image-overlay
          :url=mapsStore.getMap(mapId).image
          :bounds=mapsStore.getMapBounds(mapId)
        >
          <l-image-overlay
            v-for="layer in mapsStore.getMap(mapId).layers"
            v-bind:key="layer.id"
            :url="layer.image || mapsStore.getMap(mapId).image"
            :bounds=mapsStore.getMapBounds(mapId)>
              <l-marker
                v-for="map_marker in layer.points"
                v-bind:key="map_marker.id"
                :lat-lng="[map_marker.y_position, map_marker.x_position]">
                <l-popup>{{map_marker.name}}</l-popup>
              </l-marker>
          </l-image-overlay>
        </l-image-overlay>
<!--        <l-marker-->
<!--          v-for="map_marker in mapsStore.getMap(mapId).layers[0].points"-->
<!--          v-bind:key="map_marker.id"-->
<!--          :lat-lng="[map_marker.y_position, map_marker.x_position]">-->
<!--          <l-popup>{{map_marker.name}}</l-popup>-->
<!--        </l-marker>-->
      </l-map>
    </q-card>
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
import {APIClient} from 'assets/js/api_client'

const mapClickHandler = map => {
  map.on('click', console.log)
}

export default defineComponent({
  name: 'MapDisplay',
  components: {LPopup, LMarker, LImageOverlay, LMap},
  props: {
    map_id: Number,
    centerInput: Array
  },
  setup (props) {
    console.log(props);
    const mapsStore = useInteractiveMapStore()
    const mapId = ref(props.map_id)
    const test_client = new APIClient(mapsStore)

    test_client.loadAllMaps()
    test_client.loadMapLayers(mapId.value)

    const crs = CRS.Simple

    const zoom = 1
    return { mapsStore, mapId, crs, zoom, mapClickHandler };
  },
});
</script>
