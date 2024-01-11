<template>
    <q-card class="my-card_" flat bordered>
        <q-item>
            <!-- <q-item-section avatar>
                <q-avatar>
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                </q-avatar>
            </q-item-section> -->

            <q-item-section>
                <q-item-label>{{ sale.client }}</q-item-label>
                <q-item-label caption> {{ sale.description }} @ {{ sale.date }} </q-item-label>
                <q-item-label> {{ fmtReal(sale.value) }} </q-item-label>
            </q-item-section>
            <q-item-section side top>
                <q-item-label overline>Saldo</q-item-label>
                <q-item-label>{{ fmtReal(sale.balance) }}
                </q-item-label>
            </q-item-section>
        </q-item>

        <q-separator />

        <q-card-section horizontal class="p0">
            <!-- <q-card-section>
                {{ lorem }}
            </q-card-section> -->

            <!-- <q-separator vertical /> -->

            <q-card-section class="col-12">
                <sales-movement :movements="sale.movements" />
            </q-card-section>
        </q-card-section>
        <q-separator />
        <q-card-actions>
            <q-btn icon="paid" title="Adicionar pagamento" v-if="canAddPayment" flat @click="addPagamento">pagamento</q-btn>
            <q-btn icon="vertical_align_top" title="Aplicar acréscimo" v-if="canAddPayment" flat
                @click="addAcrescimo">acréscimo</q-btn>
            <q-btn icon="vertical_align_bottom" title="Aplicar desconto" v-if="canAddPayment" flat
                @click="AddDesconto">desconto</q-btn>
        </q-card-actions>
    </q-card>
</template>

<script>
import { defineComponent } from 'vue'
import { Dialog } from 'quasar'
import { fmtReal } from 'src/services/utils';
import SalesMovement from 'components/SalesMovement.vue'
export default defineComponent({
    name: 'SalesCard',
    components: { SalesMovement },
    props: {
        sale: { type: Object, required: true },
        // client: { type: String, required: true },
        // balance: { type: Number, required: true },
        // date: { type: Date, required: true },
        // description: { type: String, required: true },
        id: { type: Number, required: true },
        user: { type: String, required: true },
        // value: { type: Number, required: true },
        movements: { type: Array, required: true }
    },
    methods: {
        fmtReal,
        addPagamento() {
            debugger
            Dialog.create({
                title: 'Adicionar pagamento',
                message: `Informe o valor recebido em R$ de ${this.sale.client}`,
                prompt: {
                    model: -this.sale.balance,
                    type: 'number',
                    cancel: true,
                    persistent: true
                }
            }).onOk(valor => alert(`Recebido: ${valor}`))

        },
        addAcrescimo() {

        },
        addDesconto() {

        }
    },
    setup(props) {
        debugger
        const canAddPayment = props.sale.balance < 0

        return { canAddPayment }
    }
})
</script>
<style lang="sass" scoped>
.my-card
  width: 100%

</style>
