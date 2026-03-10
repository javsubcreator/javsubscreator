import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import subprocess
import os
import shutil
import pysrt
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from queue import Queue

MODEL_NAME = "Helsinki-NLP/opus-mt-ja-en"

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading translation model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16
).to(device)

model.eval()

progress_queue = Queue()


def translate_srt(jp_srt, en_srt):

    subs = pysrt.open(jp_srt, encoding="utf-8")

    texts = [s.text for s in subs]

    batch_size = 128

    total = len(texts)

    for i in range(0, total, batch_size):

        batch = texts[i:i+batch_size]

        tokens = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(device)

        with torch.no_grad():

            outputs = model.generate(**tokens)

        translated = tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )

        for j, text in enumerate(translated):

            subs[i+j].text = text

        progress = int((i / total) * 100)

        progress_queue.put(progress)

    subs.save(en_srt)

    progress_queue.put(100)


def process_video(video_path):

    input_path = os.path.abspath(video_path)

    video_dir = os.path.dirname(input_path)

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    jp_srt = os.path.join(video_dir, f"{base_name}.ja.whisperjav.srt")

    en_srt = os.path.join(video_dir, f"{base_name}.en.srt")

    status_label.config(text="Step 1/2: Generating Japanese subtitles...")

    subprocess.run([
        "whisperjav",
        input_path,
        "--mode",
        "balanced"
    ])

    status_label.config(text="Step 2/2: Translating subtitles...")

    translate_srt(jp_srt, en_srt)

    if os.path.exists(jp_srt):
        os.remove(jp_srt)

    raw_subs = os.path.join(video_dir, "raw_subs")

    if os.path.exists(raw_subs):
        shutil.rmtree(raw_subs)

    status_label.config(text=f"Finished! Saved: {en_srt}")


def start_processing():
    
    progress_bar["value"] = 0

    video_path = file_path.get()

    if not video_path:
        status_label.config(text="Please select a video file.")
        return

    thread = threading.Thread(target=process_video, args=(video_path,))
    thread.start()


def browse_file():

    path = filedialog.askopenfilename(
        filetypes=[("MP4 files", "*.mp4")]
    )

    file_path.set(path)


def update_progress():

    while not progress_queue.empty():

        value = progress_queue.get()

        progress_bar["value"] = value

    root.after(100, update_progress)


root = tk.Tk()

root.title("Subtitle Generator")

root.geometry("500x220")

file_path = tk.StringVar()

tk.Label(root, text="Select MP4 file").pack(pady=5)

entry = tk.Entry(root, textvariable=file_path, width=60)

entry.pack()

tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

tk.Button(root, text="Generate Subtitles", command=start_processing).pack(pady=10)

progress_bar = ttk.Progressbar(root, length=400)

progress_bar.pack(pady=10)

status_label = tk.Label(root, text="Idle")

status_label.pack()

root.after(100, update_progress)

root.mainloop()