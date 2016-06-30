# Daily activity recognition from egocentric images
##### from manual annotation to automatic classification


## Abstract

By analysing people way of life we can create methods of prevention and intervention for
human behaviour derived diseases. Lifelogging allow us to obtain information, through
image capture, of the daily life and the environment in which we move. However, we
need to classify those images in order to obtain information, and then to analyse that data
to detect behaviour patterns that may be affecting people. But how can we classify thou-
sand of images in a quick way? Automatic classification algorithms, such as convolutional
neural networks based techniques and deep learning have shown promising results when
classifying images. This work introduces the challenge, first, of realizing a tool for a man-
ual classification, with a website showing images that allow us to easily classify images
using batches. Such a tool allows us to create a data set of nearly 20.000 images to, in
the second part of the project, realize a fine-tuning over a convolutional neural network
trained with ImageNet. After that fine-tuning, the convolutional neural network is com-
bined to obtain the features from the images in order to train a Random Decision Forest
classifier. Finally the results are studied. The global accuracy for the CNN system based
is that of 58%. A better solution is obtained when combining CNN’s and RDF’s reaching
up to 85% of global accuracy. Thus concluding that the classification system based on
training a RDF with the data provided by the CNN, image features and probabilities, is
the system offering better results.

### Structure
This repository contains the report and the code of my bachelor project. The report is in the file called report.pdf

The project is divided in two sections, the Annotation tool and the Activity recognition.

### Annotation tool

The folder called Annotation tool contains the application for manual classification. Check the Docs folder and follow the instructoins to get the application working

### Activity recognition

The folder called Activity recognition contains the notebooks with all the information to test the classifier (use the links below to get the pre-trained models)
It also contains the notebooks, and the datasets in case you want to fine-tune the network from scratch.


### Pre-trained models

Pre-trained models can be found in the links:

[AlexNet pre-trained model and RDF's](https://drive.google.com/file/d/0B7a0tfZkiEQmQ1YxR3V4Y2J5NjQ/view?usp=sharing)

[GoogLeNet pre-trained model and RDF's](https://drive.google.com/file/d/0B7a0tfZkiEQmeWplZkY0T0lYZDg/view?usp=sharing)


### Acknowledgments

I would like to acknowledge the people who made possible this work. First of all, I
would like to thank Petia Radeva, who offer me to opportunity to start this work. I would
also like to thank Mariella Dimiccoli, my supervisor, who always had a good piece of
advice and pushed me in order to improve my work.
I would also want to acknowledge my parents, who have always trusted in me, perhaps
too much. And my sister who has always been there to lend a hand and willing to share
her experience.
To my friends and colleagues from Universitat de Barcelona. They know I just did it
for the lulz because Together we lose.
Finally, I would like to thank Neurcar. She did not want me to write these acknowl-
edgments, she is the reason why I did it though.
