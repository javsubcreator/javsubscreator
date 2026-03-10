# 🎬 Japanese → English Subtitle Generator

This tool automatically generates **English subtitles (SRT)** from a Japanese video file.

It works in two steps:

1. Generate Japanese subtitles using **WhisperJAV**
2. Translate Japanese subtitles to English using **GPU acceleration**

The final `.en.srt` file will be saved **in the same folder as the video**.

Example result:

```
movie.mp4
movie.en.srt
```

Temporary files are removed automatically.

---

# 🖥 Requirements

You need the following installed on your computer:

* **Python 3.10+**
* **NVIDIA GPU (recommended for fast translation)**

The tool has been tested with:

```
RTX 4060
RAM 16GB
CUDA enabled PyTorch
```

---

# 📦 Files in this project

```
app.py              → Main application
requirements.txt    → List of required Python packages
README.md           → Instructions
```

---

# ⚙️ Step 1 — Install Python

Download Python from:

https://www.python.org/downloads/

During installation **make sure to check**:

```
Add Python to PATH
```

---

# ⚙️ Step 2 — Open a terminal

Navigate to the project folder.

Example:

```
D:\SubtitleTool
```

Open **Command Prompt / PowerShell** inside the folder.

---

# ⚙️ Step 3 — Create a virtual environment

Run:

```
python -m venv .venv
```

This creates an isolated Python environment.

---

# ⚙️ Step 4 — Activate the environment

### Windows

```
.venv\Scripts\activate
```

You should now see:

```
(.venv)
```

in your terminal.

---

# ⚙️ Step 5 — Install dependencies

Run:

```
pip install -r requirements.txt
```

This will install:

* torch
* transformers
* pysrt
* sentencepiece
* tqdm
* and other dependencies

---

# ⚙️ Step 6 — Install WhisperJAV

Install WhisperJAV:

```
pip install whisperjav
```

Verify installation:

```
whisperjav --help
```

---

# ▶️ Step 7 — Run the application

Start the tool:

```
python app.py
```

A window will open.

---

# 🧠 How to use the tool

1. Click **Browse**
2. Select a `.mp4` video
3. Click **Generate Subtitles**

The program will:

```
Step 1/2 → Generate Japanese subtitles
Step 2/2 → Translate subtitles to English
```

When finished:

```
video.en.srt
```

will appear next to the video.

---

# 📂 Example

Input:

```
Videos/
   movie.mp4
```

Output:

```
Videos/
   movie.mp4
   movie.en.srt
```

---

# 🚀 Optional: Build a standalone EXE

If you want to share this tool with others, you can create an executable.

Install PyInstaller:

```
pip install pyinstaller
```

Build the EXE:

```
pyinstaller --onefile app.py
```

The executable will be created in:

```
dist/app.exe
```

You can run it by double-clicking.

---

# ⚡ Performance

Processing speed depends on your hardware.

Example:

```
2 hour video
RTX 4060 GPU
≈ 5–10 minutes
```

---

# ❗ Troubleshooting

### GPU not detected

Check:

```
python -c "import torch; print(torch.cuda.is_available())"
```

Should return:

```
True
```

---

### WhisperJAV not found

Run:

```
pip install whisperjav
```

---

### Dependencies missing

Run again:

```
pip install -r requirements.txt
```

---

# 🧹 Temporary files

During processing the tool may create:

```
.ja.whisperjav.srt
raw_subs/
```

These are **automatically deleted** after translation.

---

# 📝 License

This tool is provided for personal use.

---

# 🙌 Credits

* WhisperJAV
* PyTorch
* HuggingFace Transformers
