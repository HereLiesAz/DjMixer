import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from main import main as analyze_files
from analyzer.multi_track_mixer import MultiTrackMixer
from visualization.advanced_visualizer import AdvancedVisualizer

class DJMixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DJ Mix Analyzer Pro")
        self.root.geometry("1200x800")
        self.tracks = []
        self.current_analysis = None

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 10))

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - File management
        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # File controls
        ttk.Button(left_panel, text="Add Tracks", command=self.add_tracks).pack(fill=tk.X)
        ttk.Button(left_panel, text="Clear All", command=self.clear_tracks).pack(fill=tk.X, pady=5)
        self.track_list = tk.Listbox(left_panel)
        self.track_list.pack(fill=tk.BOTH, expand=True)

        # Analysis controls
        ttk.Button(left_panel, text="Analyze", command=self.run_analysis).pack(fill=tk.X, pady=10)

        # Main display area
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Notebook for different views
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Analysis results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Analysis")
        self.create_results_view()

        # Visualization tab
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Visualization")

        # Create menu
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Session", command=self.clear_tracks)
        file_menu.add_command(label="Save Project")
        file_menu.add_command(label="Load Project")
        menu_bar.add_cascade(label="File", menu=file_menu)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Waveform View")
        view_menu.add_command(label="Energy Analysis")
        menu_bar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=menu_bar)

    def create_results_view(self):
        # Results treeview
        self.results_tree = ttk.Treeview(self.results_frame, columns=('Track A', 'Track B', 'Score'), show='headings')
        self.results_tree.heading('Track A', text='Track A')
        self.results_tree.heading('Track B', text='Track B')
        self.results_tree.heading('Score', text='Match Score')
        self.results_tree.pack(fill=tk.BOTH, expand=True)

        # Details panel
        details_frame = ttk.Frame(self.results_frame)
        details_frame.pack(fill=tk.X)

        ttk.Label(details_frame, text="Recommended Transitions:").pack(anchor=tk.W)
        self.transition_details = tk.Text(details_frame, height=4, wrap=tk.WORD)
        self.transition_details.pack(fill=tk.X)

    def add_tracks(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=(("Audio Files", "*.wav *.mp3 *.aiff"), ("All Files", "*.*"))
        )
        if files:
            self.tracks.extend(files)
            self.track_list.delete(0, tk.END)
            for f in self.tracks:
                self.track_list.insert(tk.END, f.split('/')[-1])

    def clear_tracks(self):
        self.tracks = []
        self.track_list.delete(0, tk.END)
        self.results_tree.delete(*self.results_tree.get_children())
        self.transition_details.delete(1.0, tk.END)

    def run_analysis(self):
        if not self.tracks:
            messagebox.showwarning("No Tracks", "Please add tracks to analyze")
            return

        try:
            results = analyze_files(self.tracks)
            self.display_results(results)
            self.show_visualizations()
        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))

    def display_results(self, results):
        self.results_tree.delete(*self.results_tree.get_children())
        for result in results:
            track_a = result['tracks'][0].file_path.split('/')[-1]
            track_b = result['tracks'][1].file_path.split('/')[-1]
            self.results_tree.insert('', tk.END, values=(track_a, track_b, f"{result['overall']:.1f}%"))

        self.results_tree.bind('<<TreeviewSelect>>', self.show_transition_details)

    def show_transition_details(self, event):
        selection = self.results_tree.selection()
        if not selection:
            return

        item = self.results_tree.item(selection[0])
        track_a = item['values'][0]
        track_b = item['values'][1]

        # Find matching analysis result
        for result in self.current_analysis:
            if (track_a in result['tracks'][0].file_path and
                    track_b in result['tracks'][1].file_path):
                details = "\n".join(result['transition_suggestions']['tips'])
                self.transition_details.delete(1.0, tk.END)
                self.transition_details.insert(tk.END, details)
                break

    def show_visualizations(self):
        # Clear previous visualizations
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        # Create waveform plot
        fig, ax = plt.subplots(figsize=(8, 4))
        audio, sr = librosa.load(self.tracks[0], sr=None)
        librosa.display.waveshow(audio, sr=sr, ax=ax)
        ax.set_title("Waveform Preview")

        canvas = FigureCanvasTkAgg(fig, self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = DJMixGUI(root)
    root.mainloop()