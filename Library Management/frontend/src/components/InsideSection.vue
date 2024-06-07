<template>
  <AdminLayout>
    <div>
      <h1>{{ section_name }}</h1>
      <div class="book-list">
        <div v-for="(book, index) in books" :key="book.id" class="book-item">
          <div>{{ index + 1 }}. Book Name: {{ book.name }}</div>
          <div>Book Author: {{ book.authors }}</div>
          <div>
            <a href="#" @click="toggleContent(book)" class="content-link">{{ book.showContent ? 'Hide Content' : 'Content' }}</a>
          </div>
          <div v-if="book.showContent" class="book-content">
            <p>{{ book.content }}</p>
          </div>
          <div class="book-actions">
            <!-- Pass the entire book object as an argument to the updateBook method -->
            <button @click="updateBook(book)" class="btn btn-primary">Update</button>
            <button @click="confirmDelete(book.id)" class="btn btn-danger">Delete</button>
          </div>
          <br>
        </div>
      </div>
      <br>
      <router-link :to="{ name: 'AddBook' }" class="btn btn-primary">Add Book</router-link>
    </div>

    <!-- BookUpdateForm component to handle book updates -->
    <BookUpdateForm v-if="selectedBook" :bookData="selectedBook" @update-book="handleUpdateBook" />
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/Admin_layout.vue';
import BookUpdateForm from '@/components/BookUpdateForm.vue';

export default {
  components: {
    AdminLayout,
    BookUpdateForm
  },
  data() {
    return {
      section_name: '',
      books: [],
      sectionId: null,
      selectedBook: null // Track the selected book for update
    };
  },
  created() {
    this.sectionId = this.$route.params.section_id;
    this.fetchSection();
  },
  methods: {
    fetchSection() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found');
        return;
      }

      fetch(`http://127.0.0.1:5001/sections/${this.sectionId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${access_token}`,
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch section data');
        }
        return response.json();
      })
      .then(data => {
        this.section_name = data.section_name;
        this.books = data.books.map(book => ({
          ...book,
          showContent: false
        }));
      })
      .catch(error => {
        console.error('Error fetching section:', error);
      });
    },
    updateBook(book) {
      // Set the selected book for update
      this.selectedBook = book;
    },
    confirmDelete(bookId) {
      if (confirm("Are you sure you want to delete this book?")) {
        fetch(`http://127.0.0.1:5001/books/${bookId}/delete`, {
          method: 'DELETE'
        })
        .then(response => {
          if (response.ok) {
            this.fetchSection();
          } else {
            throw new Error('Failed to delete book');
          }
        })
        .catch(error => {
          console.error('Error deleting book:', error);
        });
      }
    },
    toggleContent(book) {
      book.showContent = !book.showContent;
    },
    // Method to handle update-book event emitted by BookUpdateForm
    handleUpdateBook(updatedBookData) {
      const bookId = updatedBookData.id;
      fetch(`http://127.0.0.1:5001/books/${bookId}/update`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedBookData)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to update book');
        }
        // Reset selectedBook and fetch updated data
        this.selectedBook = null;
        this.fetchSection();
      })
      .catch(error => {
        console.error('Error updating book:', error);
      });
    }
  }
};
</script>

<style>
/* Add your styles here */
.book-content {
  margin-top: 10px;
}
.content-link {
  cursor: pointer;
}
</style>
