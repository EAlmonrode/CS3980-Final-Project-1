<template>
  <div class="notes-container">
    <h2>Your Notes</h2>

    <button @click="showModal = true">Add Note</button>

    <!-- Modal -->
<div v-if="showModal" class="modal-overlay">
  <div class="modal-content">
    <h3>Create Note</h3>
    <form @submit.prevent="addNote" class="modal-form">
      <input v-model="newNote.name" placeholder="Note name" required />
      <textarea v-model="newNote.description" placeholder="Description" required></textarea>

      <select v-model="selectedGroup" required>
        <option disabled value="">Select Group</option>
        <option v-for="group in groups" :value="group._id" :key="group._id">
          {{ group.name }}
        </option>
      </select>

      <input type="file" @change="handleFileUpload" />

      <div class="modal-buttons">
        <button type="submit">Submit</button>
        <button type="button" @click="showModal = false">Cancel</button>
      </div>
    </form>
  </div>
</div>


    <div v-for="group in groupedNotes" :key="group._id" class="group-section">
      <button class="group-toggle" @click="toggleGroup(group._id)">
        {{ group.name }}
      </button>
      <ul v-if="!collapsedGroups.includes(group._id)">
        <li v-for="note in group.notes" :key="note._id">
          {{ note.name }} - {{ note.description }}
          <img
            v-if="note.image_data"
            :src="`data:image/png;base64,${note.image_data}`"
            alt="Note image"
            style="max-width: 300px; margin-top: 0.5em; border-radius: 8px;"
          />
          <a
            v-if="note.image_data"
            :href="`data:image/png;base64,${note.image_data}`"
            :download="`${note.name.replace(/\s+/g, '_') || 'note'}.png`"
            style="display: inline-block; margin-top: 0.5em; color: #90caf9;"
          >
            Download Image
          </a>
          <button @click="deleteNote(note.id)" style="margin-left: 0.5em; color: red;">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const notes = ref([]);
const groups = ref([]);
const showModal = ref(false);
const newNote = ref({ name: '', description: '' });
const selectedGroup = ref('');
const file = ref(null);
const collapsedGroups = ref([]);

const fetchNotes = async () => {
  const res = await axios.get('http://localhost:8000/notes/my', {
    headers: { Authorization: `Bearer ${auth.token}` },
  });
  notes.value = res.data;
};

const fetchGroups = async () => {
  const res = await axios.get('http://localhost:8000/groups/my', {
    headers: { Authorization: `Bearer ${auth.token}` },
  });
  groups.value = res.data;
};

const groupedNotes = computed(() => {
  return groups.value.map(group => ({
    ...group,
    notes: notes.value.filter(note => note.group_id === group._id)
  }));
});

const toggleGroup = (groupId) => {
  if (collapsedGroups.value.includes(groupId)) {
    collapsedGroups.value = collapsedGroups.value.filter(id => id !== groupId);
  } else {
    collapsedGroups.value.push(groupId);
  }
};

const handleFileUpload = (e) => {
  file.value = e.target.files[0];
};

const addNote = async () => {
  const formData = new FormData();
  formData.append('name', newNote.value.name);
  formData.append('description', newNote.value.description);
  if (selectedGroup.value) formData.append('group_id', selectedGroup.value);
  if (file.value) formData.append('file', file.value);

  await axios.post('http://localhost:8000/notes', formData, {
    headers: {
      Authorization: `Bearer ${auth.token}`,
      'Content-Type': 'multipart/form-data',
    },
  });

  newNote.value = { name: '', description: '' };
  selectedGroup.value = '';
  file.value = null;
  showModal.value = false;
  await fetchNotes();
};

const deleteNote = async (noteId) => {
  if (confirm('Are you sure you want to delete this note?')) {
    await axios.delete(`http://localhost:8000/notes/${noteId}`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    await fetchNotes();
  }
};

onMounted(() => {
  fetchNotes();
  fetchGroups();
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #1e1e1e;
  padding: 2em;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  color: #fff;
}

.modal-content h3 {
  margin-bottom: 1em;
  color: #90caf9;
}

.modal-form input,
.modal-form textarea,
.modal-form select {
  width: 100%;
  margin-bottom: 1em;
  padding: 0.5em;
  border-radius: 4px;
  border: none;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1em;
}

.notes-container {
  padding: 1em;
}
.group-section {
  margin-bottom: 1.5em;
}
.group-toggle {
  background: #333;
  color: #fff;
  padding: 0.5em 1em;
  border: none;
  margin-bottom: 0.5em;
  cursor: pointer;
}
.note-image {
  display: block;
  max-width: 300px;
  margin-top: 0.5em;
}
</style>


