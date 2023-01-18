# Copy paste challenge

### About this Submission:
Running `python main.py` will print the solutions to the given (below) strings, as well as some other edge cases. 

Editing the `strs` variable in `main.py` will enable you to change the test strings. 


## The Challenge Description
```
[
  "the big red[CTRL+C] fox jumps over [CTRL+V] lazy dog.",
  "[CTRL+V]the tall oak tree towers over the lush green meadow.",
  "the sun shines down[CTRL+C] on [CTRL+V][CTRL+C] the busy [CTRL+V].",
  "[CTRL+V]the tall oak tree towers over the lush green meadow.",
  "a majestic lion[CTRL+C] searches for [CTRL+V] in the tall grass.",
  "the shimmering star[CTRL+X]Twinkling in the dark, [CTRL+V] shines bright.",
  "[CTRL+X]a fluffy white cloud drifts [CTRL+V][CTRL+C] across the sky, [CTRL+V]",
]
```

The challenge is to analyse these strings for any instances of [CTRL+C] and [CTRL+V]. When [CTRL+C] is encountered, the contents of the string before it should be 'copied' to a clipboard. Upon any instance of [CTRL+V] in the string, this clipboard should be pasted in its place. If [CTRL+V] is encountered before any corresponding [CTRL+C] then it should simply paste nothing.
### Rewards:
 - :five:  Points are awarded for a working algorithm as described above
 - :three:  Further points are awarded for supporting [CTRL+X], which should remove the preceding text before copying it to the clipboard
 - :two:  Further points are awarded for validating your solution with a collection of unit tests
### Example:
For this example input:
`challenge("the first[CTRL+C] Coding Challenge was [CTRL+V] string manipulation task")`

Your solution might output:
`"the first Coding Challenge was the first string manipulation task"`
