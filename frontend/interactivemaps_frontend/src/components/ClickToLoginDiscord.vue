<template>
  <div>
    <q-btn
      class="glossy"
      rounded
      color="deep-purple"
      label="Log In with Discord"
      href="http://localhost:8000/login"
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
import { useInteractiveMapStore } from 'stores/map-store'

export default defineComponent({
  name: 'ClickToLoginDiscord',
});
</script>
