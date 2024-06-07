<template>
  <div>
    <header class="site-header">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <router-link class="nav-item nav-link active" to="/admin/home">Home</router-link> <!-- Added Dashboard -->
            <router-link class="nav-item nav-link" to="/admin_dashboard">Dashboard</router-link>
          </div>
          <div class="navbar-nav" style="margin-left: auto; margin-right: 10px;">
            <a class="btn btn-outline-danger my-2 my-sm-0" @click="logout">Logout</a>
          </div>
        </div>
      </nav>
    </header>
    <main role="main" class="container">
      <div class="row">
        <div class="col-md-10">
          <slot></slot>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
  methods: {
    logout() {
      // Clear the JWT token from localStorage
      localStorage.removeItem("access_token");
      
      // Redirect the user to '/'
      this.$router.push("/");
    }
  }
}
</script>

<style scoped>
/* Navigation bar styles */
.site-header {
  margin-bottom: 20px; /* Add spacing below the navigation bar */
}

.navbar-brand {
  font-size: 1.25rem; /* Increase font size */
  font-weight: bold; /* Make text bold */
}

.navbar-nav .nav-link {
  color: #007bff; /* Link color */
  padding-right: 15px; /* Add spacing between links */
}

.navbar-nav .nav-link.active {
  color: #000; /* Change active link color */
}

.navbar-nav .nav-link.disabled {
  color: #6c757d; /* Change disabled link color */
}
</style>
