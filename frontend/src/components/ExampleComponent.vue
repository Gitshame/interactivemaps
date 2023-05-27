<template>
  <div>
    <p>{{ mapsStore }}</p>
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
import { useInteractiveMapStore } from 'stores/map-store'

export default defineComponent({
  name: 'ExampleComponent',
  props: {
    title: {
      type: String,
      required: true
    },
    todos: {
      type: Array as PropType<Todo[]>,
      default: () => []
    },
    meta: {
      type: Object as PropType<Meta>,
      required: true
    },
    active: {
      type: Boolean
    }
  },
  setup (props) {
    const mapsStore = useInteractiveMapStore()
    api.get("/maps")
      .then((response) => {
        mapsStore.loadMaps(response)
      })
    return { mapsStore };
  },
});
</script>
