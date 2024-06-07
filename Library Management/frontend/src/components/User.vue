<template>
  <div class="border-for-index">
    <h1 class="big-heading">
      <router-link to="/">LibraryPro</router-link>
    </h1>
    <div>
      <br><br><br><br>
    </div>
    <div class="d-flex justify-content-center mt-12">
      <router-link class="bigger-button" to="/signup">Register</router-link>
    </div>
    <div>
      <br><br><br><br>
    </div>
    <div class="d-flex justify-content-center mt-12">
      <router-link class="bigger-button" to="/userlogin">Login</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserPage',
}
</script>

<style scoped>
.border-for-index {
  text-align: center;
  padding: 20px;
}

.big-heading {
  font-size: 32px;
  color: #333;
  margin-bottom: 30px;
}

.bigger-button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 18px;
  text-decoration: none;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.bigger-button:hover {
  background-color: #0056b3;
}
</style>
