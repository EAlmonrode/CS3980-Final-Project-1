<template>
    <nav v-if="auth.token">
      <div class="logo">📝 NoteShare</div>
      <router-link to="/notes">Notes</router-link>
        <router-link to="/groups">Groups</router-link>
        <router-link to="/admin">Admin</router-link>
      <a href="#" @click.prevent="logout">Logout</a>
    </nav>
</template>
  
  <script setup>
  import { useAuthStore } from '../stores/auth';
  import { useRouter } from 'vue-router';
  
  const auth = useAuthStore();
  const router = useRouter();
  
  const logout = () => {
    auth.logout();
    router.push('/login');
  };
  </script>

<style scoped>
nav {
  background-color: #121212;
  padding: 1em;
  display: flex;
  gap: 1em;
  border-bottom: 1px solid #333;
}

a {
  color: #90caf9;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
  