import { createRouter, createWebHistory } from 'vue-router';
import Index from '@/components/Index.vue';
import User from '@/components/User.vue';
import Signup from '@/components/Signup.vue';
import UserPage from '@/components/UserPage.vue';
import UserHome from '@/components/UserHome.vue';
import AdminPage from '@/components/AdminPage.vue';
import AdminHome from '@/components/AdminHome.vue';
import InsideSection from '@/components/InsideSection.vue';
import AddBook from '@/components/AddBook.vue';
import BookUpdateForm from '@/components/BookUpdateForm.vue';
import AdminDashBoard from '@/components/AdminDashBoard.vue';
import MyBooks from '@/components/MyBooks.vue';
import BookReview from '@/components/BookReview.vue';
import BookReviewList from '@/components/BookReviewList.vue';
import SearchResults from '@/components/SearchResults.vue';


const routes = [
    { path: '/', component: Index },
    { path: '/user', component: User },
    { path: '/signup', component: Signup },
    { path: '/userlogin', component: UserPage },
    { path: '/user/home', component: UserHome },
    { path: '/user/books', component: UserHome },
    { path: '/adminlogin', component: AdminPage },
    { path: '/admin/home', component: AdminHome },
    { path: '/admin/home/:section_id', component: AdminHome }, // Dynamic segment
    { path: '/sections/:section_id', component: InsideSection }, // Dynamic segment
    { path: '/sections/:section_id/add_book', name: 'AddBook', component: AddBook }, // Dynamic segment
    { path: '/books/:book_id/update', name: 'BookUpdateForm', component: BookUpdateForm, props: true }, // Dynamic segment
    { path: '/books/:book_id/delete', component: InsideSection }, // Dynamic segment
    { path: '/admin_dashboard/book_requests', component: AdminDashBoard },
    { path: '/admin_dashboard/granted_books', component: AdminDashBoard },
    { path: '/admin_dashboard/grant_book', component: AdminDashBoard },
    { path: '/admin_dashboard/reject_book', component: AdminDashBoard },
    { path: '/admin_dashboard', component: AdminDashBoard },
    { path: '/user/mybooks', component: MyBooks },
    { path: '/user/mybooks/:book_id', component: MyBooks },
    { path: '/review/:bookId', name: 'BookReview', component: BookReview },
    { path: '/book/:bookId/reviews', name: 'BookReviewList', component: BookReviewList },
    { path: '/user/search-books/:searchTerm', name: 'SearchResults', component: SearchResults, props: true },
    
    // Add other routes as needed
];


const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
