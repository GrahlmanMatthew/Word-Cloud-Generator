# Word Cloud Generator
## Algorithm Overview
This is a Word Cloud Generator, which will attempt to place `w` number of the most common words from an input text file, `f`, on an image of size `NxN`. Below I've summarized my implementation and some of the considerations taken:
1. Collect input parameters `w`, `f`, and `N`
2. Build Dictionary of `stopwords`, which are uninteresting words to blacklist.
3. Build the `vocabulary` Dictionary, which are the words contained in `f` that are NOT in the `stopwords` Dictionary.
4. Generate an `NxN` grid to optimize placement of words in the generated Word Cloud, as it will only try to place words in places where two lines of the same colour/ thickness intersect perpendicularly.
5. Attempts to place each word on a square in the `NxN` grid. A valid placement is:
      1. When the collision box around the word does NOT collide with any other placed word's collision box. For this I used the `does_overlap` function from the `Axis Aligned Bounding Box (AABB) Trees` library where the tree contains the coordinates of the word boxes for each placed word. This allowed for efficient checks to see whether a word placement would overlap with an already placed word.
      2. When the collision box around the word lies within the `NxN` grid's coordinates
6. Upon successful execution, the output Word Cloud image will be saved to `output/wordcloud.png`

## Sample Outputs
The following Word Cloud was generated using the novel 1984 by George Orwell's:

<img src="./output/grid.png" width="250" height="250"> <img src="./output/word-bounds.png" width="250" height="250"> <img src="./output/wordcloud.png" width="250" height="250">
- Left most image is the generated `NxN` grid mentioned in A.O. #4
- Middle image is a visualization of the word-box collision boxes mentioned in in A.O. #5.1
- Right most image is the generated Word Cloud image mentioned in in A.O. #6

### Sample Execution
Clone the repository, install the dependencies via `pip`, then from the terminal run: `python main.py`

Upon execution, you will be prompted for 3 pieces for information;
1. Input text (.txt) file `f`, must be in the `input` directory
2. Number of words `w`
3. Image dimension `N`
   
## References
1. [1984 by George Orwell, Uploaded by Project Gutenberg Australia](https://gutenberg.net.au/ebooks01/0100021.txt)
2. [StackOverflow - Algorithm to Implement Word Cloud like Wordle](https://stackoverflow.com/questions/342687/algorithm-to-implement-a-word-cloud-like-wordle)
3. [Wordle by Jonathan Feinberg](http://static.mrfeinberg.com/bv_ch03.pdf)
4. [Known English Stop Words by PyTagCloud](https://github.com/atizo/PyTagCloud/blob/master/pytagcloud/lang/stop/english)
5. [Fonts for Word Clouds by PyTagCloud](https://github.com/atizo/PyTagCloud/tree/master/pytagcloud/fonts)
6. [AABBTree PyPi Project by Kenneth Hart](https://pypi.org/project/aabbtree/)