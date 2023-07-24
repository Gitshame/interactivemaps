<template>
  <q-card bordered>
    <q-card-section class="text-bold">
      {{ layer.name }}
    </q-card-section>
    <q-separator inset />
    <q-card-section
      v-for="point in mapsStore.getMapLayerPoints(map_id, layer.id)"
      v-bind:key="point.id"
      @click="focusMapHandler([point.x_position, point.y_position])">
      {{ point.name }}
    </q-card-section>
    <q-card-actions>
      <q-btn
        icon="delete_forever"
        rounded
        v-if="layer.permissions.delete"
        @click="handleDeleteLayer(layer.id)"/>
      <q-btn
        icon="manage_accounts"
        round
        v-if="layer.permissions.modify"
        @click="permissionDialogVisible=true"
      />
      <q-btn
        icon="edit"
        round
        v-if="layer.permissions.modify"
        @click="editDialogVisible=true" />
    </q-card-actions>
    <LayerPermissionDialog
      :visible="permissionDialogVisible"
      :layer_id="layer.id"
      :map_id="map_id"
      v-if="permissionDialogVisible"
      @close="permissionDialogVisible=false"/>
  </q-card>
  <EditLayerDialog
    :visible=editDialogVisible
    :layer_input="layer"
    :api_client="backendClient"
    :map_id="map_id"
    @close="editDialogVisible=false"/>
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
import EditLayerDialog from "components/EditLayerDialog.vue";

export default defineComponent({
  name: 'LayerCard',
  components: {EditLayerDialog, LayerPermissionDialog},
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
    const editDialogVisible = ref(false)

    const handleDeleteLayer = (layer_id: number) => {
      backendClient.deleteLayer(props.map_id, layer_id)
    }

    return { mapsStore, backendClient, handleDeleteLayer, permissionDialogVisible, editDialogVisible }
  },
});
</script>
