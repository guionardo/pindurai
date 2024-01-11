<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="img:src/assets/pindurai-logo.svg" aria-label="Menu" />

        <q-toolbar-title>
          {{ AppTitle }}
        </q-toolbar-title>

        <div>v{{ store.backend.version }}</div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
import { useConsts } from '../services/consts';
import { useMainStore } from 'src/stores/mainStore';

const { AppTitle } = useConsts();

export default defineComponent({
  name: 'MainLayout',

  components: {},

  setup() {
    const store = useMainStore()
    store.updateBackendStatus()
    return {
      AppTitle, store
    }
  }
})
</script>
