import {api} from "boot/axios";
import {Store, StoreDefinition} from "pinia";
import {RemovableRef, useStorage} from '@vueuse/core'
import {ref} from "vue";

export class APIClient {
  mapStore: StoreDefinition<"interactive-maps">
  userInfo: object
  apiToken: RemovableRef<any>

  constructor(map_store: StoreDefinition<"interactive-maps">) {
    this.mapStore = map_store
    this.userInfo = ref({})
    this.apiToken = useStorage('api_token', '')
    if (this.apiToken.value != '') {
      api.defaults.headers.common.Authorization = `Bearer ${this.apiToken.value}`;
      this.getUserInfo()
    }
  }

  getToken(code: string) {
    if (this.apiToken.value == '') {
      api.get("/token", {params: {code: code}})
        .then((response) => {
          api.defaults.headers.common.Authorization = `Bearer ${response.data['token']}`;
          const api_token = useStorage('api_token');
          api_token.value = response.data['token'];
          this.getUserInfo()
        })
    }
  }

  loadAllMaps() {
    this.mapStore.loading = true
    api.get("/maps")
      .then((response) => {
        this.mapStore.loadMaps(response.data)
        this.mapStore.loading = false
      })
  }

  loadMapLayers(map_id: number) {
    this.mapStore.loading = true
    api.get(`/maps/${map_id}`)
      .then((response) => {
        this.mapStore.loadMapLayers(map_id, response.data.layers)

        for (const layerIndex in response.data.layers) {
          this.loadMapLayerPoints(map_id, response.data.layers[layerIndex].id)
        }
        this.mapStore.loading = false
      })
  }

  loadMapLayerPoints(map_id: number, layer_id: number) {
    api.get(`/maps/${map_id}/layers/${layer_id}`)
      .then((response) => {
        this.mapStore.loadMapLayerPoints(map_id, layer_id, response.data.points)
      })
  }

  getUserInfo() {
    api.get('/me').then((response) => {
      this.userInfo.value = response.data
    })
  }

  async createMap(map_name: string, game_name: string, description: string, map_url: string, x_dim: number, y_dim: number) {
    const create_body = {
      name: map_name,
      game: game_name,
      description: description,
      image: map_url,
      x_dimension: x_dim,
      y_dimension: y_dim
    }

    api.post('/maps', create_body).then((response) => {
      this.mapStore.addMap(response.data)
      return true
    })
  }
}
