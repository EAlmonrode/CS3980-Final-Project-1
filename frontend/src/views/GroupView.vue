<template>
    <div>
        <h2>Your Groups</h2>

        <form @submit.prevent="createGroup">
            <input v-model="newGroup" placeholder="Group Name" />
            <button type="submit">Create Group</button>
        </form>

        <ul>
            <li v-for="group in groups" :key="group._id">
            {{ group.name }} (created by {{ group.owner }})
            <button @click="deleteGroup(group._id)">Delete</button>
            </li>
        </ul>

    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const groups = ref([]);
const newGroup = ref('');

const fetchGroups = async () => {
    const res = await axios.get('http://localhost:8000/groups/my', {
        headers: { Authorization: `Bearer ${auth.token}` },
    });
    groups.value = res.data;
};

const createGroup = async () => {
    if (!newGroup.value) return;
    await axios.post('http://localhost:8000/groups', {
        name: newGroup.value,
        description: "optional", // Replace or expand this if needed
    }, {
        headers: {
            Authorization: `Bearer ${auth.token}`,
            'Content-Type': 'application/json'
        }
    });
    newGroup.value = '';
    fetchGroups();
};

const deleteGroup = async (groupId) => {
    if (!groupId) return;  // safety check
    await axios.delete(`http://localhost:8000/groups/${groupId}`, {
        headers: { Authorization: `Bearer ${auth.token}` },
    });
    fetchGroups();  // refresh after deletion
};

onMounted(fetchGroups);
</script>

<style scoped>
div {
  padding: 1em;
}

h2 {
  color: #90caf9;
}
</style>