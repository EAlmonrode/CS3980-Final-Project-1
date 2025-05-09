<template>
  <div>
    <h2>Sign Up</h2>
    <form @submit.prevent="handleSignUp">
      <input v-model="username" placeholder="Username" />
      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Sign Up</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
    <p v-if="success" style="color: green;">{{ success }}</p>
    <p>
      Login to your account?
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const username = ref('');
const email = ref('');
const password = ref('');
const error = ref('');
const success = ref('');

const handleSignUp = async () => {
  error.value = '';
  success.value = '';
  try {
    await axios.post('http://localhost:8000/users/signup', {
      username: username.value,
      email: email.value,
      password: password.value,
    });
    success.value = 'Sign-up successful! You can now log in.';
  } catch (err) {
    error.value = err.response?.data?.detail || 'Sign-up failed.';
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