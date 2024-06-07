<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h5 class="mt-4 mb-3">Enter Login Credentials</h5>

        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="uname">Username:</label>
            <input type="text" class="form-control" v-model="username" required>
          </div>
          <div class="form-group">
            <label for="pass">Password:</label>
            <input type="password" class="form-control" v-model="password" required>
          </div>
          <br><br><br><br>
          <div class="text-center">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </form>

        <!-- Display error message if login fails -->
        <template v-if="message">
          <p class="text-danger mt-3">{{ message }}</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminPage',
  data() {
    return {
      username: '',
      password: '',
      message: '',
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://127.0.0.1:5001/adminlogin', {
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
          if (data.message === 'Login successful') {
            this.message = data.message;
            localStorage.setItem('access_token', data.access_token);
            this.$router.push('/admin/home');
          } else {
            this.message = 'Failed to login. Please try again.';
          }
        } else {
          this.message = 'Failed to login. Please try again.';
        }
      } catch (error) {
        this.message = 'Failed to login. Please try again.';
        console.error('Error:', error);
      }
    },
  },
};
</script>
