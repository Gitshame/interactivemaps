import {defineStore,} from 'pinia';
import type L from "leaflet";
import {computed} from "vue";

interface InteractiveMap {
  id: number
  layers: object
  x_dimension: number
  y_dimension: number
}

interface InteractiveMapLayer {
  points: object
}

export const useInteractiveMapStore = defineStore('interactive-maps', {
  state: () => ({
    maps: [],
    loading: false
  }),
  getters: {
  },
  actions: {
    loadMaps(mapsList: []) {
      this.maps = mapsList;
    },
    loadMapLayers(mapId: number, layers: []) {
      const currentMap = this.getMap(mapId)
      if (currentMap != undefined) {
        if (currentMap.layers == undefined){
          currentMap.layers = {}
        }
        layers.forEach((layer) => {
          const layer_id: string = layer['id'].toString()
          currentMap.layers[layer_id] = layer
        })
      }
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
        return mapData['layers'][layerId]
      }
    },
    loadMapLayerPoints(mapId: number, layerId: number, points: []) {
      const currentMapLayer = this.getMapLayer(mapId, layerId)

      if (currentMapLayer != undefined) {
        if (currentMapLayer.points == undefined){
          currentMapLayer.points = {}
        }
        points.forEach((point) => {
          const layer_id: string = point['id'].toString()
          currentMapLayer.points[layer_id] = point
        })
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
    },
    getMapLayers(mapId: number): Array<InteractiveMapLayer> {
      const currentMap = this.getMap(mapId)
      if (currentMap == undefined || currentMap.layers == undefined) {
        return []
      }
      return Object.values(currentMap.layers)
    },
    getMapLayerPoints(mapId: number, layerId: number) {
      const layer = this.getMapLayer(mapId, layerId)
      if (layer == undefined || layer.points == undefined) {
        return []
      }
      return Object.values(layer.points)
    }
  },
});
