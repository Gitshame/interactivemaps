<template>
  <div>
    <router-view />
  </div>
</template>

<script lang="ts">
import {defineComponent, ref, watch} from 'vue';
import {useRoute} from "vue-router";
import {api} from "boot/axios";
import {useInteractiveMapStore} from "stores/map-store";
import {APIClient} from "assets/js/api_client";
export default defineComponent({
  name: 'App',
  setup () {
    const mapsStore = useInteractiveMapStore()
    const backendClient = new APIClient(mapsStore)

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const code = urlParams.get('code');

    if (code != null) {
      backendClient.getToken(code);
    }
  },
});
</script>
