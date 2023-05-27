import { defineStore } from 'pinia';

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
  },
});
