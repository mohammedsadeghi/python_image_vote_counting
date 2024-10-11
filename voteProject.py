import cv2
import numpy as np

# Load the image
image_path = "vote1.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
original_image = cv2.imread(image_path)
cv2.imwrite("step_1_loaded_image.jpg", original_image)

# Preprocess the image
blurred = cv2.GaussianBlur(image, (5, 5), 0)
cv2.imwrite("step_2_blurred_image.jpg", blurred)
_, thresholded = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("step_3_thresholded_image.jpg", thresholded)

# Find contours
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_image = original_image.copy()
cv2.drawContours(contour_image, contours, -1, (255, 0, 0), 2)
cv2.imwrite("step_4_contours.jpg", contour_image)

# Filter and sort the contours
squares = []
for contour in contours:
    area = cv2.contourArea(contour)
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / float(h)
    
    if area > 500 and area < 5000 and 0.9 < aspect_ratio < 1.1:  # Adjusted the area and aspect ratio thresholds
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            squares.append(approx)

# Draw filtered squares
filtered_squares_image = original_image.copy()
for square in squares:
    cv2.drawContours(filtered_squares_image, [square], -1, (0, 255, 0), 2)
cv2.imwrite("step_5_filtered_squares.jpg", filtered_squares_image)

# Sort squares based on their position
squares = sorted(squares, key=lambda x: (x[0][0][1], x[0][0][0]))

# Check if squares are filled
votes = []
for i, square in enumerate(squares):
    mask = np.zeros_like(image)
    cv2.drawContours(mask, [square], -1, 255, -1)
    mean_val = cv2.mean(image, mask=mask)[0]
    
    if mean_val < 180:  # Adjusted threshold
        votes.append(i)

# Draw squares and votes on the original image
voted_image = original_image.copy()
for i, square in enumerate(squares):
    if i in votes:
        color = (0, 255, 0)  # Green for votes
        label = "Voted"
    else:
        color = (255, 0, 0)  # Blue for detected squares
        label = "Not Voted"
    
    cv2.drawContours(voted_image, [square], -1, color, 2)
    cv2.putText(voted_image, label, tuple(square[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
cv2.imwrite("step_6_voted_image.jpg", voted_image)

# Map votes to nominees
nominees = [
    "عبدالحمید بامنیر",
    "حسین ابراهیم پور",
    "ابوالفضل حلوایی",
    "محسن بهپور",
    "بابک عالمی",
    "مهدی سبزواری",
    "روح الله نخعی",
    "علی عالی انوری",
    "رضا نوری"
]

vote_counts = {nominee: 0 for nominee in nominees}

for vote in votes:
    if vote < len(nominees):
        vote_counts[nominees[vote]] += 1

# Print vote counts
for nominee, count in vote_counts.items():
    print(f"{nominee}: {count} votes")

# Save the final output image
output_image_path = "/Users/user/Documents/vote/vote_result.jpg"
cv2.imwrite(output_image_path, voted_image)

print(f"Processed image saved as {output_image_path}")
