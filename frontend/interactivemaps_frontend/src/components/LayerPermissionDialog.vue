<template>
  <div>
    <q-dialog v-model="isVisible" :maximized=true>
      <q-card style="min-width: 350px">
        <q-btn dense flat icon="close" @click="$emit('close')" class="float-right">
          <q-tooltip class="bg-white text-primary">Close</q-tooltip>
        </q-btn>
        <div class="text-h5">Layer Permissions</div>
        <q-card-section>
          <div class="text-h6">User Permissions</div>
          <q-table
            :rows="permissions.user_permissions"
            row-key="id">
            <template v-slot:body="props">
                <q-tr :props="props">
                  <q-td key="user_id" :props="props">
                    {{this.users.get(props.row.user_id)}}
                  </q-td>
                  <q-td key="read" :props="props">
                    <q-checkbox v-model="props.row['read']" />
                  </q-td>
                  <q-td key="create" :props="props">
                    <q-checkbox v-model="props.row['create']" />
                  </q-td>
                  <q-td key="modify" :props="props">
                    <q-checkbox v-model="props.row['modify']" />
                  </q-td>
                  <q-td key="delete" :props="props">
                    <q-checkbox v-model="props.row['delete']" />
                  </q-td>
              </q-tr>
            </template>
          </q-table>
          <q-select
            :options="validUsers"
            option-label="1"
            option-value="0"
            v-model="newUser"
          />
          <q-btn icon="person_add" label="Add User" @click="handleAddNewUser" />
        </q-card-section>
        <q-card-section>
          <div class="text-h6">Group Permissions</div>
          <q-table
            :rows="permissions.group_permissions"
            row-key="id">
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="group_id" :props="props">
                  {{ this.groups.get(props.row.group_id) }}
                </q-td>
                <q-td key="read" :props="props">
                  <q-checkbox v-model="props.row['read']" />
                </q-td>
                <q-td key="create" :props="props">
                  <q-checkbox v-model="props.row['create']" />
                </q-td>
                <q-td key="modify" :props="props">
                  <q-checkbox v-model="props.row['modify']" />
                </q-td>
                <q-td key="delete" :props="props">
                  <q-checkbox v-model="props.row['delete']" />
                </q-td>
              </q-tr>
            </template>
          </q-table>
          <q-select
            :options="validGroups"
            option-label="1"
            option-value="0"
            v-model="newGroup"
          />
          <q-btn icon="group_add" label="Add Group" @click="handleAddNewGroup" />
        </q-card-section>
        <q-card-actions>
          <q-btn label="Cancel" @click="$emit('close')"/>
          <q-btn label="Save" @click="handleUpdatePermissions(map_id, layer_id, permissions)" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import {
  computed,
  defineComponent, ref,
} from 'vue';
import {useInteractiveMapStore} from "stores/map-store";
import {APIClient, LayerPermissions} from "assets/js/api_client";
import {valid} from "semver";
import {map, Util} from "leaflet";
import emptyImageUrl = Util.emptyImageUrl;

export default defineComponent({
  name: 'LayerPermissionDialog',
  methods: {
    emptyImageUrl() {
      return emptyImageUrl
    },
    valid,
    handleAddNewUser() {
      this.permissions.user_permissions.push({'user_id': this.newUser[0], 'read': false, 'create': false, 'delete': false, 'modify': false})
      this.newUser = null
    },
    handleAddNewGroup() {
      this.permissions.group_permissions.push({'group_id': this.newGroup[0], 'read': false, 'create': false, 'delete': false, 'modify': false})
      this.newGroup = null
    }
  },
  props: {
    map_id: {
      type: Number,
      required: true
    },
    layer_id: {
      type: Number,
      required: true
    },
    visible: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    Util() {
      return Util
    },
    isVisible(): boolean {
      return this.visible
    },
    validUsers() {
      const allUsers = this.users.entries()
      let validUsers = []
      for (const user of allUsers) {
        const matchingUsers = this.permissions['user_permissions'].some((permission) => {
          return permission['user_id'] == user[0]
        })
        if (!matchingUsers) {validUsers.push(user)}
      }
      return validUsers
    },
    validGroups() {
      const allGroups = this.groups.entries()
      let validGroups = []
      for (const group of allGroups) {
        const matchingGroups = this.permissions['group_permissions'].some((permission) => {
          return permission['group_id'] == group[0]
        })
        if (!matchingGroups) {validGroups.push(group)}
      }
      return validGroups
    }
  },
  data() {
    return {
      permissions: {} as LayerPermissions,
      users: new Map<number, string>(),
      groups: new Map<number, string>(),
      newUser: null,
      newGroup: null
    }
  },
  setup () {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)

    const handleUpdatePermissions = (map_id: number, layer_id: number, permissions: LayerPermissions) => {
      backendClient.updateLayerPermissions(map_id, layer_id, permissions).then()
    }

    return { backendClient, handleUpdatePermissions }
  },
  created() {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)

    backendClient.loadMapLayerPermissions(this.map_id, this.layer_id).then((response) => {
      this.permissions = response.data
    })

    backendClient.getAllUsers().then((response) => {
      response.data['users'].forEach((user) => {
        this.users.set(user.id, user.display_name)
      })
    })

    backendClient.getAllGroups().then((response) => {
      response.data['groups'].forEach((group) => {
        this.groups.set(group.id, `${group.server_name} - ${group.display_name}`)
      })
    })
  }
});
</script>
