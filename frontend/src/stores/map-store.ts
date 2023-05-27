import { defineStore } from 'pinia';
import type L from "leaflet";
import { computed, ref } from "vue";

export const useInteractiveMapStore = defineStore('interactive-maps', {
  state: () => ({
    maps: []
  }),
  getters: {
    doubleCount: (state) => state.counter * 2,
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
            [map.x_dimension, map.y_dimension],
          ] as L.LatLngBoundsLiteral
      );

      return bounds;
    }
  },
});
