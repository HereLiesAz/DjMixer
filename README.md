
# DJ Mix Analyzer 🎧

**DJ Mix Analyzer** is a Python-based tool for analyzing and optimizing DJ mixes. It provides features like tempo and key detection, harmonic mixing, energy analysis, and automated transition suggestions. Whether you're a beginner or a professional DJ, this tool helps you create seamless mixes with ease.

---

## Features ✨

- **Tempo & Key Detection**: Automatically detect BPM and musical key of tracks.
- **Harmonic Mixing**: Use the Camelot Wheel to find compatible tracks.
- **Energy Analysis**: Predict crowd energy levels for better set planning.
- **Transition Suggestions**: Get recommendations for smooth transitions between tracks.
- **Multi-Track Mixing**: Analyze and optimize sequences of 3+ tracks.
- **Visualization**: View waveforms, beat grids, and energy trends.
- **Cloud Integration**: Sync playlists and preferences across devices.
- **MIDI Support**: Integrate with DJ software like Traktor and Serato.

---

## Installation 🛠️

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dj-mix-analyzer.git
   cd dj-mix-analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .\.venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install TensorFlow (required for VGGish features):
   ```bash
   pip install tensorflow
   ```

---

## Usage 🚀

### Command Line Interface
Run the analyzer from the command line:
```bash
python main.py
```

### GUI Mode
Launch the graphical user interface:
```bash
python gui/dj_mix_gui.py
```

### Example Workflow
1. Add tracks to analyze:
   ```python
   from analyzer.mix_analyzer import MixAnalyzer
   analyzer = MixAnalyzer(['track1.wav', 'track2.wav'])
   matches = analyzer.analyze_matches()
   ```

2. View transition suggestions:
   ```python
   for match in matches:
       print(f"Match between {match['tracks'][0]} and {match['tracks'][1]}")
       print(f"Compatibility: {match['overall']:.1f}%")
   ```

3. Export a mix:
   ```python
   from export.mix_exporter import MixExporter
   exporter = MixExporter()
   exporter.export_mix(tracks, transitions, output_file='my_mix.wav')
   ```

---

## File Structure 📂
```
dj-mix-analyzer/
├── analyzer/              # Core analysis logic
├── utils/                 # Utility functions (BPM, key, etc.)
├── midi/                  # MIDI controller integration
├── cloud/                 # Cloud sync functionality
├── ai/                    # AI-based recommendations
├── export/                # Mix export tools
├── visualization/         # Data visualization
├── gui/                   # Graphical user interface
├── main.py                # Entry point for CLI
├── requirements.txt       # Project dependencies
└── README.md              # This file
```

---

## Dependencies 📦

- **Core Libraries**:
    - `librosa`: Audio analysis
    - `numpy`: Numerical computations
    - `scikit-learn`: Machine learning
    - `tensorflow`: VGGish embeddings

- **Visualization**:
    - `matplotlib`: Plotting
    - `seaborn`: Enhanced visualizations

- **GUI**:
    - `tkinter`: Graphical interface
    - `matplotlib.backends.backend_tkagg`: Embedding plots in GUI

---



## Acknowledgments 🙏

- **librosa**: For audio analysis tools.
- **TensorFlow Hub**: For the VGGish model.
- **madmom**: For beat tracking.
- **scikit-learn**: For machine learning utilities.

---


