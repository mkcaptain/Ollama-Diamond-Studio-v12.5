# Ollama Diamond Studio v12.5
# Copyright (c) 2026 Marinos
# Licensed under the MIT License (see LICENSE file for details)

import tkinter as tk
from tkinter import ttk, messagebox
import ollama
import subprocess
import threading
import time
import webbrowser
import os
import json

# --- ΡΥΘΜΙΣΗ ΓΙΑ ΚΑΘΑΡΑ ΓΡΑΜΜΑΤΑ (DPI AWARENESS) ---
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

class OllamaMasterStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama AI Studio v12.5 - Professional Suite")
        self.root.geometry("1450x950")
        self.root.configure(bg="#f1f5f9")  # Light gray-blue background

        # Αρχικοποίηση μεταβλητών
        self.running_test = False
        self.create_help_guide()
        
        # Ρύθμιση Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Κατασκευή του UI
        self.setup_main_layout()
        self.setup_tabs_content() # <--- FIXED: Call setup_tabs_content here
        
        # Έναρξη Live Hardware Monitoring
        self.update_live_hw()
        
        # Φόρτωση μοντέλων
        self.load_models_to_combos()

    def configure_styles(self):
        """Ρυθμίσεις εμφάνισης για όλα τα γραφικά στοιχεία."""
        self.style.configure("TNotebook", background="#f1f5f9", borderwidth=0)
        self.style.configure(
            "TNotebook.Tab", 
            background="#e2e8f0", 
            padding=[20, 10], 
            font=("Segoe UI Semibold", 10)
        )
        self.style.map(
            "TNotebook.Tab", 
            background=[("selected", "#3b82f6")], 
            foreground=[("selected", "white")]
        )
        
        # Στυλ για τα Treeviews (Πίνακες)
        self.style.configure(
            "Treeview", 
            rowheight=35, 
            font=("Segoe UI", 10), 
            background="white", 
            fieldbackground="white",
            borderwidth=0
        )
        self.style.configure(
            "Treeview.Heading", 
            background="#1e293b", 
            foreground="white", 
            font=("Segoe UI Bold", 10)
        )
        
        # Στυλ για τις Μπάρες Προόδου
        self.style.configure(
            "Blue.Horizontal.TProgressbar", 
            foreground='#3b82f6', 
            background='#3b82f6', 
            thickness=15
        )
        self.style.configure(
            "Green.Horizontal.TProgressbar", 
            foreground='#10b981', 
            background='#10b981', 
            thickness=15
        )

    def create_help_guide(self):
        """Δημιουργεί αυτόματα ένα αρχείο οδηγιών για τον χρήστη."""
        path = "Ollama_User_Guide.txt"
        content = (
            "OLLAMA AI STUDIO v12.5 - ΟΔΗΓΙΕΣ ΧΡΗΣΗΣ\n"
            "========================================\n\n"
            "1. STRESS TEST: Επιλέξτε μοντέλο και δείτε TPS vs Context.\n"
            "2. COMPARISON: Συγκρίνετε δύο μοντέλα δίπλα-δίπλα.\n"
            "3. VRAM MANAGEMENT: Χρησιμοποιήστε το Unload για άμεση ελευθέρωση μνήμης.\n"
            "4. KEEP ALIVE: Η τιμή -1 κρατάει το μοντέλο φορτωμένο επ' αόριστον.\n"
            "5. HARDWARE: Αν η θερμοκρασία GPU ξεπεράσει τους 80C, κάντε διάλειμμα.\n"
        )
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass

    def setup_main_layout(self):
        """Δημιουργία του βασικού σκελετού της εφαρμογής."""
        # --- Top Bar (GPU Status) ---
        self.top_bar = tk.Frame(self.root, bg="#ffffff", height=100, relief="flat", highlightbackground="#e2e8f0", highlightthickness=1)
        self.top_bar.pack(side=tk.TOP, fill="x", padx=20, pady=15)
# --- ΣΥΝΕΧΕΙΑ setup_main_layout (από γραμμή 100) ---
        # Label για την GPU (Αριστερά στο Top Bar)
        self.gpu_label = tk.Label(
            self.top_bar, 
            text="🔍 Αναμονή δεδομένων GPU...", 
            bg="white", 
            font=("Segoe UI Bold", 11), 
            fg="#1e40af"
        )
        self.gpu_label.pack(side=tk.LEFT, padx=25)

        # Frame για τα System Buttons (Δεξιά στο Top Bar)
        sys_btn_frame = tk.Frame(self.top_bar, bg="white")
        sys_btn_frame.pack(side=tk.RIGHT, padx=20)

        self.btn_restart = tk.Button(
            sys_btn_frame, text="🔄 Επανεκκίνηση Ollama", 
            command=self.restart_ollama_service,
            bg="#f59e0b", fg="white", relief="flat", 
            padx=15, pady=8, font=("Segoe UI Semibold", 9), cursor="hand2"
        )
        self.btn_restart.pack(side=tk.LEFT, padx=5)

        tk.Button(
            sys_btn_frame, text="ℹ️ Σχετικά", 
            command=self.show_about,
            bg="#64748b", fg="white", relief="flat", 
            padx=15, pady=8, font=("Segoe UI Semibold", 9), cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        # --- API CONTROL CENTER PANEL ---
        self.api_panel = tk.LabelFrame(
            self.root, 
            text=" 📡 API Control Center & VRAM Management ", 
            bg="white", padx=15, pady=15, 
            fg="#3b82f6", font=("Segoe UI Bold", 10),
            relief="flat", highlightbackground="#e2e8f0", highlightthickness=1
        )
        self.api_panel.pack(side=tk.TOP, fill="x", padx=20, pady=5)

        # Κουμπιά ελέγχου API
        tk.Button(
            self.api_panel, text="🔍 Έλεγχος Server", 
            command=self.check_api_health, 
            bg="#f8fafc", relief="solid", borderwidth=1, padx=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.api_panel, text="🏃 Ενεργά Μοντέλα (PS)", 
            command=self.get_active_models_ps, 
            bg="#f8fafc", relief="solid", borderwidth=1, padx=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.api_panel, text="🔄 Ανανέωση Λίστας", 
            command=self.load_models_to_combos, 
            bg="#f8fafc", relief="solid", borderwidth=1, padx=10
        ).pack(side=tk.LEFT, padx=5)

        # Διαχωριστικό
        tk.Frame(self.api_panel, width=2, bg="#e2e8f0").pack(side=tk.LEFT, fill="y", padx=15)

        # Keep Alive Επιλογή
        tk.Label(self.api_panel, text="Keep Alive:", bg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.keep_alive_combo = ttk.Combobox(
            self.api_panel, 
            values=["0 (Άμεσο Unload)", "5m", "15m", "30m", "1h", "-1 (Μόνιμα)"], 
            width=15, state="readonly"
        )
        self.keep_alive_combo.set("15m")
        self.keep_alive_combo.pack(side=tk.LEFT, padx=5)

        # Κουμπί Force Unload (Κόκκινο)
        self.btn_unload = tk.Button(
            self.api_panel, text="🛑 Επιβολή Unload", 
            command=self.force_unload_model, 
            bg="#fee2e2", fg="#991b1b", relief="flat", 
            padx=15, font=("Segoe UI Bold", 9), cursor="hand2"
        )
        self.btn_unload.pack(side=tk.RIGHT, padx=5)

        # --- ΚΥΡΙΟ ΜΕΝΟΥ (TABS) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

    # --- ΣΥΝΑΡΤΗΣΕΙΣ HARDWARE & API (Γραμμές 160-200) ---
    def get_gpu_status(self):
        """Εκτελεί το nvidia-smi για να πάρει ζωντανά δεδομένα."""
        try:
            cmd = ["nvidia-smi", "--query-gpu=gpu_name,memory.used,memory.total,temperature.gpu", "--format=csv,noheader,nounits"]
            output = subprocess.check_output(cmd, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
            name, used, total, temp = output.strip().split(", ")
            return {
                "name": name,
                "used": int(used),
                "total": int(total),
                "temp": temp,
                "display": f"🎮 {name} | 🌡️ {temp}°C | 💾 VRAM: {used}/{total} MB"
            }
        except FileNotFoundError:
            return None
        except Exception as e:
            # self.log(f"GPU Error: {e}", "error") # Avoid flooding logs here
            return None

    def update_live_hw(self):
        """Ανανεώνει την ετικέτα της GPU κάθε 2 δευτερόλεπτα."""
        status = self.get_gpu_status()
        if status:
            self.gpu_label.config(text=status["display"])
            # Αλλαγή χρώματος αν η GPU ζεσταθεί πολύ (>75C)
            if int(status["temp"]) > 75:
                self.gpu_label.config(fg="#ef4444")
            else:
                self.gpu_label.config(fg="#1e40af")
        else:
            self.gpu_label.config(text="⚠️ GPU: Μη διαθέσιμη (NVIDIA-SMI Error)")
        
        self.root.after(2000, self.update_live_hw)

    def log(self, message, type="info"):
        """Κεντρική συνάρτηση καταγραφής στο Log Area."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.config(state="normal")
        color_tag = "cyan"
        if type == "error": color_tag = "red"
        if type == "success": color_tag = "green"
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
    def setup_tabs_content(self):
        """Δημιουργία των περιεχομένων για κάθε Tab."""
        # --- TAB 1: STRESS TEST ---
        self.tab_stress = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.tab_stress, text="  🧪 Stress Test  ")
        
        stress_ctrl = tk.Frame(self.tab_stress, bg="#f8fafc", pady=15)
        stress_ctrl.pack(fill="x")
        
        tk.Label(stress_ctrl, text="Επιλογή Μοντέλου:", bg="#f8fafc", font=("Segoe UI Semibold", 10)).pack(side=tk.LEFT, padx=20)
        self.stress_combo = ttk.Combobox(stress_ctrl, width=35, state="readonly")
        self.stress_combo.pack(side=tk.LEFT, padx=5)
        
        self.btn_run_stress = tk.Button(
            stress_ctrl, text="▶ Έναρξη Benchmark", 
            command=self.start_stress_thread, 
            bg="#3b82f6", fg="white", relief="flat", padx=20, font=("Segoe UI Bold", 9)
        )
        self.btn_run_stress.pack(side=tk.LEFT, padx=15)

        # Μπάρα Προόδου Τεστ
        self.stress_progress = ttk.Progressbar(self.tab_stress, orient=tk.HORIZONTAL, mode='determinate', style="Blue.Horizontal.TProgressbar")
        self.stress_progress.pack(fill="x", padx=25, pady=5)

        # Πίνακας Αποτελεσμάτων Stress Test
        self.tree_stress = ttk.Treeview(self.tab_stress, columns=("ctx", "tps", "vram", "temp", "status"), show="headings")
        columns = [
            ("ctx", "Context (Tokens)"), ("tps", "Speed (Tokens/sec)"), 
            ("vram", "VRAM Usage"), ("temp", "GPU Temp"), ("status", "Κατάσταση")
        ]
        for col, head in columns:
            self.tree_stress.heading(col, text=head)
            self.tree_stress.column(col, anchor="center", width=120)
        self.tree_stress.pack(fill="both", expand=True, padx=20, pady=10)

        # --- TAB 2: MODEL COMPARISON ---
        self.tab_compare = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.tab_compare, text="  ⚖️ Σύγκριση Μοντέλων  ")
        
        comp_ctrl = tk.Frame(self.tab_compare, bg="#f8fafc", pady=20)
        comp_ctrl.pack(fill="x")

        # Επιλογή Μοντέλου Α
        tk.Label(comp_ctrl, text="Model A:", bg="#f8fafc").grid(row=0, column=0, padx=10)
        self.combo_a = ttk.Combobox(comp_ctrl, width=25, state="readonly")
        self.combo_a.grid(row=0, column=1)

        # Επιλογή Μοντέλου Β
        tk.Label(comp_ctrl, text="Model B:", bg="#f8fafc").grid(row=0, column=2, padx=10)
        self.combo_b = ttk.Combobox(comp_ctrl, width=25, state="readonly")
        self.combo_b.grid(row=0, column=3)

        self.btn_compare = tk.Button(
            comp_ctrl, text="Σύγκριση Ταχύτητας", 
            command=self.start_compare_thread, 
            bg="#8b5cf6", fg="white", relief="flat", padx=20
        )
        self.btn_compare.grid(row=0, column=4, padx=20)

        # Πίνακας Σύγκρισης
        self.tree_compare = ttk.Treeview(self.tab_compare, columns=("ctx", "tps_a", "tps_b", "diff", "winner"), show="headings")
        comp_cols = [
            ("ctx", "Context"), ("tps_a", "TPS (Model A)"), 
            ("tps_b", "TPS (Model B)"), ("diff", "Διαφορά %"), ("winner", "Νικητής")
        ]
        for col, head in comp_cols:
            self.tree_compare.heading(col, text=head)
            self.tree_compare.column(col, anchor="center")
        self.tree_compare.pack(fill="both", expand=True, padx=20, pady=10)

        # --- TAB 3: MODEL MANAGER (Προετοιμασία) ---
        self.tab_manager = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.tab_manager, text="  📦 Model Manager  ")
        self.setup_manager_ui()

    def setup_manager_ui(self):
        """Κατασκευή του UI για τη διαχείριση (Download/Delete)."""
        # Frame Λήψης
        dl_frame = tk.LabelFrame(self.tab_manager, text=" 📥 Λήψη Νέου Μοντέλου ", bg="white", padx=20, pady=15, font=("Segoe UI Bold", 9))
        dl_frame.pack(fill="x", padx=20, pady=10)
        
        self.dl_input = ttk.Combobox(dl_frame, values=["deepseek-r1:7b", "llama3.2:3b", "mistral:latest", "phi3:latest"], width=40)
        self.dl_input.set("deepseek-r1:7b")
        self.dl_input.pack(side=tk.LEFT, padx=10)
        tk.Button(dl_frame, text="⬇ Pull Model", command=self.run_download_thread, bg="#10b981", fg="white", relief="flat", padx=20).pack(side=tk.LEFT)
        tk.Button(dl_frame, text="🌐 Ollama Library", command=lambda: webbrowser.open("https://ollama.com/library"), bg="#3b82f6", fg="white", relief="flat", padx=15).pack(side=tk.LEFT, padx=10)

        self.dl_progress = ttk.Progressbar(dl_frame, orient=tk.HORIZONTAL, mode='determinate', style="Green.Horizontal.TProgressbar")
        self.dl_progress.pack(fill="x", pady=15, side=tk.BOTTOM)

        # Frame Διαγραφής
        del_frame = tk.LabelFrame(self.tab_manager, text=" 🗑️ Διαγραφή Μοντέλου ", bg="white", padx=20, pady=15, font=("Segoe UI Bold", 9))
        del_frame.pack(fill="x", padx=20, pady=10)
        
        self.del_combo = ttk.Combobox(del_frame, width=40, state="readonly")
        self.del_combo.pack(side=tk.LEFT, padx=10)
        tk.Button(del_frame, text="❌ Uninstall", command=self.delete_model_action, bg="#ef4444", fg="white", relief="flat", padx=20).pack(side=tk.LEFT)

        # --- LOG AREA (Στο κάτω μέρος της εφαρμογής) ---
        log_label = tk.Label(self.root, text="💻 System Console / Logs", bg="#f1f5f9", font=("Segoe UI Bold", 9), fg="#64748b")
        log_label.pack(anchor="w", padx=25)
        self.log_text = tk.Text(self.root, height=8, bg="#1e293b", fg="#38bdf8", font=("Consolas", 10), padx=15, pady=10)
        self.log_text.pack(fill="x", padx=20, pady=(0, 20))
        self.log_text.config(state="disabled")

    # --- ΣΥΝΑΡΤΗΣΕΙΣ ΛΟΓΙΚΗΣ (API & ACTIONS) ---
    def check_api_health(self):
        try:
            ollama.list()
            self.log("✅ API Connection: OK (Port 11434)", "success")
            messagebox.showinfo("API Check", "Ο Ollama Server είναι ενεργός και αποκρίνεται!")
        except Exception as e:
            self.log(f"❌ API Connection: FAILED ({e})", "error")

    def get_active_models_ps(self):
        try:
            active = ollama.ps()
            if not active.models:
                self.log("💤 Καμία διεργασία στη VRAM αυτή τη στιγμή.")
            for m in active.models:
                vram_gb = m.size_vram / (1024**3)
                self.log(f"🔥 ACTIVE: {m.model} | VRAM: {vram_gb:.2f} GB | Expires: {m.expires_at}")
        except Exception as e:
            self.log(f"❌ PS Error: {e}", "error")

    def force_unload_model(self):
        model = self.stress_combo.get()
        if not model: return
        self.log(f"🛑 Αποστολή αιτήματος Unload για: {model}...")
        try:
            ollama.generate(model=model, keep_alive=0)
            self.log(f"✅ Το μοντέλο {model} αφαιρέθηκε από τη μνήμη.")
        except Exception as e:
            self.log(f"❌ Unload Failed: {e}", "error")

    def restart_ollama_service(self):
        self.log("🔄 Επανεκκίνηση υπηρεσίας Ollama...")
        os.system("taskkill /f /im ollama.exe")
        time.sleep(2)
        subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
        self.log("⏳ Αναμονή 5 δευτερολέπτων για αρχικοποίηση...")
        self.root.after(5000, self.load_models_to_combos)

    def load_models_to_combos(self):
        try:
            models_data = ollama.list()
            all_names = [m.model for m in models_data.models]
            # Φιλτράρισμα cloud μοντέλων για Stress Test & Comparison
            local_names = [n for n in all_names if ":cloud" not in n.lower()]
            
            self.stress_combo['values'] = local_names
            self.del_combo['values'] = all_names # Τα cloud μοντέλα παραμένουν στη διαγραφή
            self.combo_a['values'] = local_names
            self.combo_b['values'] = local_names
            
            if local_names:
                self.stress_combo.current(0)
                self.combo_a.current(0)
                if len(local_names) > 1:
                    self.combo_b.current(1)
            
            if all_names:
                self.del_combo.current(0)
                
            self.log(f"📦 Φορτώθηκαν {len(all_names)} μοντέλα ({len(local_names)} τοπικά).")
        except Exception as e:
            self.log(f"⚠️ Αδυναμία λήψης λίστας μοντέλων: {e}", "error")

    # --- THREADED TASKS ---
    def start_stress_thread(self):
        m = self.stress_combo.get()
        if not m: return
        self.btn_run_stress.config(state="disabled")
        for i in self.tree_stress.get_children(): self.tree_stress.delete(i)
        threading.Thread(target=self._stress_logic, args=(m,), daemon=True).start()

    def _stress_logic(self, model):
        # Δοκιμή σε 4 επίπεδα context
        context_levels = [4096, 8192, 16384, 32768]
        keep_alive = self.keep_alive_combo.get().split(" ")[0]
        
        for i, ctx in enumerate(context_levels):
            try:
                self.log(f"🧪 Τεστ: {model} @ {ctx} context...")
                start_t = time.time()
                # Αποστολή αιτήματος generate
                res = ollama.generate(model=model, prompt="Explain the theory of relativity in 100 words.", 
                                      options={"num_ctx": ctx}, keep_alive=keep_alive)
                
                # Υπολογισμός ταχύτητας με ασφάλεια
                eval_duration = res.get('eval_duration') or 0
                eval_count = res.get('eval_count') or 0
                
                if eval_duration > 0:
                    duration = eval_duration / 1e9
                    tps = eval_count / duration
                else:
                    tps = 0
                
                # Λήψη VRAM/Temp από το nvidia-smi
                gpu = self.get_gpu_status()
                vram_info = f"{gpu['used']} MB" if gpu else "N/A"
                temp_info = f"{gpu['temp']}°C" if gpu else "N/A"
                
                self.root.after(0, lambda c=ctx, t=tps, v=vram_info, te=temp_info: 
                               self.tree_stress.insert("", "end", values=(c, f"{t:.2f}", v, te, "✅ OK")))
                
                # Ενημέρωση Progress Bar
                self.root.after(0, lambda v=(i+1)*25: self.stress_progress.configure(value=v))
            except Exception as e:
                self.log(f"❌ Error @ {ctx} ctx: {e}", "error")
                break
        
        self.root.after(0, lambda: self.btn_run_stress.config(state="normal"))
        self.log(f"🏁 Το Stress Test για το {model} ολοκληρώθηκε.")

    def run_download_thread(self):
        name = self.dl_input.get().strip()
        if not name: return
        threading.Thread(target=self._download_logic, args=(name,), daemon=True).start()

    def _download_logic(self, name):
        try:
            self.log(f"📥 Έναρξη λήψης: {name}...")
            for progress in ollama.pull(name, stream=True):
                if 'total' in progress and 'completed' in progress:
                    pct = (progress['completed'] / progress['total']) * 100
                    self.root.after(0, lambda v=pct: self.dl_progress.configure(value=v))
                elif 'status' in progress:
                    # Προαιρετικά: Ενημέρωση log με το status (π.χ. "pulling manifest")
                    pass
            self.log(f"✅ Το μοντέλο {name} εγκαταστάθηκε!", "success")
            self.root.after(0, self.load_models_to_combos)
        except Exception as e:
            self.log(f"❌ Σφάλμα λήψης {name}: {e}", "error")

    def delete_model_action(self):
        m = self.del_combo.get()
        if m and messagebox.askyesno("Επιβεβαίωση", f"Είστε σίγουροι ότι θέλετε να διαγράψετε το μοντέλο {m};"):
            try:
                ollama.delete(m)
                self.log(f"🗑️ Το μοντέλο {m} διαγράφηκε επιτυχώς.")
                self.load_models_to_combos()
            except Exception as e:
                self.log(f"❌ Αποτυχία διαγραφής: {e}", "error")

    # --- TAB COMPARISON LOGIC (Συντομογραφία για το benchmark) ---
    def start_compare_thread(self):
        a, b = self.combo_a.get(), self.combo_b.get()
        if not a or not b: return
        threading.Thread(target=self._compare_logic, args=(a, b), daemon=True).start()

    def _compare_logic(self, model_a, model_b):
        self.log(f"⚖️ Σύγκριση: {model_a} vs {model_b}")
        # Δοκιμή σε standard 8K context
        for ctx in [8192, 16384]:
            try:
                # Test Model A
                res_a = ollama.generate(model=model_a, prompt="Say Hello", options={"num_ctx": ctx})
                duration_a = res_a.get('eval_duration') or 0
                count_a = res_a.get('eval_count') or 0
                tps_a = (count_a / (duration_a / 1e9)) if duration_a > 0 else 0
                
                # Test Model B
                res_b = ollama.generate(model=model_b, prompt="Say Hello", options={"num_ctx": ctx})
                duration_b = res_b.get('eval_duration') or 0
                count_b = res_b.get('eval_count') or 0
                tps_b = (count_b / (duration_b / 1e9)) if duration_b > 0 else 0
                
                if tps_b > 0:
                    diff = ((tps_a - tps_b) / tps_b) * 100
                else:
                    diff = 0
                
                winner = model_a if tps_a > tps_b else model_b
                
                self.root.after(0, lambda c=ctx, t1=tps_a, t2=tps_b, d=diff, w=winner: 
                               self.tree_compare.insert("", "end", values=(c, f"{t1:.2f}", f"{t2:.2f}", f"{d:.1f}%", w)))
            except Exception as e:
                self.log(f"❌ Error comparing {model_a} and {model_b}: {e}", "error")

    def show_about(self):
        """Εμφανίζει το παράθυρο με τις πληροφορίες και την άδεια MIT."""
        about_text = (
            "Ollama Diamond Studio v12.5\n"
            "---------------------------\n"
            "Developer: Marinos\n"
            "License: MIT License\n\n"
            "Copyright (c) 2026 Marinos\n\n"
            "Το λογισμικό παρέχεται 'ως έχει' για σκοπούς δοκιμής "
            "της GTX 1070 Ti και διαχείρισης μοντέλων Ollama."
        )
        messagebox.showinfo("About / License", about_text)

# --- ΕΚΚΙΝΗΣΗ ΕΦΑΡΜΟΓΗΣ ---
if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaMasterStudio(root)
    root.mainloop()