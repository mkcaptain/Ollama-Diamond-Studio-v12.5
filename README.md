# 🚀 Ollama AI Studio v12.5 - Professional Suite

### _Η απόλυτη εργαλειοθήκη για AI Benchmarking & VRAM Management_

> **Ειδικά σχεδιασμένο για τους κατόχους NVIDIA GTX 1070 Ti (8GB) και Pascal Architecture.**

![Ollama AI Studio Banner](https://img.shields.io/badge/GPU-GTX_1070_Ti_Compatible-green?style=for-the-badge&logo=nvidia)
![Ollama Version](https://img.shields.io/badge/Ollama-v0.5+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

---

## 🌟 Γιατί το Ollama AI Studio είναι απαραίτητο για την 1070 Ti σου;

Η **GTX 1070 Ti** παραμένει ένα "θηρίο" με 8GB VRAM, αλλά στον κόσμο των LLMs, η σωστή διαχείριση της μνήμης είναι το παν. Αυτή η εφαρμογή δημιουργήθηκε για να σου δώσει τον πλήρη έλεγχο, επιτρέποντάς σου να "στύψεις" την κάρτα σου με ασφάλεια και ταχύτητα.

### 💎 Κύρια Χαρακτηριστικά:

- **📊 Live Hardware Monitoring:** Δες σε πραγματικό χρόνο τη θερμοκρασία και τη χρήση της VRAM. Η εφαρμογή σε προειδοποιεί αν η Pascal GPU σου αρχίσει να ζεσταίνεται υπερβολικά (>75°C).
- **🧪 Stress Test & TPS Benchmarking:** Μην μαντεύεις. Τέσταρε κάθε μοντέλο (DeepSeek, Llama 3, Mistral) σε διαφορετικά Context levels (4K έως 32K) και δες ακριβώς πόσα Tokens per Second (TPS) πιάνεις.
- **⚖️ Σύγκριση Μοντέλων (Side-by-Side):** Βρες ποιο μοντέλο τρέχει πιο αποδοτικά στην 1070 Ti. Σύγκρινε δύο μοντέλα ταυτόχρονα και δες το ποσοστό διαφοράς στην ταχύτητα.
- **🛑 Έλεγχος VRAM (Force Unload):** Μείνε εντός των 8GB. Αν ένα μοντέλο "κολλήσει" στη μνήμη, μπορείς να το κάνεις Unload με ένα κλικ για να ελευθερώσεις χώρο για το επόμενο.
- **⏳ Keep Alive Control:** Ρύθμισε πόση ώρα θα παραμένει το μοντέλο φορτωμένο στη GPU, από 0 (άμεσο unload) μέχρι -1 (μόνιμα).

---

## 🧪 Δοκιμασμένα Μοντέλα (Tested & Verified)

Η εφαρμογή έχει δοκιμαστεί με επιτυχία στην **GTX 1070 Ti** με τα παρακάτω μοντέλα. Τα αποτελέσματα είναι **άκρως εντυπωσιακά**:

- **qwen2-vl:4b** (Vision-Language capabilities)
- **qwen2.5-coder:7b** (Coding precision)
- **lfm2.5-thinking:latest** (Complex Reasoning)
- **nomic-embed-text:latest** (High-speed Embeddings)
- **gemma3:4b** (Modern standard)
- **ministral-3:3b** (Efficiency & Speed)

---

## 🛠️ Τεχνικές Προδιαγραφές & Απαιτήσεις

- **GPU:** NVIDIA GTX 1070 Ti (ή οποιαδήποτε κάρτα με NVIDIA-SMI υποστήριξη).
- **Software:** [Ollama](https://ollama.com/) installed and running.
- **Python:** 3.8+ με βιβλιοθήκες `ollama`, `tkinter`.
- **OS:** Windows 10/11 (για πλήρη υποστήριξη DPI Awareness και NVIDIA-SMI).

---

## 🚀 Γρήγορη Εγκατάσταση

1.  **Κλωνοποιήστε το αποθετήριο:**

    ```bash
    git clone https://github.com/your-repo/ollama-ai-studio.git
    cd ollama-ai-studio
    ```

2.  **Εγκαταστήστε τις εξαρτήσεις:**

    ```bash
    pip install ollama
    ```

3.  **Τρέξτε την εφαρμογή:**
    ```bash
    python Ollama_Pro.py
    ```

---

## 📖 Πώς να το χρησιμοποιήσετε

1.  **Stress Test:** Επιλέξτε το μοντέλο που κατεβάσατε και πατήστε "Έναρξη Benchmark". Η εφαρμογή θα μετρήσει την ταχύτητα σε 4 επίπεδα context.
2.  **Σύγκριση:** Επιλέξτε δύο μοντέλα (π.χ. Llama3.2-3B vs Phi-3) και δείτε ποιο είναι ο "νικητής" για το δικό σας hardware.
3.  **Model Manager:** Κατεβάστε νέα μοντέλα απευθείας από το interface ή διαγράψτε αυτά που πιάνουν χώρο στον δίσκο σας.

---

## 🛡️ Ασφάλεια & Θερμοκρασίες

Η GTX 1070 Ti είναι ανθεκτική, αλλά τα AI workloads την πιέζουν στα άκρα. Το **Ollama AI Studio** παρακολουθεί ενεργά τη θερμοκρασία. Αν δείτε το χρώμα της GPU στο Top Bar να γίνεται **κόκκινο**, συνιστάται ένα μικρό διάλειμμα για να αποφύγετε το thermal throttling.

---

## 📜 Άδεια Χρήσης

Αυτό το έργο διατίθεται υπό την άδεια **MIT**. Δείτε το αρχείο [LICENSE](LICENSE) για λεπτομέρειες.

_Developed with ❤️ by **Marinos** for the AI Community._
