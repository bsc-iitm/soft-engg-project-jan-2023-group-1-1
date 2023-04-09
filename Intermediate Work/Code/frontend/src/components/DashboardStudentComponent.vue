<template>
    <div class="conatiner">
        <div class="topic-container">
            <div v-for="t in tickets" :key="t.ticket_id">
                <div class="row">
                    <div class="col-md-10">
                        <RouterLink :to="{ name: 'response', params: { ticketId: t.ticket_id } }">
                            <p class="ticket-title">
                                {{ t.title }}
                            </p>
                        </RouterLink>
                        <div class="btn-grp">
                            <div v-if="t.is_open == 0">
                                <button class="btn btn-sm open">closed</button>
                            </div>
                            <div v-else>
                                <button class="btn btn-sm closed">open</button>
                            </div>
                            <div v-if="t.is_read == 1">
                                <button class="btn btn-sm closed">read</button>
                            </div>
                            <div v-else>
                                <button class="btn btn-sm open">unread</button>
                            </div>
                        </div>
                        <p>{{ t.description }}</p>
                    </div>
                    <div class="col-md-2">
                        <div class="row">
                            <button class="btn upvote" @click="increaseVote(t.ticket_id, t.number_of_upvotes)">^<br>{{
                                t.number_of_upvotes }}</button>
                        </div>
                        <div class="row">
                            <div class="btn-group">
                                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown">
                                    Options
                                </button>
                                <ul class="dropdown-menu">
                                    <li class="dropdown-item text-center" @click="deleteTicket(t.ticket_id)"> Delete </li>
                                    <li class="dropdown-item text-center">
                                        <RouterLink :to="{ name: 'editTicket', params: { ticketId: t.ticket_id } }">
                                            Edit
                                        </RouterLink>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <hr />
            </div>
        </div>
        <div class="text-center">
            <button class="btn btn-lg btn-primary">
                <RouterLink to="/addTicket">New Ticket</RouterLink>
            </button>
        </div>
    </div>
</template>
<script>
import axios from "axios";
export default {
    name: "DashboardStudentComponent",
    data() {
        return {
            tickets: []
        };
    },
    async created() {
        await axios.get("/api/ticket").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                this.tickets.push(res.data.data[i]);
            }
        });
    },
    methods: {
        async increaseVote(ticket_id, upVotes) {
            var data = {
                ticket_id: ticket_id,
                number_of_upvotes: upVotes + 1
            }
            data = JSON.stringify(data);
            await axios.patch("/api/ticket", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        },
        async deleteTicket(ticket_id) {
            await axios.delete("/api/ticket/" + ticket_id).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        }
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
.closed {
    border: none;
    background: #2fe72f;
    border-radius: 10%;
    color: white;
    margin-bottom: 5px;
    margin-right: 10px;
}

.open {
    border: none;
    background: #e7572f;
    border-radius: 10%;
    color: white;
    margin-bottom: 5px;
    margin-right: 10px;
}
.btn-grp {
    display: flex;
    flex-direction: row;
    /* margin-right: 2px; */
}
</style>