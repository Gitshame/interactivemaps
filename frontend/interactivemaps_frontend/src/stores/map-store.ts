import {defineStore,} from 'pinia';
import type L from "leaflet";
import {computed} from "vue";

interface InteractiveMap {
  id: number
  layers: Array<InteractiveMapLayer>
  x_dimension: number
  y_dimension: number
}

interface InteractiveMapLayer {
  points: Array<object>
}

export const useInteractiveMapStore = defineStore('interactive-maps', {
  state: () => ({
    maps: [],
    loading: false
  }),
  getters: {},
  actions: {
    loadMaps(mapsList: []) {
      this.maps = mapsList;
    },
    loadMapLayers(mapId: number, layers: []) {
      const currentMap = this.getMap(mapId)
      currentMap['layers'] = layers
    },
    addMap(map: InteractiveMap) {
      this.maps.push(map)
    },
    getMap(mapId: number): InteractiveMap | undefined {
      return this.maps.find((map) => {
        return (map.id === mapId);
      });
    },
    getMapLayer(mapId: number, layerId: number): InteractiveMapLayer | null {
      const mapData = this.getMap(mapId)
      if (mapData === undefined) {
        return null
      } else {
        console.log(mapData)
        const return_layer = mapData['layers'].find(function (layer) {
          return layer.id === layerId
        })
        if (return_layer === undefined) {
          return null
        }
        return return_layer
      }
    },
    loadMapLayerPoints(mapId: number, layerId: number, points: []) {
      const currentMapLayer = this.getMapLayer(mapId, layerId)
      if (currentMapLayer != null) {
        currentMapLayer["points"] = points
      }
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
