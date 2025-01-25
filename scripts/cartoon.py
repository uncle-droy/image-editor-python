import cv2, time
import numpy as np

start_time = time.time()
print(start_time)

def cartoonify_image(image_path, undo_number, save_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print("Could not open or find the image.")
        return
    
    # Resize image to a smaller size for faster processing
    height, width = img.shape[:2]
    img_small = cv2.resize(img, (width // 2, height // 2))
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to remove noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    print("Initialized")
    # color = cv2.bilateralFilter(img_small, 9, 75, 75)

    # # Convert to grayscale
    # gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
    
    # # Apply median blur to remove noise
    gray = cv2.medianBlur(gray, 17)
    
    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, 9, 9)
    
    # Apply bilateral filter to the original image to smooth it
    color = cv2.bilateralFilter(img_small, 15, 60, 200)
    print('Step2')
    # Reduce the number of colors in the image using k-means clustering
    Z = color.reshape((-1, 3))
    Z = np.float32(Z)
    
    # Define criteria and apply k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 35  # Number of colors
    _, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    print('Step3')
    center = np.uint8(center)
    res = center[label.flatten()]
    reduced_color_image = res.reshape((color.shape))
    edges = cv2.resize(edges, (width // 2, height // 2))

    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)
    
    # Resize back to original size
    reduced_color_image = cv2.resize(reduced_color_image, (width, height))
    edges = cv2.resize(edges, (width, height))
    
    # Convert edges to a 3-channel image
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    if reduced_color_image.shape != edges_colored.shape:
        edges_colored = cv2.resize(edges_colored, (reduced_color_image.shape[1], reduced_color_image.shape[0]))

    # Combine edges with the reduced color image
    cartoon = cv2.bitwise_and(reduced_color_image, edges_colored)
    print('Step4')
    cartoon = cv2.resize(cartoon, (width, height))
    cartoon = cv2.addWeighted(cartoon, 0.8, img, 0.2, 0)
    
    cv2.imwrite(save_path, cartoon)
    undo_number+=1
# # Example usage
# image_path = 'girl5.jpg'  # Replace with your image path
# cartoon_image = cartoonify_image(image_path)
# if cartoon_image is not None:
#     display_image('Cartoonified Image', cartoon_image)
# print(time.time())
# print('Done in: ', time.time() - start_time)