<template>
  <div>
    <q-dialog v-model="isVisible">
      <q-card>
        <q-card-section>
          <div class="text-h6" style="min-width: 350px">
            Create A New Point
          </div>
        </q-card-section>
        <q-card-section>
          <q-input standout label="Point Name" v-model="point_name"/>
          <q-select label="Layer"
                    :options="this.layers"
                    v-model="layer"
                    option-label="name"
                    option-value="id"/>
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
  name: 'CreateNewPointCard',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    api_client: {
      type: Object,
      required: true
    },
    map_id: {
      type: Number,
      required: true
    },
    layers: {
      type: Array,
      required: true
    },
    x_position: {
      type: Number,
      required: true
    },
    y_position: {
      type: Number,
      required: true
    }
  },
  computed: {
    isVisible() {
      return this.visible || false
    }
  },
  data() {
    return {
      point_name: '',
      layer: null
    }
  },
  methods: {
    handleCancel() {
      this.point_name = ''
      this.layer = null

      this.$emit('close')
    },
    async handleCreate() {
      console.log(this.api_client)
      await this.api_client.createPoint(this.map_id, this.layer['id'], this.point_name, this.x_position, this.y_position)
      this.handleCancel()
    }
  },
});
</script>
