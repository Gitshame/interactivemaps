<template>
  <div>
    <q-card v-if=!mapsStore.loading class="items-stretch">
      <l-map
        v-model:zoom="zoom" ref="map" :min-zoom=-2 :zoom=1 :center="this.centerInput" :crs=crs
        style="height: 50pc;"
        @ready="mapOnReadyHandler">
        <l-image-overlay
          :url=mapsStore.getMap(mapId).image
          :bounds=mapsStore.getMapBounds(mapId)
        >
          <l-image-overlay
            v-for="layer in mapsStore.getMapLayers(mapId)"
            v-bind:key="layer.id"
            :url="layer.image || mapsStore.getMap(mapId).image"
            :bounds=mapsStore.getMapBounds(mapId)>
            <l-marker
              v-for="map_marker in mapsStore.getMapLayerPoints(mapId, layer.id)"
              v-bind:key="map_marker.id"
              :lat-lng="[map_marker.y_position, map_marker.x_position]">
              <l-popup>{{ map_marker.name }}</l-popup>
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
      <CreateNewPointCard
        :visible="createNewPointDialogVisible"
        :layers="mapsStore.getMapLayers(mapId)"
        :map_id="mapId"
        :api_client="backendClient"
        @close="createNewPointDialogVisible=false"
        :x_position="newPointXPosition"
        :y_position="newPointYPosition"
      />
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

import {Todo, Meta} from './models';
import {api} from 'boot/axios';
import {useInteractiveMapStore} from 'stores/map-store'
import {CRS} from 'leaflet'
import {APIClient} from 'assets/js/api_client'
import CreateNewPointCard from "components/CreateNewPointCard.vue";



export default defineComponent({
  name: 'MapDisplay',
  components: {CreateNewPointCard, LPopup, LMarker, LImageOverlay, LMap},
  props: {
    map_id: Number,
    centerInput: Array,
    backendClient: APIClient
  },
  setup(props) {
    console.log(props);
    const mapsStore = useInteractiveMapStore()
    const mapId = ref(props.map_id)
    const createNewPointDialogVisible = ref(false)
    const newPointXPosition = ref(0)
    const newPointYPosition = ref(0)
    const mapOnReadyHandler = (map) => {
      map.on('click', mapClickHandler)
    }
    const mapClickHandler = (event) => {
      createNewPointDialogVisible.value = true
      newPointXPosition.value = event.latlng.lng
      newPointYPosition.value = event.latlng.lat
    }

    const crs = CRS.Simple

    const zoom = 1
    return {mapsStore, mapId, crs, zoom, mapOnReadyHandler, createNewPointDialogVisible, mapClickHandler, newPointXPosition, newPointYPosition};
  },
});
</script>
