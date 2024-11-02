import cv2
import numpy as np
from cv2 import aruco
from PIL import Image

dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
parameters =  aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)
cap = cv2.VideoCapture(1)

def FindBoard(projectBack=False):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        parameters =  aruco.DetectorParameters()
        corners, ids, rejectedImgPoints = detector.detectMarkers(frame)
        dist_coeffs = np.zeros((4, 1))
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        if len(corners) == 4:
            id_corner_pairs = list(zip(ids.flatten(), corners))

            id_corner_pairs.sort(key=lambda x: x[0])
            sorted_corners = [corner for _, corner in id_corner_pairs]
            pts_src = np.array([corner[0][0] for corner in sorted_corners], dtype="float32")

            side_length = 300 
            pts_dst = np.array([
                [0, 0],
                [side_length - 1, 0],
                [0, side_length - 1],
                [side_length - 1, side_length - 1],
            ], dtype="float32")

            h, _ = cv2.findHomography(pts_src, pts_dst)

            warped_frame = cv2.warpPerspective(frame, h, (side_length, side_length))
            #warped_frame = cv2.flip(warped_frame, 1)
            #cv2.destroyAllWindows()
            #cv2.imshow("Board", warped_frame)
            return (warped_frame, (frame, warped_frame, pts_dst, pts_src))
            

        else:
            cv2.imshow('Frame', frame_markers)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

def ProjectBack(img_data, startSquare, endSquare):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        parameters =  aruco.DetectorParameters()
        corners, ids, rejectedImgPoints = detector.detectMarkers(frame)
        dist_coeffs = np.zeros((4, 1))
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        if len(corners) == 4:
            id_corner_pairs = list(zip(ids.flatten(), corners))

            id_corner_pairs.sort(key=lambda x: x[0])
            sorted_corners = [corner for _, corner in id_corner_pairs]
            pts_src = np.array([corner[0][0] for corner in sorted_corners], dtype="float32")

            side_length = 300 
            pts_dst = np.array([
                [0, 0],
                [side_length - 1, 0],
                [0, side_length - 1],
                [side_length - 1, side_length - 1],
            ], dtype="float32")

            h, _ = cv2.findHomography(pts_src, pts_dst)

            warped_frame = cv2.warpPerspective(frame, h, (side_length, side_length))

            warped_frame = DrawArrow(warped_frame, startSquare, endSquare)
            h_inv, _ = cv2.findHomography(pts_dst, pts_src)

            warped_back = cv2.warpPerspective(warped_frame, h_inv, (frame.shape[1], frame.shape[0]))

            # Ensure pts_src is ordered as a closed quadrilateral in clockwise or counterclockwise order
            ordered_pts_src = np.array([
                pts_src[0],  # Top-left
                pts_src[1],  # Top-right
                pts_src[3],  # Bottom-right
                pts_src[2]   # Bottom-left
            ], dtype=np.int32)

            # Create a mask for the warped region to blend it into the original frame
            mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
            
            # Fill the mask with the quadrilateral defined by ordered_pts_src
            cv2.fillPoly(mask, [ordered_pts_src], 255)

            # Erode the mask to avoid boundary artifacts
            element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            mask = cv2.erode(mask, element, iterations=3)

            # Combine the warped image back into the original frame using the mask
            frame_masked = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
            warped_back_masked = cv2.bitwise_and(warped_back, warped_back, mask=mask)
            im_out = cv2.add(frame_masked, warped_back_masked)

        cv2.imshow('Frame', im_out)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def CropBoard(img, padding):
    croppedImg = img.crop((
        padding,
        padding, 
        img.width - padding,
        img.height - padding
    ))
    return croppedImg

def ToPIL(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def DrawArrow(img, startSquare, endSquare):
    grid_size = 8
    width, height, _ = img.shape
    square_width = width // grid_size
    square_height = height // grid_size

    startx, starty = startSquare
    endx, endy = endSquare

    xs = int((startx+0.5) * square_width)
    ys = int((starty+0.5) * square_height)

    xe = int((endx+0.5) * square_width)
    ye = int((endy+0.5) * square_height)

    arrowColour = (0, 255, 0)
    arrowWidth = 3
    imgWithArrow = cv2.arrowedLine(img, (ys,xs), (ye, xe), arrowColour, arrowWidth)
    return imgWithArrow

def GetSquares():
    board, img_data = FindBoard()

    grid_size = 8
    width, height, _ = board.shape
    square_width = width // grid_size
    square_height = height // grid_size

    squares = [[] for _ in range(8)]
    # Loop through each square position
    for row in range(grid_size):
        for col in range(grid_size):
            # Calculate the coordinates of the current square
            left = col * square_width
            top = row * square_height
            right = left + square_width
            bottom = top + square_height
            
            # Crop the square and add it to the list
            square = board[top:bottom, left:right]
            squares[row].append(square)
        
    # for row in squares:
    #     for square in row:
    #         cv2.imshow("Square", square)
    #         ClassifySquare(square)
    #         cv2.waitKey(0)
    return (squares, img_data)

def ClassifySquare(img):
    rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    average = np.average(rgbImg, axis = (0,1))
    print(average)
    

if __name__ == "__main__":
    seed = 139
    GetSquares()
    # for row in GetSquares():
    #     for square in row:
    #         if seed % 2 == 0:
    #             subfolder = "Red"
    #         else:
    #             subfolder = "Blue"
    #         #ToPIL(square).save(f"Training Data/{subfolder}/{seed}.png")
    #         seed += 1
    #     seed += 1
    #     if seed > 139+32:
    #         break
# # board = None
# # while board == None:
# #     board = FindBoard()
# board = FindBoard(projectBack=False)


# # while True:
# #     cv2.imshow("square", board)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break
# #board.show()

# grid_size = 8
# width, height, _ = board.shape
# square_width = width // grid_size
# square_height = height // grid_size

# squares = []
# # Loop through each square position
# for row in range(grid_size):
#     for col in range(grid_size):
#         # Calculate the coordinates of the current square
#         left = col * square_width
#         top = row * square_height
#         right = left + square_width
#         bottom = top + square_height
        
#         # Crop the square and add it to the list
#         square = board[top:bottom, left:right]
#         squares.append(square)
    
# iterable = iter(squares)
# while True:
#     cv2.imshow("sqaure", next(iterable))
#     cv2.waitKey(0)

