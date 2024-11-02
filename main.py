import solver
import opencvrun2


def main():
    images = [[]]
    board = [[opencvrun2.classify(image) for image in row] for row in images]
    move = solver.CheckersSolver(board).calculate_move()


if __name__ == "__main__":
    main()
