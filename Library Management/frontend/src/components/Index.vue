<template>
  <div class="border-for-index">
    <h1 class="big-heading">
      <router-link to="/">LibraryPro</router-link>
    </h1>
    <div>
      <br><br><br><br>
    </div>
    <div class="d-flex justify-content-center mt-12">
      <router-link class="bigger-button" to="/adminlogin">Librarian</router-link>
    </div>
    <div>
      <br><br><br><br>
    </div>
    <div class="d-flex justify-content-center mt-12">
      <router-link class="bigger-button" to="/user">User</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeIndex',
}
</script>

<style scoped>
/* Style for the container */
.border-for-index {
  text-align: center;
}

/* Style for the big heading */
.big-heading {
  font-size: 2.5rem;
  color: #333;
}

/* Style for the bigger button */
.bigger-button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 1.2rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.bigger-button:hover {
  background-color: #0056b3;
}
</style>
