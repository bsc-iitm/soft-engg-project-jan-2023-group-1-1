<template>
  <div class="container">
    <h1 class="text-center">Login</h1>
    <form @submit.prevent="loginUser">
      <div class="form-group">
        <label>Email</label>
        <input type="text" v-model="email" class="form-control" placeholder="Enter Email" autocomplete="off" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" v-model="password" class="form-control" placeholder="Password" autocomplete="off" required>
      </div>
      <button type="submit" class="btn btn-primary btn-lg">Submit</button>

      <p class="text" style="margin-top:10px">
        You want to change password? <a href="#">Change Password</a>
      </p>
    </form>
  </div>
</template>

<script>
export default {
  name: "LoginComponent",
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    async loginUser(e) {
      e.preventDefault();
      console.log(this.email, this.password);
      this.$bvToast.toast("Login Successful", {
        title: "Success",
        variant: "success",
        solid: true
      });
    },
  }
}
</script>

<style scoped>
.container {
  /* border: #40cbea solid 2px;
  border-radius: 20px; */
  font-family: "Muli", sans-serif;
  margin-top: 50px;
  width: 50%;
  padding: 20px 40px;
  margin-left: auto;
  margin-right: auto;
}

.container h1 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 50px;
}

.form-group {
  margin-bottom: 25px;
}

label {
  font-size: 20px;
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
}
</style>
