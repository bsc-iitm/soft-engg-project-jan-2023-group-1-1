<template>
    <div class="conatiner">
        <div class="topic-container">
            <div class="row">
                <p class="ticket-title">{{ title }}</p>
                <p>{{ description }}</p>
            </div>
            <hr />
            <h3>Responses :</h3>
            <div v-for="r in responses" :key="r.response_id">
                <p class="response">{{ r.response }}</p>
                <hr />
            </div>
            <form v-on:submit="addResponse">
                <div class="row">
                    <div class="col-md-10">
                        <input type="text" class="form-control" v-model="response" placeholder="Enter Response" />
                    </div>
                    <div class="col-md-2">
                        <button class="btn" type="submit">Submit</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: "ResponseComponent",
    data() {
        return {
            title: "",
            description: "",
            is_read: 0,
            ticket_id: this.$route.params.ticketId,
            response: "",
            responses: []
        };
    },
    methods: {
        async addResponse() {
            // console.log(this.response)
            await axios.post("/api/respTicket", {
                ticket_id: this.ticket_id,
                response: this.response
            }).then((res) => {
                this.response = "";
                this.$router.go();
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
        }
    },
    async created() {
        await axios.get("/api/ticketAll").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                if (this.ticket_id == res.data.data[i].ticket_id) {
                    this.title = res.data.data[i].title;
                    this.description = res.data.data[i].description;
                    this.is_read = res.data.data[i].is_read;
                }
            }
        });
        const role = localStorage.getItem("role");
        if (role == 2 && this.is_read == 0) {
            await axios.patch("/api/ticketAll", {
                ticket_id: this.ticket_id,
                is_read: 1
            }).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
        }
        var data = {
            ticket_id: this.ticket_id
        }
        data = JSON.stringify(data);
        await axios.post("/api/getResponseAPI_by_ticket", data).then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                this.responses.push(res.data.data[i]);
            }
        }).catch((err) => {
            console.log(err);
        });

    },
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

.response {
    font-size: 20px;

}

a {
    color: rgb(255, 255, 255);
    text-decoration: none;
}

.dropdown-menu a {
    color: rgb(0, 0, 0);
    text-decoration: none;
}
</style>