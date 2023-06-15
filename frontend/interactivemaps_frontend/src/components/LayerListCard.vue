<template>
  <q-card>
    <div class="text-h5">Layers</div>
    <q-card
      v-for="layer in layers"
      v-bind:key="layer.id">
      <q-card-section>
        <q-card bordered>
          <q-card-section class="text-bold">
            {{ layer.name }}
          </q-card-section>
          <q-separator inset />
          <q-card-section
            v-for="point in mapsStore.getMapLayerPoints(this.map_id, layer.id)"
            v-bind:key="point.id"
            @click="this.focusMapHandler([point.x_position, point.y_position])">
            {{ point.name }}
          </q-card-section>
          <q-card-actions>
            <q-btn
              icon="delete_forever"
              label="Delete"
              v-if="layer.permissions.delete"
              @click="handleDeleteLayer(layer.id, $event)"/>
          </q-card-actions>
        </q-card>
      </q-card-section>
    </q-card>
    <q-btn
      label="Add New Layer"
      color="primary"
      rounded
      class="full-width"
      @click="this.$emit('createNewLayer')" />
  </q-card>
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
import {useInteractiveMapStore} from "stores/map-store";
import {APIClient} from "assets/js/api_client";

export default defineComponent({
  name: 'LayerListCard',
  props: {
    layers: Array,
    focusMapHandler: Function,
    map_id: {
      type: Number,
      required: true
    }
  },
  setup (props) {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)

    const handleDeleteLayer = (layer_id: number) => {
      backendClient.deleteLayer(props.map_id, layer_id)
    }

    return { mapsStore, handleDeleteLayer }
  },
});
</script>
