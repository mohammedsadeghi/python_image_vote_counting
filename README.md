# Voting Image Processing using OpenCV

This project processes an image of voting squares using **OpenCV** to detect and count votes based on filled squares. It walks through the steps of loading an image, preprocessing, detecting contours, filtering for square shapes, and determining which squares are filled to identify votes. The project saves intermediate images at each step of the process to provide a clear overview of the operations being performed.

## Features

- **Image Preprocessing**: The image is blurred and thresholded to improve contour detection.
- **Contour Detection**: The project identifies contours and filters them based on size and shape to detect square voting areas.
- **Vote Recognition**: It checks whether each detected square is filled (interpreted as a vote) by analyzing the pixel intensity within each square.
- **Annotated Images**: The project generates and saves images at various stages, including the final image with detected and marked voting areas.
- **Nominee Vote Counting**: Votes are mapped to specific nominees and the total number of votes per nominee is printed.

## Dependencies

The project requires the following Python libraries:

```bash
pip install opencv-python numpy