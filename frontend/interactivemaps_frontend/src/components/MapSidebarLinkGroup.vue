<template>
  <q-expansion-item :label="groupName" v-model="groupOpen">
    <q-card>
      <q-card-section>
        <q-list>
          <MapSidebarLink
            v-for="map in maps"
            :key="map.name"
            v-bind="map"
            :caption="map.caption"
            :title="map.name"
            :link="`/maps/${map.id}`"
          />
        </q-list>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import {InteractiveMap} from "stores/map-store";
import MapSidebarLink from "components/MapSidebarLink.vue";

export default defineComponent({
  name: 'MapSidebarLinkGroup',

  components: {MapSidebarLink},

  props: {
    groupName: {
      type: String,
      required: true
    },
    maps: {
      type: Array<InteractiveMap>,
      required: true
    }
  },

  setup() {
    const groupOpen = ref(true)
    return {
      groupOpen
    }
  }
})
</script>
