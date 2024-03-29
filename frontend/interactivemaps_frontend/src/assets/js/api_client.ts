import {api} from "boot/axios";
import {_GettersTree, Store} from "pinia";
import {MapStoreState, MapStoreActions} from "stores/map-store"
import {RemovableRef, useStorage} from '@vueuse/core'
import {Ref, ref} from "vue";
import {map} from "leaflet";

export interface LayerPermissions {
  user_permissions: Array<UserPermissionEntry>
  group_permissions: Array<GroupPermissionEntry>
}

interface UserPermissionEntry {
  user_id: number
  read: boolean
  create: boolean
  modify: boolean
  delete: boolean
}

interface GroupPermissionEntry {
  group_id: number
  read: boolean
  create: boolean
  modify: boolean
  delete: boolean
}

export interface UserInfo {
  discord_id: number | null
  display_name: string | null
  is_admin: boolean
}

export class APIClient {
  mapStore: Store<"interactive-maps", MapStoreState, _GettersTree<MapStoreState>, MapStoreActions>
  userInfo: Ref<UserInfo>
  apiToken: RemovableRef<any>

  constructor(map_store: Store<"interactive-maps", MapStoreState, _GettersTree<MapStoreState>, MapStoreActions>) {
    this.mapStore = map_store
    this.userInfo = ref({'discord_id': null, 'display_name': null, 'is_admin': false})
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
          const api_token = useStorage('api_token', null);
          api_token.value = response.data['token'];
          this.getUserInfo()
        })
    }
  }

  loadAllMaps() {
    this.mapStore.setLoading(true)
    api.get("/maps")
      .then((response) => {
        this.mapStore.loadMaps(response.data)
        this.mapStore.setLoading(false)
      })
  }

  loadMapLayers(map_id: number) {
    this.mapStore.setLoading(true)
    api.get(`/maps/${map_id}`)
      .then((response) => {
        this.mapStore.loadMapLayers(map_id, response.data.layers)

        for (const layerIndex in response.data.layers) {
          this.loadMapLayerPoints(map_id, response.data.layers[layerIndex].id)
        }
        this.mapStore.setLoading(false)
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
      this.userInfo = response.data
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

  async createLayer(map_id: number, layer_name: string, description: string, map_url: string, priority: number, isPublic: boolean) {
    const create_body = {
      name: layer_name,
      description: description,
      image: map_url,
      priority: priority,
      public: isPublic
    }

    api.post(`/maps/${map_id}/layers`, create_body).then((response) => {
      this.mapStore.loadMapLayers(map_id, [response.data])
      return true
    })
  }

  async updateLayer(map_id: number, layer_id: number, layer_name: string, description: string, map_url: string, priority: number, isPublic: boolean) {
    const updateBody = {
      name: layer_name,
      description: description,
      image: map_url,
      priority: priority,
      public: isPublic
    }

    api.patch(`/maps/${map_id}/layers/${layer_id}`, updateBody).then((response) => {
      this.mapStore.updateLayer(map_id, layer_id, response.data)
      return true
    })
  }

  async createPoint(map_id: number, layer_id: number, point_name: string, x_position: number, y_position: number) {
    const create_body = {
      name: point_name,
      x_position: x_position,
      y_position: y_position
    }
    api.post(`/maps/${map_id}/layers/${layer_id}/points`, create_body).then((response) => {
      this.mapStore.loadMapLayerPoints(map_id, layer_id, [response.data])
      return true
    })

  }

  async updatePoint(map_id: number, layer_id: number, point_id: number, point_name: string, x_coord: number, y_coord: number) {
    const updateBody = {
      name: point_name,
      x_position: x_coord,
      y_position: y_coord
    }

    api.patch(`/maps/${map_id}/layers/${layer_id}/points/${point_id}`, updateBody).then((response) => {
      this.mapStore.loadMapLayerPoints(map_id, layer_id, [response.data])
      return true
    })
  }

  async deletePoint(map_id: number, layer_id: number, point_id: number) {
    api.delete(`/maps/${map_id}/layers/${layer_id}/points/${point_id}`).then(() => {
      this.mapStore.removePoint(map_id, layer_id, point_id)
      return true
    })
  }

  async deleteLayer(map_id: number, layer_id: number) {
    api.delete(`/maps/${map_id}/layers/${layer_id}`).then(() => {
      this.mapStore.removeLayer(map_id, layer_id)
      return true
    })
  }
  async loadMapLayerPermissions(map_id: number, layer_id: number) {
    return api.get(`/maps/${map_id}/layers/${layer_id}/permissions`)
  }

  async getAllUsers() {
    return api.get("/users")
  }

  async getAllGroups() {
    return api.get("/groups")
  }

  async updateLayerPermissions(map_id: number, layer_id: number, new_permissions: LayerPermissions) {
    return api.post(`/maps/${map_id}/layers/${layer_id}/permissions`, new_permissions)
  }
}
