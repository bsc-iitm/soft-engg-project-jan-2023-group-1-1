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
            ticket_id: this.$route.params.ticketId,
            responses:[]
        };
    },
    async created() {
        await axios.get("/api/ticket").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                if (this.ticket_id == res.data.data[i].ticket_id) {
                    this.title = res.data.data[i].title;
                    this.description = res.data.data[i].description;
                }
            }
        });
        var data = {
            ticket_id: this.ticket_id
        }
        data=JSON.stringify(data);
        await axios.post("/api/getResponseAPI_by_ticket", data).then((res) => {
            console.log(res.data.data);
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
.response{
    font-size: 20px;

}
a{
  color: rgb(255, 255, 255);
    text-decoration: none;
}
.dropdown-menu a{
  color: rgb(0, 0, 0);
    text-decoration: none;
}
</style>