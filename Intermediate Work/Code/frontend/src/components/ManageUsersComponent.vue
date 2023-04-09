<template>
    <div class="container">
        <div class="topic-container">
            <h3>ADD A USER BY EMAIL ID</h3>
        </div>
        <br />
        <form v-on:submit="addUser">
            <!-- <div class="row"> -->
                <!-- <div class="col-md-10"> -->
                    <div class="form-group"><label>Enter Email ID</label><input type="text" class="form-control" v-model="emailID"  required /></div>
                <!-- </div> -->
                <!-- <br />
                <br />
                <br />
                <div class="col-md-10">
                    <input type="text" class="form-control" v-model="roleID" placeholder="Enter Role" required />
                </div> -->
                <br/>
                
                <div class="form-group"><label>Choose Role</label><select v-model="roleID" class="form-select">
                    <option value="student">Student</option>
                    <option value="support agent">Support Agent</option>
                    <option value="admin">Admin</option>
                    <option value="manager">Manager</option>
                    
                </select></div>

                <!-- <div class="col-md-2"> -->
                    
                    <button class="btn btn-lg" type="submit">Submit</button>
                <!-- </div> -->
            <!-- </div> -->
        </form>
        <div class="topic-container">
            <h3>ADD MULTIPLE USERS BY CSV FILE</h3>
        </div>
        <br/>
        <label> Please upload a CSV file if you wish to import data</label><br/>
        <div class="form-group"><input class="btn btn-lg" ref="file" id = file type="file" accept=".csv" v-on:change="onUpload($event)" /></div>
        
        <button class="btn btn-outline-success rounded" @click="fileSubmission">Submit</button>
    </div>
</template>
<script>
//import router from '@/router';
import axios from 'axios';
export default {
    name: "ManageUsersComponent",
    data() {
        return {
            emailID: "",
            roleID: "",
            myFile: ''
        };

    },
    methods: {
        async addUser(x) {
            // console.log(this.response)
            x.preventDefault();
            let thing = null;
            if (this.roleID.toLowerCase() == "student") {
                thing = 1;
            }
            else if (this.roleID.toLowerCase() == "admin") {
                thing = 3;
            }
            else if (this.roleID.toLowerCase() == "support agent") {
                thing = 2;
            }
            else if (this.roleID.toLowerCase() == "manager") {
                thing = 4;
            }
            else {
                alert("Please choose role amongst student/admin/manager/support agent!")
                this.roleID = "";
            }
            if (this.roleID == "") {
                location.reload();
            }
            else {
                console.log(this.emailID);
                console.log(thing);
                let c = this.emailID
                var data = { email_id: c, role_id: thing };
                console.log(c);
                data = JSON.stringify(data);
                console.log("Data is :")
                console.log(data);
                await axios.post("/api/user", data).then((res) => {
                    alert("User has been successfully added.")
                    this.$router.go();
                    console.log(res)
                }).catch((err) => {
                    console.log(err);
                });
            }
        },
        onUpload(){
            this.myFile = this.$refs.file.files[0];
        },
        fileSubmission(){
            let formData = new FormData();
            let c = this.myFile;
            formData.append('file',c);
            let authtoken = localStorage.getItem("token");
            fetch("/api/importUsers", {
            method: 'POST', 
            mode: 'cors', 
            cache: 'no-cache', 
            credentials: 'omit', 
            headers: {
              'secret-authtoken' : authtoken
              
            },
            redirect: 'follow', 
            referrerPolicy: 'no-referrer', 
            body: formData 
          }).then ( () => {alert("User addition request has been received. You will get notified via email on the status.");location.reload()}).catch( e => console.log(e));
    },
    }
}
</script>
<style scoped>
.topic-container {
    margin: 33px 63px;
}
.form-group {
    margin-bottom: 1.5rem;
}
</style>