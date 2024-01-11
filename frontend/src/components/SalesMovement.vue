<template>
    <!--
        {"id":1,"user":"guionardo","date":"2023-12-08T23:40:55.120Z","movement_type":"S","movement_type_str":"Venda","description":"Venda","value":150}
{"id":2,"user":"guionardo","date":"2023-12-08T23:44:02.132Z","movement_type":"P","movement_type_str":"Pagamento","description":"Cartão","value":50}
{"id":3,"user":"guionardo","date":"2023-12-08T23:46:59.992Z","movement_type":"A","movement_type_str":"Acréscimo","description":"Taxa","value":1.5}
{"id":4,"user":"guionardo","date":"2023-12-08T23:53:53.779Z","movement_type":"D","movement_type_str":"Desconto","description":"teste","value":30}
    -->
    <q-list>
        <!-- <q-item>
            {{ JSON.stringify(movement) }}
        </q-item> -->
        <q-item v-for="movement in movements" v-bind:key="movement.id" clickable v-ripple>
            <q-item-section avatar>
                <q-icon :color="getCor(movement)" :name="getIcon(movement)" />
            </q-item-section>

            <q-item-section>
                <q-item-label overline>{{ movement.movement_type_str }}</q-item-label>
                <q-item-label caption lines="2">{{ movement.description }}</q-item-label>

            </q-item-section>
            <q-item-section side top>
                <q-item-label caption>{{ getData(movement) }}</q-item-label>
                <q-item-label caption>{{ fmtReal(movement.value) }}</q-item-label>
                <!-- <q-icon name="star" color="yellow" /> -->
            </q-item-section>
        </q-item>

        <!-- <q-item clickable v-ripple>
            <q-item-section avatar>
                <q-avatar color="teal" text-color="white" icon="bluetooth" />
            </q-item-section>

            <q-item-section>Avatar-type icon</q-item-section>
        </q-item>

        <q-item clickable v-ripple>
            <q-item-section avatar>
                <q-avatar rounded color="purple" text-color="white" icon="bluetooth" />
            </q-item-section>

            <q-item-section>Rounded avatar-type icon</q-item-section>
        </q-item>

        <q-item clickable v-ripple>
            <q-item-section avatar>
                <q-avatar color="primary" text-color="white">
                    R
                </q-avatar>
            </q-item-section>

            <q-item-section>Letter avatar-type</q-item-section>
        </q-item>

        <q-separator />

        <q-item clickable v-ripple>
            <q-item-section avatar>
                <q-avatar>
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                </q-avatar>
            </q-item-section>
            <q-item-section>Image avatar</q-item-section>
        </q-item>

        <q-item clickable v-ripple>
            <q-item-section avatar>
                <q-avatar square>
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                </q-avatar>
            </q-item-section>
            <q-item-section>Image square avatar</q-item-section>
        </q-item>

        <q-item clickable v-ripple>
            <q-item-section avatar>
                <q-avatar rounded>
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                </q-avatar>
            </q-item-section>
            <q-item-section>Image rounded avatar</q-item-section>
        </q-item>

        <q-separator />

        <q-item clickable v-ripple>
            <q-item-section avatar>
                <q-avatar rounded>
                    <img src="https://cdn.quasar.dev/img/mountains.jpg">
                </q-avatar>
            </q-item-section>
            <q-item-section>List item</q-item-section>
        </q-item>

        <q-item clickable v-ripple>
            <q-item-section thumbnail>
                <img src="https://cdn.quasar.dev/img/mountains.jpg">
            </q-item-section>
            <q-item-section>List item</q-item-section>
        </q-item> -->
    </q-list>
</template>

<script>
import { defineComponent } from 'vue'
import { fmtReal } from 'src/services/utils';

export default defineComponent({
    name: 'SalesMovement',
    props: {
        movements: { type: Array, required: true },
    },
    methods: {
        fmtReal,
        getCor(mvt) {
            return {
                S: 'blue',
                P: 'green',
                A: 'red',
                D: 'orange',
            }[mvt.movement_type]
        },
        getIcon(mvt) {
            return {
                S: 'shopping_bag',
                P: 'paid',
                A: 'vertical_align_top',
                D: 'vertical_align_bottom',
            }[mvt.movement_type]
        },
        getData(mvt) {
            return new Date(mvt.date).toLocaleTimeString()
        }
    },
})
</script>
