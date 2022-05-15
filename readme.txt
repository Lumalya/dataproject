Names
SEANG Chea-Jimmy
NIAOURI Dimitra
ROSHANFEKR Ghasem

Files
make.sh
extraction.py
preprocessing.py
clustering.py
classifying.py

All the files are made with the same pattern-section : Libraries, Global variables, functions and methods, test or main processing.
Each functions and methods are commented with their input/output, with hypothesis and what they do.
Some functions are not used since we change our decision toward the lecture's code or think it's not useful anymore, but we tried to clean-up so it is still readable.

#### Pre-launch ####

This code can be launched in a terminal (UNIX-based system). Linux's shell/bash terminal is the best, but can work with a Window Sub-System Linux or with Mac OS terminal.

#### Requirements PIP Libraries ####

1.1 - Make sure you have pip installed on your computer. In a terminal, write the following command :
            sudo apt install python3-pip
It will install it if the computer doesn't have it.

1.2 - Make sure you have pip libraries installed on your computer, write the following commands :
            pip3 install -r requirements.txt
            please use the spacy installer model on their website, to install the spacy library
            
It will install it if the computer doesn't have it, update it if outdated, or does nothing if the pip library is already installed and up-to-date.
bdb, os, string and json libraries are already installed by default.


#### How to launch our code ####

Method 1 :

2.1 - Go to the directory through the terminal, in the root of the folder.

2.2 - Write the following commands :
                chmod -R 744 *
                ./make.sh
The results will be printed in the terminal

Method 2 (if the make file doesn't work) :

2bis.1 - Go to the directory through the terminal, in the root of the folder.

2bis.2 - Write the following commands :
                chmod -R 744 *
                (python3 extraction.py)
                python3 preprocessing.py
                python3 clustering.py
                python3 classifying.py
