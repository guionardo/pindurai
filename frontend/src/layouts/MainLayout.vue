<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          {{ AppTitle }}
        </q-toolbar-title>

        <div>v{{ Version }}</div>
        <q-btn icon="account_circle" aria-label="Basic Menu" flat>
          <q-menu>
            <q-list style="min-width: 100px">
              <q-item v-close-popup>
                <q-item-section>{{ store.username.name }}</q-item-section>
              </q-item>
              <q-separator />


                <q-item v-for="p in store.pos" v-bind:key="p.id" v-close-popup>
                  <q-item-section>{{ p.name }}</q-item-section>
                </q-item>

              <q-separator />

              <q-item clickable v-close-popup @click="doLogout">
                <q-item-section>Sair</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header>
          Essential Links
        </q-item-label>

        <EssentialLink v-for="link in essentialLinks" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { useConsts } from '../services/consts';
import { useMainStore } from 'src/stores/mainStore';

const { Version, AppTitle } = useConsts();
const store = useMainStore()

const linksList = [
  {
    title: 'Docs',
    caption: 'quasar.dev',
    icon: 'school',
    link: 'https://quasar.dev'
  },
  {
    title: 'Github',
    caption: 'github.com/quasarframework',
    icon: 'code',
    link: 'https://github.com/quasarframework'
  },
  {
    title: 'Discord Chat Channel',
    caption: 'chat.quasar.dev',
    icon: 'chat',
    link: 'https://chat.quasar.dev'
  },
  {
    title: 'Forum',
    caption: 'forum.quasar.dev',
    icon: 'record_voice_over',
    link: 'https://forum.quasar.dev'
  },
  {
    title: 'Twitter',
    caption: '@quasarframework',
    icon: 'rss_feed',
    link: 'https://twitter.quasar.dev'
  },
  {
    title: 'Facebook',
    caption: '@QuasarFramework',
    icon: 'public',
    link: 'https://facebook.quasar.dev'
  },
  {
    title: 'Quasar Awesome',
    caption: 'Community Quasar projects',
    icon: 'favorite',
    link: 'https://awesome.quasar.dev'
  }
]

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink
  },

  setup() {
    const leftDrawerOpen = ref(false)

    return {
      store,
      Version,
      AppTitle,
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      doLogout() {
        store.logout()
      }
    }
  }
})
</script>
