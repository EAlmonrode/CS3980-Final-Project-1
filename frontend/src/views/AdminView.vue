<template>
  <div class="admin-view">
    <h2>Admin Dashboard</h2>

    <div v-if="loading">Loading...</div>

    <div v-else-if="notAdmin">
      <p style="color: red;">Access denied. Admins only.</p>
    </div>

    <div v-else>
      <div>
        <h3>Users</h3>
        <ul>
          <li v-for="user in users" :key="user._id">{{ user.username }} ({{ user.email }})</li>
        </ul>
      </div>

      <div>
        <h3>Groups</h3>
        <ul>
          <li v-for="group in groups" :key="group._id">{{ group.name }} (Owner: {{ group.owner }})</li>
        </ul>
      </div>

      <div>
        <h3>Notes</h3>
        <ul>
          <li v-for="note in notes" :key="note._id">{{ note.name }} - {{ note.description }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const users = ref([]);
const groups = ref([]);
const notes = ref([]);
const notAdmin = ref(false);
const loading = ref(true);

onMounted(async () => {
  try {
    loading.value = true;

    await auth.fetchUser();

    if (!auth.user || !auth.user.is_admin) {
      notAdmin.value = true;
      console.warn("User is not admin");
      return;
    }

    const headers = { Authorization: `Bearer ${auth.token}` };

    const [u, g, n] = await Promise.all([
      axios.get('http://localhost:8000/admin/users', { headers }),
      axios.get('http://localhost:8000/admin/groups', { headers }),
      axios.get('http://localhost:8000/admin/notes', { headers }),
    ]);

    users.value = u.data;
    groups.value = g.data;
    notes.value = n.data;
  } catch (e) {
    console.error('Failed to fetch admin data:', e);
  } finally {
    loading.value = false;
  }
});

</script>
