import solver
import opencvrun2
import ArucoDetector


def main():
    images = ArucoDetector.GetSquares()
    board = [[opencvrun2.classify(image) for image in row] for row in images]
    start, end = solver.CheckersSolver(board).calculate_move()


if __name__ == "__main__":
    main()
