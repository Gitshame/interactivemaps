<template>
  <div>
    <q-dialog v-model="isVisible">
      <q-card>
        <q-card-section>
          <div class="text-h6" style="min-width: 350px">
            Create A New Map
          </div>
        </q-card-section>
        <q-card-section>
          <q-input standout label="Map Name" v-model="map_name"/>
          <q-input standout label="Game Name" v-model="game_name"/>
          <q-input standout label="Description" v-model="description"/>
          <q-input standout label="Map Image URL" v-model="map_url"/>
          <q-input standout label="X Dimension" type="number" v-model="x_dim"/>
          <q-input standout label="Y Dimension" type="number" v-model="y_dim"/>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn @click="handleCancel" label="Cancel"/>
          <q-btn @click="handleCreate" color="primary" label="Create"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  computed,
  ref,
  toRef,
  Ref,
} from 'vue';
import {Todo, Meta} from './models';
import {api} from 'boot/axios';
import {useInteractiveMapStore} from 'stores/map-store'

export default defineComponent({
  name: 'CreateNewMapDialog',
  props: {
    visible: {
      type: Boolean
    },
    api_client: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      map_name: '',
      game_name: '',
      description: '',
      map_url: '',
      x_dim: 0,
      y_dim: 0
    }
  },
  computed: {
    isVisible() {
      return this.visible
    }
  },
  methods: {
    handleCancel() {
      this.map_name = ''
      this.game_name = ''
      this.description = ''
      this.map_url = ''
      this.x_dim = 0
      this.y_dim = 0

      this.$emit('close')
    },
    async handleCreate() {
      await this.api_client.createMap(this.map_name, this.game_name, this.description, this.map_url, this.x_dim, this.y_dim)
      this.handleCancel()
    }
  }
});
</script>
