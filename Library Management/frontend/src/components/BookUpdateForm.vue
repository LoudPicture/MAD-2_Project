<template>
  <div class="update-form-container">
    <h2>Update Book</h2>
    <form @submit.prevent="submitForm" class="update-form">
      <div class="form-group">
        <label for="name">Book Name:</label>
        <input type="text" id="name" v-model="localBookData.name" required>
      </div>
      <div class="form-group">
        <label for="authors">Authors:</label>
        <input type="text" id="authors" v-model="localBookData.authors" required>
      </div>
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea id="content" v-model="localBookData.content" required></textarea>
      </div>
      <button type="submit" class="btn-submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    bookData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localBookData: { ...this.bookData }
    };
  },
  methods: {
    submitForm() {
      this.$emit('update-book', this.localBookData);
    }
  }
};
</script>

<style scoped>
.update-form-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.update-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}
</style>
