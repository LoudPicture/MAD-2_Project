<template>
  <UserLayout>
    <div>
      <h3 class="text-center">Search Results</h3>

      <!-- Display search query -->
      <p class="text-center">Search Query: {{ searchTerm }}</p>

      <!-- Display search results -->
      <div v-if="books.length > 0">
        <div v-for="book in books" :key="book.id" class="card mb-3">
          <div class="card-body">
            <!-- Display book information in one line -->
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h5 class="card-title">{{ book.name }}</h5>
                <p class="card-text">Author: {{ book.authors }}</p>
                <p class="card-text">Section: {{ book.section }}</p>
              </div>
              <!-- Show request button or 'Requested' -->
              <button @click="requestBook(book.id)" class="btn btn-primary" v-if="canRequestBook(book.id)">Request</button>
            </div>
            <!-- Show reviews button -->
            <button @click="viewReviews(book.id)" class="btn btn-secondary ml-2">Reviews</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No books found matching the search criteria.</p>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/User_layout.vue';
import axios from 'axios';

export default {
  name: 'SearchResults',
  components: {
    UserLayout,
  },
  props: {
    searchTerm: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      books: [], // Initialize books data property
      requestedBooks: [], // Initialize requestedBooks data property
    };
  },
  methods: {
    async searchBooks() {
      console.log('Search term:', this.searchTerm);
      try {
        const response = await axios.get(`http://127.0.0.1:5001/user/search-books?search=${this.searchTerm}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        if (response.status === 200) {
          // Update the books data property with the search results
          this.books = response.data.books;
        } else {
          console.error('Failed to search books');
        }
      } catch (error) {
        console.error('Error searching books:', error);
      }
    },
    async requestBook(bookId) {
      if (!this.canRequestBook(bookId)) {
        alert("You have already requested 5 books.");
        return;
      }
      
      try {
        const response = await fetch(`http://127.0.0.1:5001/user/request-book/${bookId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          },
        });

        if (response.ok) {
          this.requestedBooks.push(bookId);
        } else if (response.status === 400) {
          const data = await response.json();
          alert(data.error); // Display error message
        } else {
          console.error('Failed to request book:', response.statusText);
        }
      } catch (error) {
        console.error('Error requesting book:', error);
      }
    },
    canRequestBook(bookId) {
      return this.requestedBooks.length < 5 && !this.isBookRequested(bookId);
    },
    isBookRequested(bookId) {
      return this.requestedBooks.includes(bookId);
    },
    viewReviews(bookId) {
      // Redirect to the reviews route for the selected book
      this.$router.push({ name: 'BookReviewList', params: { bookId: bookId } });
    },
  },
  created() {
    // Call the searchBooks method when the component is created
    this.searchBooks();
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
