<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Log In</button>
    </form>
    <p>
      Don’t have an account?
      <router-link to="/signup">Sign up</router-link>
    </p>

    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const username = ref('');
const password = ref('');
const error = ref('');
const auth = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  try {
    await auth.login(username.value, password.value);
    router.push('/notes');
  } catch (e) {
    error.value = e.message || 'Login failed.';
  }
};
</script>

<style scoped>
div {
  padding: 1em;
}

h2 {
  color: #90caf9;
}
</style>
