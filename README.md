Cryptogram-Solver
=================

Takes a coded message with random letter assignments and returns decoded message

A cryptogram is a puzzle in which every letter is randomly assigned a new letter to create a coded message.  The program operates by comparing the letter patterns in the coded words all the words in an English dictionary with the same letter pattern.  It then makes a Python dictionary of all the possible letters each coded letter might be based on possible words with the same pattern, prunes any that are excluded by the use of the same coded letter in another word, and going back and forth shrinking the letter and words until only one choice remains.