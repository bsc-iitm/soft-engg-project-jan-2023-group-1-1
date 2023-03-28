<script >
import { createWebHistory, createRouter } from 'vue-router';
import ChangePasswordComponent from './components/ChangePasswordComponent.vue';
import LoginComponent from './components/LoginComponent.vue';
const routes = [
    {
        path: "/",
        component: LoginComponent,
    },
    {
        path: "/changePassword",
        component: ChangePasswordComponent,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
</script>