# Author: Mehak
import streamlit as st
import json
import os

class TaskManager:
    """Class to handle saving and loading tasks to a JSON file."""
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_tasks(self, tasks):
        with open(self.filename, "w") as f:
            json.dump(tasks, f)

# Initialize Task Manager
task_manager = TaskManager()

# Streamlit Page Config
st.set_page_config(page_title="My To-Do App", page_icon="📝")
st.title("📝 Simple To-Do List")

# Load existing tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = task_manager.load_tasks()

# Input area
new_task = st.text_input("Add a new task:", placeholder="What do you need to do?")
if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append({"task": new_task, "completed": False})
        task_manager.save_tasks(st.session_state.tasks)
        st.rerun()
    else:
        st.warning("Please enter a task first!")

# Display tasks
st.subheader("Your Tasks:")
for index, item in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        # Checkbox for completion
        completed = st.checkbox(item["task"], value=item["completed"], key=f"check_{index}")
        if completed != item["completed"]:
            st.session_state.tasks[index]["completed"] = completed
            task_manager.save_tasks(st.session_state.tasks)
            st.rerun()
            
    with col2:
        # Delete button
        if st.button("❌", key=f"del_{index}"):
            st.session_state.tasks.pop(index)
            task_manager.save_tasks(st.session_state.tasks)
            st.rerun()