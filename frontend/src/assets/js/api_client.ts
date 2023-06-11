import {api} from "boot/axios";
import {Store} from "pinia";
import {useStorage} from '@vueuse/core'

export class APIClient {
  mapStore: Store

  constructor(map_store: Store) {
    this.mapStore = map_store
    const api_token = useStorage('api_token', '')
    if (api_token.value != '') {
      api.defaults.headers.common.Authorization = `Bearer ${api_token.value}`;
    }
  }

  getToken(code: string) {
    api.get("/token", {params: {code: code}})
      .then((response) => {
        api.defaults.headers.common.Authorization = `Bearer ${response.data['token']}`;
        const api_token = useStorage('api_token');
        api_token.value = response.data['token'];
      })
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
