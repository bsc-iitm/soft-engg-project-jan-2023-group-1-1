<template>
    <nav class="navbar navbar-expand-lg bg-light" style="width: 100%;">
        <div class="container-fluid">
            <router-link to="/DraggerComp" class="navbar-brand">APPLICATION</router-link>

            <form class="d-flex" role="search">
                <button class="btn btn-outline-danger" type="submit" @click="logout">Logout</button>
            </form>
        </div>
    </nav>
</template>
<script>
export default {
    name: 'NavBar'
}
</script>
