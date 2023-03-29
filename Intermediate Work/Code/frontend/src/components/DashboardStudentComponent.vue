<template>
    <div class="conatiner">
        <div class="topic-container">
            <div v-for="t in tickets" :key="t.ticket_id">
                <div class="row">
                    <div class="col-md-10">
                        <p class="ticket-title">{{ t.title }}</p>
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
                                    Move
                                </button>
                                <ul class="dropdown-menu">
                                    <li class="dropdown-item text-center" @click="deleteTicket(t.ticket_id)"> Delete </li>
                                    <li class="dropdown-item text-center">Edit</li>
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
    name: "DashboardStudentComponent",
    data() {
        return {
            tickets: []
        };
    },
    async created() {
        await axios.get("http://127.0.0.1:5000/api/ticket", {
            headers: {
                "secret_authtoken": localStorage.getItem("token")
            }
        }).then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                this.tickets.push(res.data.data[i]);
            }
        });
    },
    methods: {
        increaseVote(ticket_id, upVotes) {
            var data = {
                ticket_id: ticket_id,
                number_of_upvotes: upVotes + 1
            }
            data = JSON.stringify(data);
            axios.patch("http://127.0.0.1:5000/api/ticket", data, {
                headers: {
                    "secret_authtoken": localStorage.getItem("token")
                }
            }).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        },
        deleteTicket(ticket_id) {
            axios.delete("http://127.0.0.1:5000/api/ticket/" + ticket_id, {
                headers: {
                    "secret_authtoken": localStorage.getItem("token")
                }
            }).then((res) => {
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
</style>