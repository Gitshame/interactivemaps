import { defineStore } from 'pinia';
import type L from "leaflet";
import { computed, ref } from "vue";
import {map} from "leaflet";

export const useInteractiveMapStore = defineStore('interactive-maps', {
  state: () => ({
    maps: [],
    loading: true
  }),
  getters: {
  },
  actions: {
    loadMaps(mapsList: []) {
      this.maps = mapsList;
    },
    loadMapLayers(mapId: number, layers: []) {
      const currentMap = this.getMap(mapId)
      currentMap['layers'] = layers
    },
    getMap(mapId: number) {
      return this.maps.find((map) => map.id === mapId);
    },
    getMapLayer(mapId: number, layerId: number) {
      const mapData = this.getMap(mapId)
      if (mapData === undefined) {
        return {}
      }
      else {
        return mapData['layers'].find((layer) => layer.id === layerId);
      }
    },
    loadMapLayerPoints(mapId: number, layerId: number, points: []) {
      const currentMapLayer = this.getMapLayer(mapId, layerId)
      currentMapLayer['points'] = points
    },
    getMapBounds(mapId: number) {
      const map = this.getMap(mapId);
      const bounds = computed(
        () =>
          [
            [0, 0],
            [map.y_dimension, map.x_dimension],
          ] as L.LatLngBoundsLiteral
      );
      return bounds.value;
    }
  },
});
