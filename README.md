# A-U-NET-Based-Audio-Denoiser

## Introduction
Noise reduction is a crucial problem in the field of audio processing, as it significantly impacts the quality and intelligibility of sound signals. In this project, we propose a novel approach based on the U-Net architecture to tackle sound noise reduction efficiently. The U-Net is a deep learning model known for its effectiveness in image segmentation tasks, and we adapt it to handle the challenges posed by audio denoising. The introduction of the project provides an overview of the significance of noise reduction in audio processing and the growing interest in leveraging deep learning techniques for this purpose. We highlight the drawbacks of traditional methods, which often struggle to effectively remove noise while preserving the original audio content.
![image](https://github.com/Snig17/A-U-NET-Based-Audio-Denoiser/assets/127118518/606e3c93-e118-45b3-96cb-7af26afc3d0e)

## Data Creation: To create the datasets for training, I gathered english speech clean voices and environmental noises from different sources.

The clean voices were mainly gathered from LibriSpeech: an ASR corpus based on public domain audio books. I used as well some datas from SiSec. The environmental noises were gathered from ESC-50 dataset or https://www.ee.columbia.edu/~dpwe/sounds/.

For this project, I focused on 10 classes of environmental noise: tic clock, foot steps, bells, handsaw, alarm, fireworks, insects, brushing teeth, vaccum cleaner and snoring. These classes are illustrated in the image below (I created this image using pictures from https://unsplash.com).

