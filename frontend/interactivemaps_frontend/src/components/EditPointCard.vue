<template>
  <div>
    <q-dialog v-model="isVisible">
      <q-card>
        <q-card-section>
          <div class="text-h6" style="min-width: 350px">
            Edit Point
          </div>
        </q-card-section>
        <q-card-section>
          <q-input standout label="Point Name" v-model="point_name" />
          <q-input standout label="X Coordinate" v-model="x_coordinate" />
          <q-input standout label="Y Coordinate" v-model="y_coordinate" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn @click="handleCancel" label="Cancel"/>
          <q-btn @click="handleUpdate" color="primary" label="Update"/>
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
import {InteractiveMapPoint, useInteractiveMapStore} from 'stores/map-store'

export default defineComponent({
  name: 'EditPointCard',
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
    layer_id: {
      type: Number,
      required: true
    },
    point: {
      type: Object as PropType<InteractiveMapPoint>,
      required: true
    }
  },
  computed: {
    isVisible(): boolean {
      return this.visible || false
    },
  },
  data() {
    return {
      point_name: ref(this.point.name),
      x_coordinate: ref(this.point.x_position),
      y_coordinate: ref(this.point.y_position)
    }
  },
  methods: {
    handleCancel() {
      this.point_name = this.point.name
      this.x_coordinate = this.point.x_position
      this.y_coordinate = this.point.y_position

      this.$emit('close')
    },
    async handleUpdate() {
      await this.api_client.updatePoint(this.map_id, this.layer_id, this.point.id, this.point_name, this.x_coordinate, this.y_coordinate)

      this.$emit('close')
    }
  },
});
</script>
