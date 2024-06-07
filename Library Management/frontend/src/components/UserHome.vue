<template>
  <UserLayout>
    <div>
      <h3 class="text-center">Welcome {{ username }}</h3>
      
      <!-- Search bar -->
      <form @submit.prevent="searchBooks" class="input-group mb-3">
        <input v-model="searchTerm" type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon">
        <button type="submit" class="btn btn-outline-primary">Search</button>
      </form>

      <!-- Display all books -->
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
                <button @click="requestBook(book.id)" class="btn btn-primary" v-if="canRequestBook">Request</button>
            </div>
            <!-- Show reviews button -->
              <button @click="viewReviews(book.id)" class="btn btn-secondary ml-2">Reviews</button> 
          </div>
        </div>
      </div>
      <div v-else>
        <p>No books found.</p>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/User_layout.vue';

export default {
  name: 'UserHome',
  components: {
    UserLayout,
  },
  data() {
    return {
      username: '',
      searchTerm: '',
      books: [],
      requestedBooks: [],
    };
  },
  computed: {
    // Compute whether the user can request more books
    canRequestBook() {
      return this.requestedBooks.length < 5;
    }
  },
  mounted() {
    this.fetchUserData();
    this.fetchBooks();
  },
  methods: {
    async fetchUserData() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        this.$router.push('/userlogin');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5001/user/home', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${access_token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.result) {
            this.username = data.result;
          } else {
            this.$router.push('/userlogin');
          }
        } else {
          this.$router.push('/userlogin');
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        this.$router.push('/userlogin');
      }
    },
    async fetchBooks() {
      try {
        const response = await fetch('http://127.0.0.1:5001/user/books', {
          method: 'GET',
        });
        if (response.ok) {
          const data = await response.json();
          this.books = data.books;
        } else {
          console.error('Failed to fetch books');
        }
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async searchBooks() {
  console.log('Search term:', this.searchTerm);
  try {
    const response = await fetch(`http://127.0.0.1:5001/user/search-books?search=${this.searchTerm}`, {
      method: 'GET',
    });
    if (response.ok) {
      const data = await response.json();
      // Redirect to search results page with search term and results
      this.$router.push({ name: 'SearchResults', params: { searchTerm: this.searchTerm, searchResults: data.books } });
    } else {
      console.error('Failed to search books');
    }
  } catch (error) {
    console.error('Error searching books:', error);
  }
},

    async requestBook(bookId) {
      if (!this.canRequestBook) {
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
    isBookRequested(bookId) {
      return this.requestedBooks.includes(bookId);
    },
    viewReviews(bookId) {
      // Redirect to the reviews route for the selected book
      this.$router.push({ name: 'BookReviewList', params: { bookId: bookId } });
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
