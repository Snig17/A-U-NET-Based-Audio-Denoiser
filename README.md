# A-U-NET-Based-Audio-Denoiser

## Introduction
Noise reduction is a crucial problem in the field of audio processing, as it significantly impacts the quality and intelligibility of sound signals. In this project, we propose a novel approach based on the U-Net architecture to tackle sound noise reduction efficiently. The U-Net is a deep learning model known for its effectiveness in image segmentation tasks, and we adapt it to handle the challenges posed by audio denoising. The introduction of the project provides an overview of the significance of noise reduction in audio processing and the growing interest in leveraging deep learning techniques for this purpose. We highlight the drawbacks of traditional methods, which often struggle to effectively remove noise while preserving the original audio content.
![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/606e3c93-e118-45b3-96cb-7af26afc3d0e)

## Data Creation: 
To create the datasets for training, I gathered english speech clean voices and environmental noises from different sources.

The clean voices were mainly gathered from LibriSpeech: an ASR corpus based on public domain audio books. I used as well some datas from SiSec. The environmental noises were gathered from ESC-50 dataset or https://www.ee.columbia.edu/~dpwe/sounds/.

For this project, I focused on 10 classes of environmental noise: tic clock, foot steps, bells, handsaw, alarm, fireworks, insects, brushing teeth, vaccum cleaner and snoring. These classes are illustrated in the image below (I created this image using pictures from https://unsplash.com).

![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/ed27fa12-74b9-4c31-8387-b8dfbc32622c)
To create the datasets for training/validation/testing, audios were sampled at 8kHz and I extracted windows slighly above 1 second. I performed some data augmentation for the environmental noises (taking the windows at different times creates different noise windows). Noises have been blended to clean voices with a randomization of the noise level (between 20% and 80%). At the end, training data consisted of 10h of noisy voice & clean voice, and validation data of 1h of sound.

To prepare the data, I recommend to create data/Train and data/Test folders in a location separate from your code folder. Then create the following structure as in the image below:

data folder structure

You would modify the noise_dir, voice_dir, path_save_spectrogram, path_save_time_serie, and path_save_sound paths name accordingly into the args.py file that takes the default parameters for the program.

Place your noise audio files into noise_dir directory and your clean voice files into voice_dir.

Specify how many frames you want to create as nb_samples in args.py (or pass it as argument from the terminal) I let nb_samples=50 by default for the demo but for production I would recommend having 40 000 or more.

Then run python main.py --mode='data_creation'. This will randomly blend some clean voices from voice_dir with some noises from noise_dir and save the spectrograms of noisy voices, noises and clean voices to disk as well as complex phases, time series and sounds (for QC or to test other networks). It takes the inputs parameters defined in args.py. Parameters for STFT, frame length, hop_length can be modified in args.py (or pass it as arguments from the terminal), but with the default parameters each window will be converted into spectrogram matrix of size 128 x 128.

Datasets to be used for training will be magnitude spectrograms of noisy voices and magnitude spectrograms of clean voices.
