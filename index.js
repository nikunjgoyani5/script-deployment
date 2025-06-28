const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post('/api/ask', (req, res) => {
  const prompt = req.body.prompt;
  if (!prompt) {
    return res.status(400).json({ status: "error", message: "Prompt is required" });
  }

  const pythonProcess = spawn(
  'C:\\Users\\hp1\\AppData\\Local\\Programs\\Python\\Python313\\python.exe',
  ['gpt_script.py', prompt]
);


  let result = "";
  let error = "";

  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    error += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0 || error.includes("Error:")) {
      return res.status(500).json({ status: "error", message: result.trim() || error.trim() });
    }
    return res.json({ status: "success", response: result.trim() });
  });
});

app.listen(5000, () => {
  console.log("✅ Node API running at http://localhost:5000");
});
