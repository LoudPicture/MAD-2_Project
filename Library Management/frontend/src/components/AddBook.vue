<template>
  <AdminLayout>
    <h1>Add Book</h1>
    <form @submit.prevent="addBook">
      <div class="form-group">
        <label for="book_name">Book Name:</label>
        <input type="text" class="form-control" v-model="bookName" id="book_name" required>
      </div>
      <div class="form-group">
        <label for="author">Author:</label>
        <input type="text" class="form-control" v-model="authorName" id="author" required>
      </div>
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea class="form-control" v-model="content" id="content" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Add Book</button>
    </form>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/Admin_layout.vue';
import axios from 'axios';

export default {
  name: 'AddBook',
  components: {
    AdminLayout
  },
  data() {
    return {
      bookName: '',
      authorName: '',
      content: ''
    };
  },
  methods: {
    async addBook() {
      try {
        const response = await axios.post(`http://127.0.0.1:5001/sections/${this.$route.params.section_id}/add_book`, {
          name: this.bookName,
          authors: this.authorName,
          content: this.content
          // You may need to include other book details here as required by your backend
        });
        console.log('Book added successfully:', response.data);
        // Optionally, you can redirect to a different page after successfully adding the book
        // Replace '/admin/home' with the desired route
        this.$router.push('/admin/home');
      } catch (error) {
        console.error('Error adding book:', error);
        // Handle error (e.g., show an error message to the user)
      }
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
