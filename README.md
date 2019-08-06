# Research Apps
Code for research that I use to automate my workflow.

ClinicProgram: Is a program being used by the clinic at Foothills Hospital which takes their dataset and splices it into individual patients. It's mean't to have the simplest UI it can an still be very functional.

AutoFooof: Script that creates fooof_objects which can be used by CreateFigures for further analysis. Also cleans and filters the signal. It does what I used to do in 12 hours, in 30 minutes!

CreateFigures: Gui.py launches a graphical user interface which is used to launch a subset of scripts that can be used to analyze the output of AutoFooof, and then collect the data from said output. Using that data it creates figures showcasing section by section how the results differ, and also creates an excel file for the raw data so that it can be easily accessed for further analysis.

Modified CreateFigures: Acts in a similar fashion to the original but runs a different type of dataset, and creates its excel files in a different way as well. A lot of the code is rewritten from createFigures and from what I can tell it's also a bit faster.

DiscardFigures: An app that makes data analysis from autoFoof really quick by treating it sort of like a game. Shows figures one by one from autoFoof, where you can swipe left for bad data and right for good data, the bad data gets noted and stored in a text file which createFigures can use to ignore the bad data.

NoteMaker: Is an app that I created for my self that automates the process of taking notes in a specific context, and minimized how much I needed to type.
