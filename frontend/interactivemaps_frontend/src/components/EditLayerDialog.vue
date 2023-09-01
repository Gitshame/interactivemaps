<template>
  <div>
    <q-dialog v-model="isVisible">
      <q-card>
        <q-card-section>
          <div class="text-h6" style="min-width: 350px">
            Edit Layer
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
} from 'vue';
import {InteractiveMapLayer} from 'stores/map-store';


export default defineComponent({
  name: 'EditLayerDialog',
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
    },
    layer_input: {
      type: Object as PropType<InteractiveMapLayer>,
      required: true
    }
  },
  data() {
    return {
      layer_name: this.layer_input.name,
      description: this.layer_input.description,
      map_url: this.layer_input.image,
      priority: this.layer_input.priority,
      public: this.layer_input.public
    }
  },
  computed: {
    isVisible() {
      return this.visible
    }
  },
  methods: {
    handleCancel() {
      this.layer_name = this.layer_input.name
      this.description = this.layer_input.description
      this.map_url = this.layer_input.image
      this.priority = this.layer_input.priority
      this.public = this.layer_input.public

      this.$emit('close')
    },
    async handleUpdate() {
      await this.api_client.updateLayer(this.map_id, this.layer_input.id, this.layer_name, this.description, this.map_url, this.priority, this.public)

      this.$emit('close')
    }
  }
});
</script>
