# Corner Detector

**Instructions**:

1) Use the corner detection function available at “Skimage” library and detect the corners of the
given reference image as well as the transformed versions.

2) Define a descriptor for the detected corners and find the matching corners between the
reference image and each of the transformed versions. Then plot the matching corners using
a line from the reference to the transformed image.

An example of a simple descriptor is creating a nxn window around the corner point and
finding the average intensity. Then creating a 1x2 descriptor vector consists of the corner pixel
intensity value and the average intensity that you calculated from nxn window. Once you
define the descriptor, then you can use Euclidean distance to find the similarity between each
detected corner at the reference image and the transformed one. Finally, based on the similarity,
you can find the matching ones and plot a line in between.
