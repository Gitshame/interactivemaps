import {_GettersTree, defineStore,} from 'pinia';
import type L from "leaflet";
import {computed} from "vue";

export interface InteractiveMap {
  id: number
  game: string
  layers: Map<string, InteractiveMapLayer>
  x_dimension: number
  y_dimension: number
  image: string
}

export interface InteractiveMapLayer {
  name: string
  id: number
  points: Map<string, InteractiveMapPoint>
  image: string
  permissions: LayerPermissions
}

export interface InteractiveMapPoint {
  id: number
  name: string
  x_position: number
  y_position: number
}

export interface MapStoreState {
  maps: Array<InteractiveMap>
  loading: boolean
}

export interface LayerPermissions {
  read: boolean
  create: boolean
  delete: boolean
  modify: boolean
}

export interface MapStoreActions extends MapStoreState{
  loadMaps: (mapsList: Array<InteractiveMap>) => void
  loadMapLayers: (mapId: number, layers: Array<InteractiveMapLayer>) => void
  addMap: (map: InteractiveMap) => void
  getMap: (mapId: number) => InteractiveMap | undefined
  getMapLayer: (mapId: number, layerId: number) => InteractiveMapLayer | undefined
  loadMapLayerPoints: (mapId: number, layerId: number, points: Array<InteractiveMapPoint>) => void
  getMapBounds: (mapId: number) => L.LatLngBoundsLiteral
  getMapLayers: (mapId: number) => Array<InteractiveMapLayer>
  getMapLayerPoints: (mapId: number, layerId: number) => Array<InteractiveMapPoint>
  setLoading: (loading: boolean) => void
  removePoint: (map_id: number, layer_id: number, point_id: number) => void
  removeLayer: (map_id: number, layer_id: number) => void
}

export const useInteractiveMapStore = defineStore('interactive-maps', {
  state: (): MapStoreState => ({
    maps: [],
    loading: false
  }),
  getters: <_GettersTree<MapStoreState>> {
  },
  actions: <MapStoreActions> {
    loadMaps(mapsList: Array<InteractiveMap>) {
      this.maps = mapsList;
    },
    loadMapLayers(mapId: number, layers: Array<InteractiveMapLayer>) {
      const currentMap = this.getMap(mapId)
      if (currentMap != undefined) {
        if (currentMap.layers == undefined){
          currentMap.layers = new Map()
        }
        layers.forEach((layer) => {
          const layer_id: string = layer.id.toString()
          currentMap.layers.set(layer_id, layer)
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
    getMapLayer(mapId: number, layerId: number): InteractiveMapLayer | undefined {
      const mapData = this.getMap(mapId)
      if (mapData === undefined) {
        return undefined
      } else {
        return mapData.layers.get(layerId.toString())
      }
    },
    loadMapLayerPoints(mapId: number, layerId: number, points: Array<InteractiveMapPoint>) {
      const currentMapLayer = this.getMapLayer(mapId, layerId)

      if (currentMapLayer != undefined) {
        if (currentMapLayer.points == undefined){
          currentMapLayer.points = new Map()
        }
        points.forEach((point: InteractiveMapPoint) => {
          const layer_id: string = point.id.toString()
          currentMapLayer.points.set(layer_id, point)
        })
      }
    },
    getMapBounds(mapId: number) {
      const map = this.getMap(mapId);
      if (map != undefined) {
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
    getMapLayers(mapId: number): Array<InteractiveMapLayer> {
      const currentMap = this.getMap(mapId)
      if (currentMap == undefined || currentMap.layers == undefined) {
        return []
      }
      return Array.from(currentMap.layers.values())
    },
    getMapLayerPoints(mapId: number, layerId: number) {
      const layer = this.getMapLayer(mapId, layerId)
      if (layer == undefined || layer.points == undefined) {
        return []
      }
      return Array.from(layer.points.values())
    },
    setLoading(loading: boolean) {
      this.loading = loading
    },
    removePoint(map_id: number, layer_id: number, point_id: number) {
      const layer = this.getMapLayer(map_id, layer_id)
      if (layer != undefined) {
        layer.points.delete(point_id.toString())
      }
    },
    removeLayer(map_id: number, layer_id: number) {
      const map = this.getMap(map_id)
      if (map != undefined) {
        map.layers.delete(layer_id.toString())
      }
    }
  },
});
