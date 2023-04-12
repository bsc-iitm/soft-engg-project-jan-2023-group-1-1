<template>
    <div class="conatiner">
        <div class="topic-container">
            <div class="row">
                <div class="col-md-10">
                    <h3>Hi Agent</h3>
                </div>
                <div class="col-md-2">
                    <div class="btn-group">
                        <button type="button" class="btn dropdown-toggle sortB" data-bs-toggle="dropdown">
                            Sort
                        </button>
                        <ul class="dropdown-menu">
                            <li class="dropdown-item text-center" @click="sort_upvotes">Number of upvotes</li>
                            <li class="dropdown-item text-center" @click="sort_time">Time of creation</li>
                        </ul>
                    </div>
                </div>
            </div>
            <br />
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
                            <button class="btn upvote">^<br>{{
                                t.number_of_upvotes }}</button>
                        </div>
                        <div class="row">
                            <div class="btn-group">
                                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown">
                                    Options
                                </button>
                                <ul class="dropdown-menu">
                                    <li class="dropdown-item text-center" @click="flagTicket(t.ticket_id, t.creator_id)">Flag</li>
                                    <li class="dropdown-item text-center" @click="suggestFAQ(t.ticket_id)">
                                        Suggest as FAQ
                                    </li>
                                    <li class="dropdown-item text-center" @click="mark_as_closed(t.ticket_id)">
                                        Mark as closed
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <hr />
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
export default {
    name: "DashboardSupportAgentComponent",
    data() {
        return {
            tickets: []
        };
    },
    async created() {
        await axios.get("/api/ticketAll").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                if(res.data.data[i].is_open == 1)
                    this.tickets.push(res.data.data[i]);
            }
        });
    },
    methods: {
        async flagTicket(ticket_id, creator_id) {
            var data = {
                ticket_id: ticket_id,
                is_offensive: 1
            }
            data = JSON.stringify(data);
            await axios.patch("/api/ticketAll", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            let flagger_id = localStorage.getItem("user_id")
            await axios.post("/api/flaggedPosts", {ticket_id: ticket_id, creator_id: creator_id, flagger_id: flagger_id});
            this.$router.go();
        },
        sort_upvotes() {
            this.tickets.sort((a, b) => {
                return b.number_of_upvotes - a.number_of_upvotes;
            });
        },
        sort_time() {
            this.tickets.sort((a, b) => {
                return new Date(b.created_at) - new Date(a.created_at);
            });
        },
        async suggestFAQ(ticket_id) {
            var data = {
                ticket_id: ticket_id,
                is_faq: 1
            }
            data = JSON.stringify(data);
            await axios.patch("/api/ticketAll", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        },
        async mark_as_closed(ticket_id) {
            var data = {
                ticket_id: ticket_id,
                is_open: 0
            }
            data = JSON.stringify(data);
            await axios.patch("/api/ticketAll", data).then((res) => {
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

.sortB {
    background-color: #000000;
    color: #ffffff;
    font-weight: bold;
    font-size: 10px;
    border-radius: 10%;
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