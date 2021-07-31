# string-art

string-art is an algorithm to construct string-art pictures including an
install instruction from digital images.

## algorithm

the idea is to crop a picture to a given shape (e.g. circle or square) and then
place a number of nails evenly spaced around that. Then based on a random nail
the algorithm starts calculating the best route (that is with the highest
darkness) to the next nail. This continues until the simulated picture is as
close to the original input as possible.

* probably works best for b/w pictures? what kind of preprocessing is useful?


