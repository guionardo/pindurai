<template>
  <q-page class="flex flex-center column">
    <img alt="Quasar logo" src="~assets/pindurai-logo.svg" style="width: 200px; height: 200px" />
    <h1>{{ AppTitle }}</h1>
    <p>Uma plataforma para você deixar de usar o caderninho de fiados.</p>
    <p>A prioridade é a simplicidade.</p>
    <ol>
      <li>Você cadastra seu(s) ponto(s)-de-venda</li>
      <li>Você cadastra seus clientes, identificando-os e definindo limite de crédito</li>
      <li>Você efetua sua venda a crédito e combina o pagamento do cliente</li>
      <li>O cliente, fiel e honesto, volta ao seu PDV, efetua o pagamento da dívida</li>
      <li>Em caso de atrasos, podemos habilitar a correção monetária</li>
      <li>As informações do seu PDV estão sempre atualizadas, com os valores a receber, clientes inadinplentes, etc.</li>
    </ol>
    <q-btn class="q-mt-xl" color="primary" text-color="white" unelevated :to="btnTo" :label="btnLabel" no-caps />

  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useConsts } from '../services/consts.js'
import { useMainStore } from 'src/stores/mainStore'
const { AppTitle } = useConsts()
const store = useMainStore()
export default defineComponent({
  name: 'IndexPage',
  setup() {
    const btnLabel = store.isAuthorized ? 'Acessar o sistema' : 'Login'
    const btnTo = store.isAuthorized ? 'home' : 'login'
    return {
      AppTitle,
      btnLabel,
      btnTo
    }
  }
})
</script>
