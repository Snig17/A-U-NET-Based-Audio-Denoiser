# A-U-NET-Based-Audio-Denoiser

## Introduction
Noise reduction is a crucial problem in the field of audio processing, as it significantly impacts the quality and intelligibility of sound signals. In this project, we propose a novel approach based on the U-Net architecture to tackle sound noise reduction efficiently. The U-Net is a deep learning model known for its effectiveness in image segmentation tasks, and we adapt it to handle the challenges posed by audio denoising. The introduction of the project provides an overview of the significance of noise reduction in audio processing and the growing interest in leveraging deep learning techniques for this purpose. We highlight the drawbacks of traditional methods, which often struggle to effectively remove noise while preserving the original audio content.
![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/606e3c93-e118-45b3-96cb-7af26afc3d0e)

## Data Creation: 
To create the datasets for training, I gathered english speech clean voices and environmental noises from different sources.

The clean voices were mainly gathered from LibriSpeech(http://www.openslr.org/12/): an ASR corpus based on public domain audio books. I used as well some datas from SiSec(https://sisec.inria.fr/sisec-2015/2015-two-channel-mixtures-of-speech-and-real-world-background-noise/). The environmental noises were gathered from ESC-50 dataset or https://www.ee.columbia.edu/~dpwe/sounds/.

For this project, I focused on 10 classes of environmental noise: tic clock, foot steps, bells, handsaw, alarm, fireworks, insects, brushing teeth, vaccum cleaner and snoring. These classes are illustrated in the image below (I created this image using pictures from https://unsplash.com).

![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/ed27fa12-74b9-4c31-8387-b8dfbc32622c)
To create the datasets for training/validation/testing, audios were sampled at 8kHz and I extracted windows slighly above 1 second. I performed some data augmentation for the environmental noises (taking the windows at different times creates different noise windows). Noises have been blended to clean voices with a randomization of the noise level (between 20% and 80%). At the end, training data consisted of 10h of noisy voice & clean voice, and validation data of 1h of sound.

To prepare the data, I recommend to create data/Train and data/Test folders in a location separate from your code folder. Then create the following structure as in the image below:

![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/fd51b61d-1b33-40f8-af8b-afff71ba5590)

You would modify the noise_dir, voice_dir, path_save_spectrogram, path_save_time_serie, and path_save_sound paths name accordingly into the args.py file that takes the default parameters for the program.

Place your noise audio files into noise_dir directory and your clean voice files into voice_dir.

Specify how many frames you want to create as nb_samples in args.py (or pass it as argument from the terminal) I let nb_samples=50 by default for the demo but for production I would recommend having 40 000 or more.

Then run python main.py --mode='data_creation'. This will randomly blend some clean voices from voice_dir with some noises from noise_dir and save the spectrograms of noisy voices, noises and clean voices to disk as well as complex phases, time series and sounds (for QC or to test other networks). It takes the inputs parameters defined in args.py. Parameters for STFT, frame length, hop_length can be modified in args.py (or pass it as arguments from the terminal), but with the default parameters each window will be converted into spectrogram matrix of size 128 x 128.

Datasets to be used for training will be magnitude spectrograms of noisy voices and magnitude spectrograms of clean voices.

## Training
The model used for the training is a U-Net, a Deep Convolutional Autoencoder with symmetric skip connections. U-Net was initially developed for Bio Medical Image Segmentation. Here the U-Net has been adapted to denoise spectrograms.

As input to the network, the magnitude spectrograms of the noisy voices. As output the Noise to model (noisy voice magnitude spectrogram - clean voice magnitude spectrogram). Both input and output matrix are scaled with a global scaling to be mapped into a distribution between -1 and 1.

Many configurations have been tested during the training. For the preferred configuration the encoder is made of 10 convolutional layers (with LeakyReLU, maxpooling and dropout). The decoder is a symmetric expanding path with skip connections. The last activation layer is a hyperbolic tangent (tanh) to have an output distribution between -1 and 1. For training from scratch the initial random weights where set with He normal initializer.

Model is compiled with Adam optimizer and the loss function used is the Huber loss as a compromise between the L1 and L2 loss.

At the end, I obtained a training loss of 0.002129 and a validation loss of 0.002406. Below a loss graph made in one of the trainings.

![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/d7f4449b-a20f-4b31-ad09-b892f3049c77)

## Prediction

For prediction, the noisy voice audios are converted into numpy time series of windows slightly above 1 second. Each time serie is converted into a magnitude spectrogram and a phase spectrogram via STFT transforms. Noisy voice spectrograms are passed into the U-Net network that will predict the noise model for each window (cf graph below). Prediction time for one window once converted to magnitude spectrogram is around 80 ms using classical CPU.

![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/bde5346a-7946-44d9-8236-3252dec92193)


Then the model is subtracted from the noisy voice spectrogram (here I apply a direct subtraction as it was sufficient for my task, we could imagine to train a second network to adapt the noise model, or applying a matching filter such as performed in signal processing). The "denoised" magnitude spectrogram is combined with the initial phase as input for the inverse Short Time Fourier Transform (ISTFT). Our denoised time serie can be then converted to audio (cf graph below).

![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/ecf52382-5f07-4e6c-b7d9-a3b768947d01)



