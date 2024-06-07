<template>
  <div class="login-container">
    <h3>Enter Login Credentials</h3>

    <form @submit.prevent="submitForm" class="login-form">
      <div class="form-group">
        <label for="uname">Username:</label>
        <br>
        <input type="text" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="pass">Password:</label>
        <br>
        <input type="password" v-model="password" required>
      </div>
      <div class="text-center">
        <input type="submit" value="Submit" class="submit-button">
      </div>
    </form>
    <p>Don't have an account? <router-link to="/signup">Sign up here</router-link></p>

    <!-- Display error message if login fails -->
    <template v-if="message">
      <p id="error" class="error-message">{{ message }}</p>
    </template>
  </div>
</template>

<script>
export default {
  name: 'UserPage',
  data() {
    return {
      username: '',
      password: '',
      message: '',
    };
  },
  methods: {
    async submitForm() {
      // Handle form submission logic here
      try {
        const response = await fetch('http://127.0.0.1:5001/userlogin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password, 
          }),
        });

        
        if (response.ok) {
          const data = await response.json();
          // Login successful, show message and navigate to user dashboard
          if (data.message === 'Login successful') {
            // Login successful, show success message
            this.message = data.message;

            // Store the JWT token in localStorage
            localStorage.setItem('access_token', data.access_token);

            // Redirect to the next page or user dashboard on successful login
            this.$router.push('/user/home');
          }
          else{
            this.message = 'Failed to login. Please try again.';
          }
        } else {
          // Login failed, show error message
          this.message = 'Failed to login. Please try again.';
        }
      } catch (error) {
        // Handle any network errors or exceptions
        this.message = 'Failed to login. Please try again.';
        console.error('Error:', error);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-size: 16px;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="password"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 70%;
}

.text-center {
  text-align: center;
}

.submit-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #0056b3;
}

p {
  font-size: 16px;
  color: #555;
  margin-top: 10px;
}

.error-message {
  color: #ff0000;
}

</style>
