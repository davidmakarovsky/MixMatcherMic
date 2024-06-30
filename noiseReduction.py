import noisereduce as nr
import librosa
import soundfile as sf



def reduce_noise(wav_file_path, reduction_strength=0.5):
    # Load the audio file
    audio_data, sr = librosa.load(wav_file_path, sr=None)
    
    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sr, stationary=False, prop_decrease=reduction_strength, n_std_thresh_stationary=1.5)
    
    # Write noise-reduced audio back to the same file path
    sf.write(wav_file_path, reduced_noise, sr)
    
    return wav_file_path
