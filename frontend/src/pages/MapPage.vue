<template>
    <q-page class="row items-center">
      <map-component :map_id=mapId />
    </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import MapComponent from "components/MapComponent.vue";
import {useRoute} from "vue-router";


export default defineComponent({
  name: 'MapPage',
  components: {MapComponent},
  props: {
  },
  setup () {
    const route = useRoute();
    const mapId = parseInt(route.params.map_id, 10)

    return { mapId }
  }
});
</script>
