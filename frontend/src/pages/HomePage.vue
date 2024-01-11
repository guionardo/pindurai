<template>
  <q-page>
    <h2>{{ pdv.name }}</h2>
    <div class="flex row">
      <SalesCard class="m-2" v-for="sale in pdv.pending_sales" :sale="sale" v-bind:key="sale.id" />
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useConsts } from '../services/consts.js'
import { useMainStore } from 'src/stores/mainStore'
import { useRouter } from 'vue-router'
import SalesCard from 'components/SalesCard.vue'
const { AppTitle } = useConsts()
const store = useMainStore()
const router = useRouter()
export default defineComponent({
  name: 'HomePage',
  props: ['pdv_id'],
  components: { SalesCard },
  beforeMount(e) {

    debugger
    console.log('HomePage.beforeMount', this)
    if (!(this.pdv_id && store.pos.find(x => x.id == this.pdv_id))) {
      router.push({ path: `/pdv/${store.username.default_pos_id}` })
      return
    }

  },
  setup(props) {
    console.log('HomePage.setup', props)
    store.getAllPos()
    debugger
    const pdv = store.pos.find(x => x.id == props.pdv_id)

    return {
      AppTitle,
      isAuthorized: store.isAuthorized,
      pos: store.pos,
      pdv
    }
  }
})
</script>
