<template>
  <AdminLayout>
    <div>
      <form @submit.prevent="searchBooks" class="input-group">
        <input v-model="searchTerm" type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon">
        <button type="submit" class="btn btn-outline-primary">Search</button>
      </form>

      <!-- Display search results -->
      <div v-if="searchResults.length > 0">
        <div v-for="(book, index) in searchResults" :key="book.id" class="book-item">
          <div>{{ index + 1 }}. Book Name : {{ book.name }}</div>
          <div>Book Author : {{ book.authors }}</div>
          <div>
            <a href="#" @click="toggleContent(book)" class="content-link">{{ book.showContent ? 'Hide Content' : 'Content' }}</a>
          </div>
          <div v-if="book.showContent" class="book-content">
            <p>{{ book.content }}</p>
          </div>
          <div class="book-actions">
            <button @click="showUpdateForm(book)" class="btn btn-primary">Update</button>
            <button @click="confirmDeleteBook(book.id)" class="btn btn-danger">Delete</button>
          </div>
          <!-- Add other book details as needed -->
        </div>
      </div>

      <div v-else>
        <p v-if="searchTerm">No books found.</p>
      </div>

      <br>

      <button @click="toggleSectionForm">Add Sections</button>

      <div v-if="showSectionForm" id="sectionForm">
        <span @click="toggleSectionForm" class="close">&times;</span>
        <h3>Add New Section</h3>
        <form @submit.prevent="addSection">
          <label for="sectionName">Section Name:</label>
          <input v-model="sectionName" type="text" id="sectionName" required>
          <button type="submit">Submit</button>
        </form>
      </div>

      <br>
      <br>

      <div v-for="section in sections" :key="section.id" class="section-item">
        <a :href="'/sections/' + section.id">{{ section.name }}</a>
        <div class="section-actions">
          <button @click="showUpdateFormSection(section)" class="btn btn-primary">Update</button>
          <button @click="confirmDeleteSection(section.id)" class="btn btn-danger">Delete</button>
        </div>
      </div>

      <div id="update-form" v-if="showUpdateFormFlag">
        <h3>Update Section</h3>
        <form @submit.prevent="updateSection">
          <label for="updatedSectionName">Updated Section Name:</label>
          <input v-model="updatedSectionName" type="text" id="updatedSectionName" required>
          <button type="submit">Update Section</button>
        </form>
      </div>

      <!-- BookUpdateForm component -->
      <BookUpdateForm v-if="selectedBook" :bookData="selectedBook" @update-book="handleUpdateBook" />
    </div>
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
      searchTerm: '',
      showSectionForm: false,
      sectionName: '',
      sections: [],
      showUpdateFormFlag: false,
      updatedSectionName: '',
      sectionIdToUpdate: null,
      searchResults: [], // Added property to store search results
      selectedBook: null // Selected book for update
    };
  },
  mounted() {
    this.fetchSections();
  },
  methods: {
    fetchSections() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found');
        return;
      }

      fetch('http://127.0.0.1:5001/admin/home', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${access_token}`,
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch sections');
        }
        return response.json();
      })
      .then(data => {
        this.sections = data.sections;
      })
      .catch(error => {
        console.error('Error fetching sections:', error);
      });
    },
    searchBooks() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found');
        return;
      }

      fetch('http://127.0.0.1:5001/admin/home', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${access_token}`,
        },
        body: JSON.stringify({ search_term: this.searchTerm })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to search books');
        }
        return response.json();
      })
      .then(data => {
        this.searchResults = data.books;
      })
      .catch(error => {
        console.error('Error searching books:', error);
      });
    },
    toggleSectionForm() {
      this.showSectionForm = !this.showSectionForm;
    },
    addSection() {
      fetch('http://127.0.0.1:5001/admin/home', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({ sectionName: this.sectionName })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to add section');
        }
        return response.json();
      })
      .then(data => {
        console.log(data.message);
        this.fetchSections();
        this.sectionName = ''; // Clear input field
      })
      .catch(error => {
        console.error('Error adding section:', error);
      });
    },
    showUpdateForm(book) {
      // Set the selected book for update
      this.selectedBook = book;
    },
    showUpdateFormSection(section) {
      // Set section ID and show the update form
      this.sectionIdToUpdate = section.id;
      this.showUpdateFormFlag = true;
    },
    updateSection() {
      // Get access token
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        console.error('Access token not found');
        return;
      }

      // Get updated section name
      const updatedSectionName = this.updatedSectionName.trim();
      if (!updatedSectionName) {
        console.error('Updated section name cannot be empty');
        return;
      }

      // Send PUT request to update section
      fetch(`http://127.0.0.1:5001/admin/home/${this.sectionIdToUpdate}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${access_token}`,
        },
        body: JSON.stringify({ sectionName: updatedSectionName })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to update section');
        }
        return response.json();
      })
      .then(data => {
        console.log(data.message);
        this.fetchSections(); // Refresh the sections list after update
        this.showUpdateFormFlag = false; // Hide update form after update
        this.updatedSectionName = ''; // Clear input field
      })
      .catch(error => {
        console.error('Error updating section:', error);
      });
    },
    confirmDeleteBook(bookId) {
      if (confirm("Are you sure you want to delete this book?")) {
        fetch(`http://127.0.0.1:5001/books/${bookId}/delete`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          }
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to delete book');
          }
          return response.json();
        })
        .then(data => {
          console.log(data.message);
          this.searchBooks(); // Refresh the search results after deletion
        })
        .catch(error => {
          console.error('Error deleting book:', error);
        });
      }
    },
    confirmDeleteSection(sectionId) {
      if (confirm("Are you sure you want to delete this section?")) {
        fetch(`http://127.0.0.1:5001/admin/home/${sectionId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          }
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to delete section');
          }
          return response.json();
        })
        .then(data => {
          console.log(data.message);
          this.fetchSections(); // Refresh the sections list after deletion
        })
        .catch(error => {
          console.error('Error deleting section:', error);
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
        this.searchBooks(); // Refresh the search results after update
      })
      .catch(error => {
        console.error('Error updating book:', error);
      });
    },
  }
};
</script>

<style>
/* Add your styles here */
</style>
