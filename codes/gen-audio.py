import numpy as np
import soundfile as sf
import argparse
import tensorflow as tf
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from scipy.signal import resample
from tqdm import tqdm
import os
import json
import nltk

# Ensure nltk punkt is downloaded
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Constants
# DATA_CACHE_DIR = "/mundus/abadawi696/slibrilight/download/librilight/small"
DATA_CACHE_DIR = "/mundus/abadawi696/slibrilight/slibrilight-medium/download/librilight/medium"
VOCODER_SR = 22050
SR = 16000
MAX_TOKEN_LENGTH = 2048  # This is your model's token limit

def process_chunk(text, processor, fastspeech2, mb_melgan, line_wavs, silence):
    input_ids = processor.text_to_sequence(text)
    if len(input_ids) > MAX_TOKEN_LENGTH:
        # If still too long, split by commas and process each as separate
        sub_chunks = text.split(',')
        for sub_chunk in sub_chunks:
            process_sub_chunk(sub_chunk.strip(), processor, fastspeech2, mb_melgan, line_wavs, silence)
    else:
        generate_speech(input_ids, fastspeech2, mb_melgan, line_wavs, silence)

def process_sub_chunk(text, processor, fastspeech2, mb_melgan, line_wavs, silence):
    input_ids = processor.text_to_sequence(text)
    # Final check to avoid any mishaps
    if len(input_ids) > MAX_TOKEN_LENGTH:
        input_ids = input_ids[:MAX_TOKEN_LENGTH]  # Force truncation if all else fails
    generate_speech(input_ids, fastspeech2, mb_melgan, line_wavs, silence)

# def generate_speech(input_ids, fastspeech2, mb_melgan, line_wavs, silence):
#     _, mel_after, _, _, _ = fastspeech2.inference(
#         input_ids=tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
#         speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
#         speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
#         f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
#         energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
#     )
#     wav = mb_melgan.inference(mel_after)[0, :, 0]
#     wav = resample(wav, int(len(wav) * SR / VOCODER_SR))
#     line_wavs.append(wav)
#     line_wavs.append(silence)  # Add a short silence after each sentence

def generate_speech(input_ids, fastspeech2, mb_melgan, line_wavs, silence):
    try:
        _, mel_after, _, _, _ = fastspeech2.inference(
            input_ids=tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
            speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
            speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        )
        wav = mb_melgan.inference(mel_after)[0, :, 0]
        wav = resample(wav, int(len(wav) * SR / VOCODER_SR))
        line_wavs.append(wav)
        line_wavs.append(silence)  # Add a short silence after each sentence
    except tf.errors.InvalidArgumentError as e:
        print(f"Error during model inference: {e}")
        # Optionally, you can log this error to a file or take other recovery actions.
    except Exception as e:
        print(f"Unhandled exception: {e}")
        # General exception catch, which could log or handle unexpected errors.

def get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--save-dir", help="Output path to store the features", required=True)
    parser.add_argument("--nshard", type=int, default=1)
    parser.add_argument("--rank", type=int, default=0)
    return parser

def get_shard_range(tot, nshard, rank):
    assert rank < nshard and rank >= 0, f"invalid rank/nshard {rank}/{nshard}"
    start = round(tot / nshard * rank)
    end = round(tot / nshard * (rank + 1))
    assert start < end, f"start={start}, end={end}"
    print(f"rank {rank + 1} of {nshard}, process {end-start} ({start}-{end}) out of {tot}")
    return start, end

def main():
    parser = get_parser()
    args = parser.parse_args()
    fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-ljspeech-en")
    mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-ljspeech-en")
    processor = AutoProcessor.from_pretrained("tensorspeech/tts-fastspeech2-ljspeech-en")

    shard_filenames = []
    for root, dirs, files in os.walk(DATA_CACHE_DIR):
        for file in files:
            if file.endswith(".json"):
                shard_filenames.append(os.path.join(root, file))
    shard_filenames = sorted(shard_filenames)
    start, end = get_shard_range(len(shard_filenames), args.nshard, args.rank)
    shard_filenames = shard_filenames[start:end]

    silence_duration = int(0.5 * SR)
    silence = np.zeros(silence_duration)

    for file_i, json_file in enumerate(shard_filenames):
        print(f"Processing file {file_i + 1}/{len(shard_filenames)}")
        with open(json_file, "r") as f:
            data = json.load(f)

        input_dir = os.path.dirname(json_file)
        relative_dir = os.path.relpath(input_dir, start=DATA_CACHE_DIR)
        save_path = os.path.join(args.save_dir, relative_dir, os.path.basename(json_file).split('.')[0])
        os.makedirs(save_path, exist_ok=True)

        for audio_key, text in data.items():
            print(f"Processing text for {audio_key}")
            if os.path.exists(os.path.join(save_path, f'{audio_key}.wav')):
                continue

            text = text.strip()
            sentences = sent_tokenize(text)
            line_wavs = []
            for sentence in sentences:
                process_chunk(sentence, processor, fastspeech2, mb_melgan, line_wavs, silence)

            if line_wavs:
                story_wav = np.concatenate(line_wavs)
                sf.write(os.path.join(save_path, f'{audio_key}.wav'), story_wav, SR, "PCM_16")

if __name__ == "__main__":
    main()
gen
