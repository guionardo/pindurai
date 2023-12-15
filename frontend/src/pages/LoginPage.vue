<template>
    <q-page class="flex flex-center">
        <q-card class="my-card q-pa-md">
            <q-card-section>
                <div class="text-h6">Digite suas credenciais</div>
            </q-card-section>
            <div>{{ auth }}</div>
            <div>{{ validUntil }}</div>
            <q-separator />
            <q-form class="q-gutter-md">
                <q-input filled v-model="username" label="Usuário" />
                <q-input filled v-model="password" label="Senha" type="password" />
                <div>
                    <q-btn label="Entrar" color="primary" @click="doLogin" />
                </div>
            </q-form>
        </q-card>
    </q-page>
</template>

<script>
import { defineComponent, computed, ref } from 'vue'
import { useMainStore } from 'src/stores/mainStore';
import { storeToRefs } from 'pinia';
import { useBackendApi } from 'src/services/backendApi'
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'LoginPage',
    setup() {
        const username = ref('')
        const password = ref('')

        const store = useMainStore();

        const auth = computed(() => store.auth.authorization)
        const validUntil = computed(() => store.auth.validUntil)

        // // Option 3: use destructuring to use the store in the template
        // const { counter, doubleCount } = storeToRefs(store); // state and getters need "storeToRefs"
        // const { increment } = store; // actions can be destructured directly
        const api = useBackendApi()
        const doLogin = async () => {
            try {
                const auth = await store.login(username.value, password.value)
                console.info('LoginPage.login', auth)
                await store.getWhoIAm()
                await store.getAllPos()
            } catch (err) {
                console.error('LoginPage.login', err)
            }
        }
        return {
            username, password,
            // Option 1: return the store directly and couple it in the template
            store, auth, validUntil,
            doLogin,
            // Option 2: use the store in functions and compute the state to use in the template


            // // Option 3: pass the destructed state, getters and actions to the template
            // counter,
            // increment,
            // doubleCount,
        };
    }
})
</script>
<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 250px
</style>
