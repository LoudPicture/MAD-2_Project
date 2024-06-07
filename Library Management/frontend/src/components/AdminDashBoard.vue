<template>
  <AdminLayout>
    <div>
      <h3>Admin Dashboard</h3>
      <div v-if="bookRequests.length === 0">
        <p>No book requests available.</p>
      </div>
      <div v-else>
        <div class="dashboard-container">
          <!-- Left half: User requests -->
          <div class="left-half">
            <h4>User Requests</h4>
            <div class="card-container">
              <div class="card" v-for="(request, index) in bookRequests" :key="index">
                <div class="card-content">
                  <p><strong>User ID:</strong> {{ request.user.id }}</p>
                  <p><strong>Username:</strong> {{ request.user.username }}</p>
                  <p><strong>Book Name:</strong> {{ request.book.name }}</p>
                </div>
                <div class="button-container">
                  <button class="grant-button" @click="grantBook(request.id)">Grant</button>
                  <button class="reject-button" @click="rejectBook(request.id)">Reject</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Right half: Granted books -->
      <div class="right-half">
        <h4>Granted Books</h4>
        <div class="card-container">
          <div class="card" v-for="(book, index) in grantedBooks" :key="index">
            <div class="card-content">
              <p><strong>User ID:</strong> {{ book.user.id }}</p>
              <p><strong>Username:</strong> {{ book.user.username }}</p>
              <p><strong>Book Name:</strong> {{ book.book.name }}</p>
            </div>
            <div class="button-container">
              <button class="revoke-button" @click="revokeBook(book.id)">Revoke</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>


<script>
import AdminLayout from '@/components/Admin_layout.vue';
import axios from 'axios';

export default {
  components: {
    AdminLayout
  },
  data() {
    return {
      bookRequests: [],
      grantedBooks: []
    };
  },
  created() {
    this.fetchBookRequests();
    this.fetchGrantedBooks();
  },
  methods: {
    fetchBookRequests() {
      const token = localStorage.getItem('access_token');
      axios.get('http://127.0.0.1:5001/admin_dashboard', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        this.bookRequests = response.data.book_requests;
      })
      .catch(error => {
        console.error('Error fetching book requests:', error);
      });
    },
    fetchGrantedBooks() {
      const token = localStorage.getItem('access_token');
      axios.get('http://127.0.0.1:5001/admin_dashboard/granted_books', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        this.grantedBooks = response.data.granted_books;
      })
      .catch(error => {
        console.error('Error fetching granted books:', error);
      });
    },
    grantBook(requestId) {
      const token = localStorage.getItem('access_token');
      axios.post('http://127.0.0.1:5001/admin_dashboard/grant_book', { action: 'grant', request_id: requestId }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        // Refresh book requests and granted books
        this.fetchBookRequests();
        this.fetchGrantedBooks();
      })
      .catch(error => {
        console.error('Error granting book:', error);
      });
    },
    rejectBook(requestId) {
      const token = localStorage.getItem('access_token');
      axios.post('http://127.0.0.1:5001/admin_dashboard/reject_book', { action: 'reject', request_id: requestId }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        // Refresh book requests
        this.fetchBookRequests();
      })
      .catch(error => {
        console.error('Error rejecting book:', error);
      });
    },
    revokeBook(grantedBook) {
      console.log('Request Data:', grantedBook);
      const token = localStorage.getItem('access_token');
      axios.post('http://127.0.0.1:5001/admin_dashboard/revoke_book', { action: 'revoke', granted_book_id: grantedBook }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    
    })
  .then(() => {
    // Refresh granted books
    this.fetchGrantedBooks();
  })
  .catch(error => {
    console.error('Error revoking book:', error);
  });
}

  }
};
</script>
