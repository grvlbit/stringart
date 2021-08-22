# string-art

string-art is an algorithm to construct string-art pictures.

![Mona Lisa stringart](stringart/demo/results_ml.png "Mona Lisa stringart")

This project has been inspired by the magnificant works of [Petros
Vrellis](http://artof01.com/vrellis/works/knit.html).

## Algorithm

The idea is to crop a picture to a given shape (e.g. circle) and then
place a number of nails evenly spaced around that. Then based on a random nail
the algorithm starts calculating the best route (that is the route with the highest
darkness) to the next nail. This procedure is continued until a maximum number
of iterations is reached or the simulated picture matches the input. 

## Usage

The general idea of how to use the module in your own scripts is presented in
the `__main__.py` routine. 

## Notes

This is a relatively naive implementation. The problem scales with the number
of nails, iterations as well as the resolution of the input. 

* Use cropped images roughly 300x300px
* Works best with pictures with high contrast
* Works best on portraits


