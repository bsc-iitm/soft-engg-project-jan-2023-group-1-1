<template>
    <div class="container">
        <h1 class="text-center">Add Ticket</h1>
        <form @submit.prevent="addCard">
            <div class="form-group">
                <label>Title</label>
                <input type="text" v-model="title" class="form-control" placeholder="Enter title" autocomplete="off"
                    required />
            </div>
            <div class="form-group">
                <label>Description</label>
                <input type="text" v-model="description" class="form-control" placeholder="Enter description" autocomplete="off"
                    required>
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>
        </form>
    </div>

</template>
  
<script>
import axios from "axios";
export default {
    name: "AddTicketComponent",
    data() {
        return {
            title: "",
            description: "",
        };
    },
    methods: {
        async addCard() {
            var data = {
                title: this.title,
                description: this.description,
                number_of_upvotes : 0,
                is_read: 0,
                is_open: 0,
                is_offensive: 0,
                is_FAQ: 0
            };
            data = JSON.stringify(data);
            console.log(data);
            await axios.post("/api/ticket",data, {
            headers: {
                    // "secret_authtoken": localStorage.getItem("token"),
                    "Content-Type": "application/json"
            }
            }).then((res) => {
                console.log(res);
                if (res.status == 200) {
                    alert("Ticket Added Successfully");
                    this.$router.push("/dashboard");
                } else {
                    alert(res.data.message);
                }
            }).catch((err) => {
                console.log(err);
            });       
            
        }
    },
}
</script>
  
<style scoped>
.container {
    font-family: "Muli", sans-serif;
    /* display: flex;
     */
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 75vh;
    overflow: hidden;
    margin-top: 75px;
}

label {
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: 5px;
}

h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}
</style>
  