<template>
  <div>
    <q-dialog v-model="isVisible">
      <q-card>
        <q-card-section>
          <div class="text-h6" style="min-width: 350px">
            Create A New Layer
          </div>
        </q-card-section>
        <q-card-section>
          <q-input standout label="Layer Name" v-model="layer_name"/>
          <q-input standout label="Description" v-model="description"/>
          <q-input standout label="Map Image URL" v-model="map_url"/>
          <q-input standout label="Priority" type="number" v-model="priority"/>
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
  name: 'CreateNewLayerDialog',
  props: {
    visible: {
      type: Boolean
    },
    api_client: {
      type: Object,
      required: true
    },
    map_id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      layer_name: '',
      description: '',
      map_url: null,
      priority: 0,
      public: false
    }
  },
  computed: {
    isVisible() {
      return this.visible
    }
  },
  methods: {
    handleCancel() {
      this.layer_name = ''
      this.description = ''
      this.map_url = null
      this.priority = 0
      this.public = false

      this.$emit('close')
    },
    async handleCreate() {
      await this.api_client.createLayer(this.map_id, this.layer_name, this.description, this.map_url, this.priority, this.public)
      this.handleCancel()
    }
  }
});
</script>
