import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: '',
    user: null
  }),
  actions: {
    async login(username, password) {
      const res = await axios.post('http://localhost:8000/users/sign-in', {
        username,
        password,
      }, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        transformRequest: [(data) => {
          const params = new URLSearchParams();
          for (const key in data) {
            params.append(key, data[key]);
          }
          return params;
        }],
      });

      this.token = res.data.access_token;
      this.username = username;
      localStorage.setItem('token', this.token);
    },

    logout() {
      this.token = '';
      this.username = '';
      localStorage.removeItem('token');
    },
    async fetchUser() {
      if (!this.token) return;
    
      try {
        const res = await axios.get('http://localhost:8000/users/me', {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });
        this.user = res.data; // This will include is_admin
      } catch (err) {
        console.error('Failed to fetch user info:', err);
        this.logout();
      }
    }
    
  },
});