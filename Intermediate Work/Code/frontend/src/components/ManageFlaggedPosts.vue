<template>
    <div class="container">
        <div class="topic-container">
            <h3>The following tickets have been flagged. </h3>
            <br/>
            <hr/>
            <br/>
            <div class="container" v-for="(t, index) in relevant_tickets"  :key="index">
                <div class="row">
                    <div class="col-md-10">
                        <RouterLink :to="{ name: 'response', params: { ticketId: t.ticket_id } }">
                            <p class="ticket-title">
                                {{ t.title }}
                            </p>
                        </RouterLink>
                        <p>{{ t.description }}</p>
                       
                    </div>
                    
                    <div class="col-md-2">
                        <div class="row">
                            <button class="btn upvote disabled">^<br>{{t.number_of_upvotes }}</button>
                        </div>
                        <br/>
                    </div>
                </div>
                <br/>
                <hr/>
            </div>
        </div>
        <br/>
        <!-- Modal -->

    </div>
</template>
<script>
//import router from '@/router';

import axios from 'axios';

export default {
    name: "ManageFlaggedPosts",
    data() {
        return {
            data : null,
            selected: null,
            selected_ticket: null,
            flagged_ticket_ids: [],
            relevant_tickets: []
        };
    
    },
    async created() {
        var res3 = await axios.get('/api/flaggedPosts');
        this.data = res3.data.data;
        this.flagged_ticket_ids = this.data.map(({ticket_id}) => ticket_id);
        var res2 = await axios.get('/api/ticketAll');
        for (var i = 0; i < res2.data.data.length; i++) {
            if (res2.data.data[i].is_offensive) {
                // eslint-disable-next-line
                if (this.flagged_ticket_ids.includes(res2.data.data[i].ticket_id)){
                    this.relevant_tickets.push(res2.data.data[i]);
                }
            }
        }
        console.log(res2);
    },
    computed: {
    }
}
</script>
<style scoped>
.topic-container {
    margin: 33px 63px;
}

.upvote {
    font-size: 20px;
}

.ticket-title {
    font-weight: bold;
    font-size: 25px;
}

.btn a {
    color: rgb(255, 255, 255);
    text-decoration: none;
}

a {
    color: rgb(0, 0, 0);
    text-decoration: none;
}
</style>