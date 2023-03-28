<script >
import { createWebHistory, createRouter } from 'vue-router';
import ChangePasswordComponent from './components/ChangePasswordComponent.vue';
import LoginComponent from './components/LoginComponent.vue';
import DashboardStudentComponent from './components/DashboardStudentComponent.vue';
import DashboardAdminComponent from './components/DashboardAdminComponent.vue';
import DashboardSupportAgentComponent from './components/DashboardSupportAgentComponent.vue';
const routes = [
    {
        path: "/",
        component: LoginComponent,
    },
    {
        path: "/changePassword",
        component: ChangePasswordComponent,
    },
    {
        path: "/dashboard",
        component: DashboardStudentComponent,
    },
    {
        path: "/dashboardAdmin",
        component: DashboardAdminComponent,
    },
    {
        path: "/dashboardSupportAgent",
        component: DashboardSupportAgentComponent,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
</script>