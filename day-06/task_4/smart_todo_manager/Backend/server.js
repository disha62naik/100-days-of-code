const express = require("express");
const fs = require("fs");
const cors = require("cors");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

const DB_FILE = "./db.json";

// Helper function to read DB
function readData() {
  const data = fs.readFileSync(DB_FILE);
  return JSON.parse(data);
}

// Helper function to write DB
function writeData(data) {
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

/* =========================
   GET - Fetch All Tasks
========================= */
app.get("/tasks", (req, res) => {
  const data = readData();
  res.json(data.tasks);
});

/* =========================
   POST - Add Task
========================= */
app.post("/tasks", (req, res) => {
  const data = readData();

  const newTask = {
    id: Date.now(),
    title: req.body.title,
    category: req.body.category,
    dueDate: req.body.dueDate,
    status: "Pending"
  };

  data.tasks.push(newTask);
  writeData(data);

  res.json(newTask);
});

/* =========================
   PUT - Toggle Status
========================= */
app.put("/tasks/:id", (req, res) => {
  const data = readData();
  const taskId = Number(req.params.id);

  const task = data.tasks.find(t => t.id === taskId);

  if (task) {
    task.status = task.status === "Pending" ? "Completed" : "Pending";
    writeData(data);
    res.json(task);
  } else {
    res.status(404).json({ message: "Task not found" });
  }
});

/* =========================
   DELETE - Delete Task
========================= */
app.delete("/tasks/:id", (req, res) => {
  const data = readData();
  const taskId = Number(req.params.id);

  data.tasks = data.tasks.filter(t => t.id !== taskId);
  writeData(data);

  res.json({ message: "Task deleted" });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});