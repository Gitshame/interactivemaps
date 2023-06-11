<template>
  <div>
    <q-btn
      class="glossy"
      rounded
      color="deep-purple"
      label="Log In with Discord"
      :href="api_base_url() + '/login'"
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
import {api, api_base_url} from 'boot/axios';
import { useInteractiveMapStore } from 'stores/map-store'

export default defineComponent({
  name: 'ClickToLoginDiscord',
  methods: {
    api_base_url() {
      return api_base_url
    }
  },
});
</script>
