import { defineStore } from 'pinia';
import type L from "leaflet";
import { computed, ref } from "vue";

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
    getMap(mapId: number) {
      return this.maps.find((map) => map.id === mapId);
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

      console.log(bounds.value)

      return bounds.value;
    }
  },
});
