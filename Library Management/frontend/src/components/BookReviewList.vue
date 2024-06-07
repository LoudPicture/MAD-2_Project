<template>
<UserLayout>
  <div>
    <h2>{{ book.name }} Reviews</h2>
    <div v-if="reviews.length > 0">
      <div v-for="review in reviews" :key="review.id">
      <p>User : {{ review.user_id }}</p>
        <p>Rating: {{ review.rating }}</p>
        <p>Comment: {{ review.comment }}</p>
        <hr>
      </div>
    </div>
    <div v-else>
      <p>No reviews found for this book.</p>
    </div>
  </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/User_layout.vue';
export default {
  name: 'BookReviewList',
  components: {
    UserLayout,
  },
  data() {
    return {
      book: {},
      reviews: []
    };
  },
  mounted() {
    // Fetch book details and reviews on component mount
    this.fetchBookAndReviews();
  },
  methods: {
    async fetchBookAndReviews() {
      try {

        // Fetch reviews for the book
        const reviewsResponse = await fetch(`http://127.0.0.1:5001/book/${this.$route.params.bookId}/reviews`);
        if (reviewsResponse.ok) {
          this.reviews = await reviewsResponse.json();
        } else {
          console.error('Failed to fetch reviews for the book');
        }
      } catch (error) {
        console.error('Error fetching book and reviews:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
