from noiseReduction import reduce_noise
from autotune import autotune, closest_pitch
import serial
import time
import wave
import soundfile as sf

SERIAL_PORT =  "/dev/cu.usbserial-10"
BAUD_RATE = 115200

output_wav_file = '/Users/justwhy/Downloads/output.wav'
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout = 1)

def record_audio(output_wav_file):
    # Open a WAV file for writing
    output_wav = wave.open(output_wav_file, "wb")

    # Set parameters for the WAV file
    output_wav.setnchannels(1)  # Mono
    output_wav.setsampwidth(2)  # 16-bit
    output_wav.setframerate(16000)  # Sample rate

    # Read and process data from serial
    audio_data = b""
    number = None
    start_time = time.time()

    while True:
        # Read data from serial
        data = ser.read(512)

        # Check if any data is received
        if data:
            # Check if it's audio data or a number
            if len(data) == 2:  # Assuming the number sent is of 2 bytes
                number = int.from_bytes(data, byteorder='little', signed=True)
                print("Received number:", number)
            else:
                audio_data += data

        # Check if recording of audio has stopped
        if b"ENDAUDIO" in data:
            break

        # Check timeout
        if time.time() - start_time > 120:
            print("Timeout reached. No audio received.")
            ser.close()
            output_wav.close()
            return None

    # Write audio data to WAV file
    output_wav.writeframes(audio_data)
    output_wav.close()

    print("WAV file saved as", output_wav_file)
    return number

def process_audio_file(wav_file_path, data):

    if data == '1':
        print("Noise reduction only")
        reduce_noise(wav_file_path)

    elif data == '2':
        print("Autotune only")
        autotuned = autotune(wav_file_path, closest_pitch)
        sf.write(wav_file_path, autotuned, sr = None)

    elif data == '12' or data == '21':
       print("Noise reduction & autotune")
       reduce_noise(wav_file_path)
       autotuned = autotune(wav_file_path, closest_pitch)
       sf.write(wav_file_path, autotuned, sr = None)

def main():
    num = record_audio(output_wav_file)
    process_audio_file(output_wav_file, num)

if __name__=='__main__':
    main()