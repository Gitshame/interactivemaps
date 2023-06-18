<template>
  <q-card>
    <div class="text-h5">Layers</div>
    <q-card
      v-for="layer in layers"
      v-bind:key="layer.id">
      <q-card-section>
        <LayerCard :focusMapHandler="this.focusMapHandler"
                   :map_id="map_id"
                   :layer="layer" />
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
import LayerPermissionDialog from "components/LayerPermissionDialog.vue";
import LayerCard from "components/LayerCard.vue";

export default defineComponent({
  name: 'LayerListCard',
  components: {
    LayerCard
  },
  props: {
    layers: Array,
    focusMapHandler: {
      type: Function,
      required: true
    },
    map_id: {
      type: Number,
      required: true
    }
  },
  setup () {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)

    return { mapsStore }
  },
});
</script>
