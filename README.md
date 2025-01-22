# Audio-Volume-Tone
Python code to generate tones and control the volume setting for the output

There are two versions of this implementation. tone-generator-w is windows specific as there is no linux implementation of pcaw. tone-generator is a generic version that should work on all python implementations however it uses master volume control and doesn't read the original value.

The developer using Python Core Advanced Windows (pcaw) can't set a scalar volume. It needs to be set in decibels. 27% volume is approximately -20dB

The variable tone is an array of values including floating point values that would map out to a 44.1 kHz sample rate over two seconds = 88,200 values. 

tone-generator-w has examples of triangle, square and sine wave generation plus plots of the waves
