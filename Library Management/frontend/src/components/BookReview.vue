<template>
<UserLayout>
  <div>
    <h3>Review Book</h3>
    <form @submit.prevent="submitReview">
      <div class="form-group">
        <label for="rating">Rating (1-5)</label>
        <select id="rating" v-model="rating" class="form-control" required>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </div>
      <div class="form-group">
        <label for="opinion">Opinion</label>
        <textarea id="opinion" v-model="opinion" class="form-control" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/User_layout.vue';
export default {
    components: {
    UserLayout,
  },
  data() {
    return {
      rating: null,
      opinion: ''
    };
  },
  methods: {
    async submitReview() {
  try {
    // Log the data being sent in the POST request
    console.log('Data being sent:', {
      book_id: this.$route.params.bookId,
      rating: this.rating,
      comment: this.opinion
    });

    const response = await fetch('http://127.0.0.1:5001/feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        book_id: this.$route.params.bookId,
        rating: this.rating,
        comment: this.opinion
      })
    });

    if (response.ok) {
      // Handle successful submission (e.g., show a success message)
      console.log('Review submitted successfully');
      
      // Redirect to the user home page
      this.$router.push('/user/home');
    } else {
      console.error('Failed to submit review');
    }
  } catch (error) {
    console.error('Error submitting review:', error);
  }
}

  }
};
</script>
