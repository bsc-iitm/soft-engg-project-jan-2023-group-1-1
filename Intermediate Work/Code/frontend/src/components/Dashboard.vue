<template>
    <component :is="appropriateComponent"></component>
</template>
  

<script>
import { mapGetters } from "vuex";
import DashboardStudentComponent from './DashboardStudentComponent.vue';
import DashboardAdminComponent from './DashboardAdminComponent.vue';
import DashboardSupportAgentComponent from './DashboardSupportAgentComponent.vue';

export default {
  name: 'dash_board',
  components: {
    DashboardStudent: DashboardStudentComponent,
    DashboardAdmin: DashboardAdminComponent,
    DashboardSupport: DashboardSupportAgentComponent,
  },
  computed: {
    ...mapGetters("role"),
    appropriateComponent() {
    switch(this.$store.state.role){
        case 1:
            return "DashboardStudent"
        case 2: 
            return "DashboardSupport"
        case 3: 
            return "DashboardAdmin"
    }
    return null
    }
  },
};
</script>