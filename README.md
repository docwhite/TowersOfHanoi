Towers Of Hanoi
============

Puzzle solver. To use in Maya, written in Python.

![](https://github.com/docwhite/TowersOfHanoi/raw/master/images/ui.png)

## What is the Towers Of Hanoi Puzzle?
*(...extracted from Wikipedia)* The Tower of Hanoi is a mathematical game or puzzle. It consists of three rods, and a number of disks of different sizes which can slide onto any rod. The puzzle starts with the disks in a neat stack in ascending order of size on one rod, the smallest at the top, thus making a conical shape.

The objective of the puzzle is to move the entire stack to another rod, obeying the following simple rules:
* Only one disk can be moved at a time.
* Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack i.e. a disk can only be moved if it is the uppermost disk on a stack.
* No disk may be placed on top of a smaller disk.

With three disks, the puzzle can be solved in seven moves. The minimum number of moves required to solve a Tower of Hanoi puzzle is `2n - 1`, where n is the number of disks.

## Installation
First of all, if you are not familiarized with git and you don't know how the cloning stuff works, just keep it simple:
Download all this project as a ZIP file (button on right side of the screen). Then, once you have extracted all the contents on your Desktop or wherever you want..
* Uncompress the ZIP file you just downloaded
* Open `startup.py` with Notepad or your favourite text editor
* Copy all the content from it.
* Paste it to the Script Editor in Maya
* Execute the code
* You will be asked to point the location where all the scripts are. You must point to the folder called `script` inside the uncompressed  folder in which you have uncompressed the ZIP file.
* The UI should be created, then you can click on "Instructions" in order to get started as soon as possible.

This method for including the pointed folder as a sys.path for maya to access the files has been adapted from Jared Auty's wonderful scripting project, which you can download here  http://bit.ly/1kDUXhj

## Usage
It is stated in the **Instructions** tab inside the *Graphics User Interface* I build, but I will write it here as well:
* 1. Select the numbers of disks you want to play with.
* 2. Click 'Place Disks' first. Then you will see that the disks has been brought to scene.
* 3. Click 'Solve it!'. A lot of keyframes will appear on your timel
ine. Furthermore you will be able to see each movement written down if you see the Script Editor window.
* 4. If you want to change the number of disks FIRST CLEAR the scene by pressing 'Clear All'. If you skip this step you might crash the program.
* 5. Once you are finished press the 'Exit' button and it will delete all the elements that have been created for you

## More
If you are interested on how I used recursion in order to get this thing working I include a file called `simplifiedPuzzle.py` which is for you to try to figure out what is going on in each step. This file doesn't require the maya library, it is just a snippet that helps to see the flow.

Feel free as well to read the documentation HTML files in the `documentation` folder. If you are interested in seeing the flowchart of my script here I made an image to illustrate it:

![](https://github.com/docwhite/TowersOfHanoi/raw/master/images/flowchart.png)

*Ramon Blanquer (NCCA) ©*
