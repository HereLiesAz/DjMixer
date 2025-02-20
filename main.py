from analyzer.mix_analyzer import MixAnalyzer
from realtime.realtime_analyzer import RealTimeAnalyzer
from dj_software.traktor_integration import TraktorIntegration
from midi.midi_mapper import MIDIMapper
from playlist.playlist_generator import PlaylistGenerator
from cloud.cloud_sync import CloudSync
from ai.track_recommender import TrackRecommender
from visualization.advanced_visualizer import AdvancedVisualizer
from utils.bpm_key_adjuster import BPMKeyAdjuster
from export.mix_exporter import MixExporter
from ai.crowd_energy_predictor import CrowdEnergyPredictor
from analyzer.multi_track_mixer import MultiTrackMixer
from analyzer.song_analyzer import SongAnalyzer

def main():
    mode = input("""Choose mode:
1. File Analysis
2. Real-Time Analysis
3. DJ Software Integration
4. MIDI Mapping
5. Playlist Generation
6. Cloud Sync
7. AI Recommendations
8. Advanced Visualization
9. Multi-Track Mixing
10. Full Auto-Mix
Your choice: """)

    if mode == '1':
        analyzer = MixAnalyzer(['track1.wav', 'track2.wav', 'track3.wav'])
        matches = analyzer.analyze_matches()
        # ... (print results)

    elif mode == '2':
        rt_analyzer = RealTimeAnalyzer()
        rt_analyzer.start_monitoring()

    elif mode == '9':
        files = ['track1.wav', 'track2.wav', 'track3.wav']
        tracks = [SongAnalyzer(f).analyze() for f in files]
        mixer = MultiTrackMixer(tracks)
        sequence = mixer.find_optimal_sequence()
        # ... (print sequence)

    elif mode == '10':
        files = ['track1.wav', 'track2.wav', 'track3.wav']
        tracks = [SongAnalyzer(f).analyze() for f in files]
        mixer = MultiTrackMixer(tracks)
        sequence = mixer.find_optimal_sequence()
        adjuster = BPMKeyAdjuster()
        adjusted_tracks = adjuster.adjust_sequence(tracks, sequence)
        exporter = MixExporter()
        exporter.export_mix(adjusted_tracks, [{'fade_samples': 44100}]*2)
        print("Mix exported!")

if __name__ == "__main__":
    main()

    import sys
print(sys.path)