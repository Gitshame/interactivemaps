<template>
  <q-card bordered>
    <q-card-section class="text-bold">
      {{ layer.name }}
    </q-card-section>
    <q-separator inset />
    <q-card-section
      v-for="point in mapsStore.getMapLayerPoints(this.map_id, layer.id)"
      v-bind:key="point.id"
      @click="focusMapHandler([point.x_position, point.y_position])">
      {{ point.name }}
    </q-card-section>
    <q-card-actions>
      <q-btn
        icon="delete_forever"
        label="Delete"
        rounded
        v-if="layer.permissions.delete"
        @click="handleDeleteLayer(layer.id)"/>
      <q-btn
        icon="manage_accounts"
        round
        v-if="layer.permissions.modify"
        @click="permissionDialogVisible=true"
      />
    </q-card-actions>
    <LayerPermissionDialog
      :visible="permissionDialogVisible"
      :layer_id="layer.id"
      :map_id="map_id"
      v-if="permissionDialogVisible"
      @close="permissionDialogVisible=false"/>
  </q-card>
</template>

<script lang="ts">
import {
  defineComponent,
  PropType,
  ref,
} from 'vue';
import {useInteractiveMapStore, InteractiveMapLayer} from "stores/map-store";
import {APIClient} from "assets/js/api_client";
import LayerPermissionDialog from "components/LayerPermissionDialog.vue";

export default defineComponent({
  name: 'LayerCard',
  components: {LayerPermissionDialog},
  props: {
    layer: {
      type: Object as PropType<InteractiveMapLayer>,
      required: true
    },
    map_id: {
      type: Number,
      required: true
    },
    focusMapHandler: {
      type: Function,
      required: true
    }
  },
  setup (props) {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)

    const permissionDialogVisible = ref(false)

    const handleDeleteLayer = (layer_id: number) => {
      backendClient.deleteLayer(props.map_id, layer_id)
    }

    return { mapsStore, handleDeleteLayer, permissionDialogVisible }
  },
});
</script>
