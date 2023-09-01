<template>
  <div>
    <div class="text-h5">
      {{ point.name }}
    </div>
    <q-card-actions align="right">
      <q-btn
        color="red"
        rounded
        icon="delete_forever"
        label="Delete"
        @click="handleDelete"
        v-if="canDelete"/>
      <q-btn
        color="red"
        rounded
        icon="delete_forever"
        label="Edit"
        @click="editCardVisible=true"
        v-if="canEdit"/>
    </q-card-actions>
    <EditPointCard
      :point="point"
      :visible="editCardVisible"
      :api_client="apiClient"
      :map_id="map_id"
      :layer_id="layer_id"
      @close="editCardVisible=false"
    />
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
import { Todo, Meta } from './models';
import { api } from 'boot/axios';
import { useInteractiveMapStore, InteractiveMapPoint } from 'stores/map-store'
import {APIClient} from "assets/js/api_client";
import EditPointCard from "components/EditPointCard.vue";


export default defineComponent({
  name: 'MapPointCard',
  components: {EditPointCard},
  props: {
    point: {
      type: Object as PropType<InteractiveMapPoint>,
      required: true
    },
    layer_id: {
      type: Number,
      required: true
    },
    map_id: {
      type: Number,
      required: true
    },
    apiClient: {
      type: APIClient,
      required: true
    },
    canDelete: {
      type: Boolean,
      required: true
    },
    canEdit: {
      type: Boolean,
      required: true
    }
  },
  setup (props) {
    console.log("map point goes here")
    const handleDelete = () => {
      props.apiClient.deletePoint(props.map_id, props.layer_id, props.point.id)
    }

    const editCardVisible = ref(false)

    return {handleDelete, editCardVisible}
  },
});
</script>
