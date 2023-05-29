import {api} from "boot/axios";
import {Store} from "pinia";

export class APIClient {
  mapStore: Store

  constructor(map_store: Store) {
    this.mapStore = map_store
  }

  loadAllMaps() {
    api.get("/maps")
      .then((response) => {
          this.mapStore.loadMaps(response.data)
          this.mapStore.loading = false
      })
  }

  loadMapLayers(map_id: number) {
    api.get(`/maps/${map_id}`)
      .then((response) => {
        this.mapStore.loadMapLayers(map_id, response.data.layers)
        this.mapStore.loading = false

        for (const layerIndex in response.data.layers) {
          this.loadMapLayerPoints(map_id, response.data.layers[layerIndex].id)
        }
      })
  }
  loadMapLayerPoints(map_id: number, layer_id: number) {
    api.get(`/maps/${map_id}/layers/${layer_id}`)
      .then((response) => {
        this.mapStore.loadMapLayerPoints(map_id, layer_id, response.data.points)
        this.mapStore.loading = false
      })
  }
}
