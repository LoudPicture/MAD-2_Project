<template>
  <div class="signup-container">
    <h3>Create an Account</h3>

    <form @submit.prevent="submitForm" class="signup-form">
      <label for="uname">Username:</label>
      <input id="uname" type="text" v-model="username" required>
      <br>
      <label for="email">Email:</label>
      <input id="email" type="text" v-model="email" required>
      <br>
      <label for="pass">Password:</label>
      <input id="pass" type="password" v-model="password" required>
      <br>
      <div class="text-center">
        <input id="sub" type="submit" value="Sign up" class="signup-button">
      </div>
    </form>

    <!-- Display success or error message after signup attempt -->
    <p v-if="message" class="signup-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      message: '',
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('http://127.0.0.1:5001/signup', {
          username: this.username,
          password: this.password,
          email: this.email,
        });

        if (response.data.message === 'SignUp successful') {
          this.$router.push('/userlogin');
        } else {
          this.message = 'Failed to sign up. Please try again.';
        }
      } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          this.message = error.response.data.error;
        } else {
          this.message = 'An error occurred during signup. Please try again.';
        }
      }
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
.signup-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.signup-form label {
  margin-bottom: 5px;
}

.signup-form input[type="text"],
.signup-form input[type="password"] {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 80px;
  width: 70%; 
}

.signup-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.signup-message {
  margin-top: 10px;
  font-size: 14px;
  color: red;
}
</style>
