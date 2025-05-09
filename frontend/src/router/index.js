import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import NotesView from '../views/NotesView.vue';
import SignUpView from '../views/SignUpView.vue';
import GroupView from '../views/GroupView.vue';
import AdminView from '../views/AdminView.vue';
import { useAuthStore } from '../stores/auth';


const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/notes', name: 'notes', component: NotesView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/groups', name: 'groups', component: GroupView },
  { path: '/admin', name: 'AdminView', component: AdminView, meta: { requiresAuth: true, requiresAdmin: true }}
  
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();
  console.log('Route:', to.path, '| Auth token:', auth.token);

  if (to.meta.requiresAuth && !auth.token) {
    console.warn('Blocked - No token');
    return next('/login');
  }

  next();
});



export default router;
