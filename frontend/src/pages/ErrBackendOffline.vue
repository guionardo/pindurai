<template>
  <div class="fullscreen bg-orange text-white text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 30vh">
        500
      </div>

      <div class="text-h2">
        Ops! Backend não está respondendo!
      </div>

      <q-btn class="q-mt-xl" color="white" text-color="blue" unelevated :to="returnTo" label="Tentar novamente" no-caps />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ErrorNotFound',
  props: function(){
    return {'returnTo':'/'}
  }
})
</script>
