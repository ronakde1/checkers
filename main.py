import solver
import opencvrun2
import ArucoDetector


def main():
    while True:
        images, img_data = ArucoDetector.GetSquares()
        board = [[opencvrun2.classify(image) for image in row] for row in images]
        for row in board:
            print(row)
        start, end = solver.CheckersSolver(board).calculate_move()
        print(start, end)
        ArucoDetector.ProjectBack(img_data, start, end)


if __name__ == "__main__":
    main()
