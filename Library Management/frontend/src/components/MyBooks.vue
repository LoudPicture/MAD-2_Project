<template>
  <UserLayout>
    <div>
      <h3>All My Books</h3>
      <div v-if="grantedBooks.length > 0">
        <div v-for="book in grantedBooks" :key="book.id" class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">{{ book.book.name }}</h5>
            <p class="card-text">Author: {{ book.book.authors }}</p>
            <p class="card-text">Section: {{ book.book.section.name }}</p>
            <div>
              <a href="#" @click="toggleContent(book)" class="content-link">{{ book.showContent ? 'Hide Content' : 'Show Content' }}</a>
            </div>
            <div v-if="book.showContent" class="book-content">
              <p>{{ book.book.content }}</p>
            </div>
            <button class="btn btn-primary" @click="reviewBook(book.id)">Review</button>
            <button class="btn btn-danger" @click="returnBook(book.id)">Return</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No books granted.</p>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/User_layout.vue';

export default {
  name: 'MyBooks',
  components: {
    UserLayout,
  },
  data() {
    return {
      grantedBooks: [],
    };
  },
  mounted() {
    this.fetchMyBooks();
  },
  methods: {
    async fetchMyBooks() {
      try {
        const response = await fetch('http://127.0.0.1:5001/user/mybooks', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.grantedBooks = data.grantedBooks.map(book => ({
            ...book,
            showContent: false,
          }));
        } else {
          console.error('Failed to fetch granted books');
        }
      } catch (error) {
        console.error('Error fetching granted books:', error);
      }
    },
    reviewBook(bookId) {
  console.log('Review book with ID:', bookId);
  this.$router.push({ name: 'BookReview', params: { bookId } });
},
    async returnBook(bookId) {
  console.log('Return book with ID:', bookId);
  try {
    const response = await fetch(`http://127.0.0.1:5001/user/mybooks/${bookId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (response.ok) {
      // Remove the returned book from the grantedBooks array
      this.grantedBooks = this.grantedBooks.filter(book => book.id !== bookId);
    } else {
      console.error('Failed to return the book');
    }
  } catch (error) {
    console.error('Error returning the book:', error);
  }
},

    toggleContent(book) {
      book.showContent = !book.showContent;
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
