function showAlert(message, type = "success") {
  let alertContainer = document.getElementById("alert-container");
  let alertBox = document.createElement("div");
  alertBox.classList.add("alert", `alert-${type}`);
  alertBox.setAttribute("role", "alert");
  alertBox.textContent = message;

  alertContainer.appendChild(alertBox);
  setTimeout(() => {
    alertBox.classList.add("show");
  }, 100);

  setTimeout(() => {
    alertBox.classList.remove("show");
    setTimeout(() => {
      alertContainer.removeChild(alertBox);
    }, 300);
  }, 3000);
}

function displayTask(taskData) {
  let tasksList = document.getElementById("tasks-list");
  let listItem = document.createElement("li");
  listItem.classList.add("list-group-item");
  listItem.innerHTML = `${taskData.task} - ${taskData.priority} - ${taskData.due_date} ${taskData.due_time}`;
  tasksList.appendChild(listItem);
}

function fetchTasks() {
  fetch("/get_tasks")
    .then((response) => {
      return response.json();
    })
    .then((tasks) => {
      tasks.forEach((taskData) => {
        displayTask(taskData);
      });
    });
}

function displayTask(taskData) {
  let tasksList = document.getElementById("tasks-list");
  let listItem = document.createElement("li");
  listItem.classList.add("list-group-item");
  listItem.setAttribute("data-task-id", taskData.id);

  // Add priority color based on task priority
  let priorityColor;
  switch (taskData.priority) {
    case "Low":
      priorityColor = "rgba(255, 255, 0, 0.2)"; // semi-transparent yellow
      break;
    case "Medium":
      priorityColor = "rgba(255, 165, 0, 0.2)"; // semi-transparent orange
      break;
    case "High":
      priorityColor = "rgba(255, 0, 0, 0.2)"; // semi-transparent red
      break;
    default:
      priorityColor = "rgba(255, 255, 0, 0.2)";
  }
  listItem.style.backgroundColor = priorityColor;

  let checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.classList.add("form-check-input");
  checkbox.addEventListener("change", function () {
    listItem.classList.toggle("completed");

    let completedTasks = document.getElementsByClassName("completed");
    if (this.checked) {
      tasksList.insertBefore(listItem, completedTasks[0]);
    } else {
      tasksList.insertBefore(listItem, tasksList.firstChild);
    }
  });

  let label = document.createElement("label");
  label.classList.add("form-check-label");
  label.innerHTML = `${taskData.task} - ${taskData.due_date} ${taskData.due_time}`;

  listItem.appendChild(checkbox);
  listItem.appendChild(label);
  tasksList.appendChild(listItem);

  showAlert("Task added successfully!");
}

function sortTasks(option) {
  fetch("/get_tasks")
    .then((response) => {
      return response.json();
    })
    .then((tasks) => {
      if (option === "Date") {
        tasks.sort(compareDates);
      } else if (option === "Time") {
        tasks.sort(compareTimes);
      } else if (option === "Priority") {
        tasks.sort(comparePriorities);
      }

      let tasksList = document.getElementById("tasks-list");
      tasksList.innerHTML = "";

      tasks.forEach((taskData) => {
        displayTask(taskData);
      });
    });
}

function showAlert(message, type = "success") {
  let alertContainer = document.getElementById("alert-container");
  let alertBox = document.createElement("div");
  alertBox.classList.add("alert", `alert-${type}`);
  alertBox.setAttribute("role", "alert");
  alertBox.textContent = message;

  alertContainer.appendChild(alertBox);
  setTimeout(() => {
    alertBox.classList.add("show");
  }, 100);

  setTimeout(() => {
    alertBox.classList.remove("show");
    setTimeout(() => {
      alertContainer.removeChild(alertBox);
    }, 300);
  }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("add-task-btn").addEventListener("click", () => {
    let taskInput = document.getElementById("task-input");
    let prioritySelect = document.getElementById("priority-select");
    let dueDateInput = document.getElementById("due-date-input");
    let dueTimeInput = document.getElementById("due-time-input");

    let task = taskInput.value;
    let priority = prioritySelect.value;
    let dueDate = dueDateInput.value;
    let dueTime = dueTimeInput.value;

    let formData = new FormData();
    formData.append("task", task);
    formData.append("priority", priority);
    formData.append("due_date", dueDate);
    formData.append("due_time", dueTime);

    fetch("/add_task", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        displayTask(data);

        taskInput.value = "";
        dueDateInput.value = "";
        dueTimeInput.value = "";
      });
  });

  // Add dark-mode-btn event listener
  const darkModeButton = document.getElementById("dark-mode-btn");
  darkModeButton.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    const icon = darkModeButton.querySelector("i");
    if (document.body.classList.contains("dark-mode")) {
      icon.classList.replace("fas", "far");
      icon.classList.replace("fa-sun", "fa-moon");
      icon.style.color = "white"; // Change the icon color to white in dark mode
    } else {
      icon.classList.replace("far", "fas");
      icon.classList.replace("fa-moon", "fa-sun");
      icon.style.color = ""; // Reset the icon color to default in light mode
    }
  });

  document.getElementById("sort-date").addEventListener("click", () => {
    sortTasks("date");
  });

  document.getElementById("sort-time").addEventListener("click", () => {
    sortTasks("time");
  });

  document.getElementById("sort-priority").addEventListener("click", () => {
    sortTasks("priority");
  });

  document.getElementById("clear-all-btn").addEventListener("click", () => {
    fetch("/clear_tasks", {
      method: "POST",
    })
      .then((response) => {
        if (response.status === 200) {
          let tasksList = document.getElementById("tasks-list");
          while (tasksList.firstChild) {
            tasksList.removeChild(tasksList.firstChild);
          }
        } else {
          console.error("Error clearing tasks:", response.statusText);
        }
      })
      .catch((error) => {
        console.error("Error clearing tasks:", error);
      });
  });

  fetchTasks();
});
