<template>
  <div>
    <q-card v-if="!mapsStore.loading && map != undefined" class="items-stretch">
      <l-map
        v-model:zoom="zoom" ref="map" :min-zoom=-2 :zoom=1 :center="this.centerInput" :crs=crs
        style="height: 50pc;"
        @ready="mapOnReadyHandler">
        <l-image-overlay
          :url="map.image"
          :bounds=mapBounds
        >
          <l-image-overlay
            v-for="layer in mapLayers"
            v-bind:key="layer.id"
            :url="layer.image || map.image"
            :bounds=mapBounds>
            <l-marker
              v-for="map_marker in mapsStore.getMapLayerPoints(map_id, layer.id)"
              v-bind:key="map_marker.id"
              :lat-lng="[map_marker.y_position, map_marker.x_position]">
              <l-popup :options="{minWidth: 350}">
                <MapPointCard
                  :point="map_marker"
                  :layer_id="layer.id"
                  :map_id="map_id"
                  :apiClient="apiClient"
                  :canDelete="layer.permissions.delete"/>
              </l-popup>
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
        :layers="validLayers"
        :map_id="map_id"
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
import MapPointCard from "components/MapPointCard.vue";



export default defineComponent({
  name: 'MapDisplay',
  components: {
    MapPointCard,
    CreateNewPointCard, LPopup, LMarker, LImageOverlay, LMap},
  props: {
    map_id: {
      type: Number,
      required: true
    },
    centerInput: Array,
    backendClient: APIClient
  },
  setup(props) {
    const mapsStore = useInteractiveMapStore()
    const apiClient = new APIClient(mapsStore)
    const createNewPointDialogVisible = ref(false)
    const newPointXPosition = ref(0)
    const newPointYPosition = ref(0)
    const mapOnReadyHandler = (map: typeof LMap) => {
      map.on('click', mapClickHandler)
    }
    const mapClickHandler = (event: { latlng: { lng: number; lat: number; }; }) => {
      createNewPointDialogVisible.value = true
      newPointXPosition.value = event.latlng.lng
      newPointYPosition.value = event.latlng.lat
    }

    const crs = CRS.Simple

    const zoom = 1

    const map = computed(() => mapsStore.getMap(props.map_id))
    const mapLayers = computed(() => mapsStore.getMapLayers(props.map_id))
    const mapBounds = computed(() => mapsStore.getMapBounds(props.map_id))

    const validLayers = computed(() => mapsStore.getMapLayers(props.map_id).filter((layer) => layer.permissions.create))

    return {mapsStore,
      crs,
      zoom,
      mapOnReadyHandler,
      createNewPointDialogVisible,
      mapClickHandler,
      newPointXPosition,
      newPointYPosition,
      map,
      mapLayers,
      mapBounds,
      apiClient,
      validLayers};
  },
});
</script>
