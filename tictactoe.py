""" RULES
    The user always makes the first move
    The user should be asked to input their move until the game ends.
    The format for input should be “x, y” where x is the horizontal axis and y is the vertical axis.
    You can assume that the user will always enter their input in the form “,” (i.e., no negative numbers, letters, symbols and multiple-digit numbers)
    After the user enters a move, the computer should make their move, if possible.
    Every time the computer makes its move, the state of the board should be printed out.
    If either the player or the computer wins, the state of the board should be printed out and the winner announced. The program should exit at that point.
    Additional: try to make the computer play optimally instead of randomly. Be sure to still read the suggested solution document, though!
"""

import random
import sys

# variable where I store list of all coordinates in the game
coordinates = []

# list of lists containing empty table
rows = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]


def main():
    while True:
        # get coordinates from the user
        user_coordinates = get_user_pos()
        # add user coordinates to record of choices
        coordinates.append(user_coordinates)
        # add user coordinates to the table
        add_coordinates()

        # get coordiantes from computer if space is available
        if len(coordinates) < 8:
            # get coordinates from the computer
            cp_coordinates = get_cp_pos()
            # add computer coordinates to record of choices
            coordinates.append(cp_coordinates)
            # add computer coordinates to the table
            add_coordinates()

        # print out the current table
        print_table()


# adding to table x (user) and o (computer)
def add_coordinates():
    for index, coordinate in enumerate(coordinates):
        if index == 0 or (index % 2 == 0):
            rows[coordinate["y"]][coordinate["x"]] = "x"
        else:
            rows[coordinate["y"]][coordinate["x"]] = "o"


# get coordinates from user
def get_user_pos():
    while True:
        choice = input(
            "Make your move by entering the coordinates in a range of 0-2 (format 'x,y'): "
        ).strip()

        # check if any coordinates given
        if not choice:
            print("No coordinates entered. Please, try again.")
            continue

        # check if too many coordinates
        try:
            x, y = choice.split(",")
        except ValueError:
            print("Too many coordinates. Please, try again.")
            continue

        # check if coordinates in range
        if 0 <= int(x) <= 2 and 0 <= int(y) <= 2:
            choice = {"x": int(x), "y": int(y)}
        else:
            print("Coordinates out of range. Please, try again.")
            continue

        # check if coordinates are already selected
        if choice in coordinates:
            print("Coordinates are already selected. Please, try again")
            continue

        return choice


# get computer coordinates (optimal selection)
def get_cp_pos():
    """
    Method:
    OFFENSE
    1. Scan rows to see if there are two 'o' and if cp can win
    2. Scan columns to see if there are two 'o' and cp can win
    3. Scan diagonals to see if there are two 'o' and cp can win
    DEFENSE
    4. Scan diagonals to see if there are two 'x' and user can be stopped
    5. Scan rows to see if there are two 'x' and user can be stopped
    6. Scan columns to see if there are two 'x' and user can be stopped
    """

    while True:
        """start with offense"""

        # check if 3 values 'o' row can be reached
        for row in rows:
            if row.count("o") == 2:
                if " " in row:
                    y = rows.index(row)
                    x = row.index(" ")
                    return {"x": x, "y": y}

        for i in range(3):
            col = []
            # check if 3 values 'o' column can be reached
            for row in rows:
                col.append(row[i])

            if col.count("o") == 2:
                if " " in col:
                    x = i
                    y = col.index(" ")
                    return {"x": x, "y": y}

        j = 0
        diag_right = []
        for row in rows:
            diag_right.append(row[j])
            j += 1

        # check if 3 values 'o' in diagonal can be reached
        if diag_right.count("o") == 2:
            if " " in diag_right:
                x = diag_right.index(" ")
                y = diag_right.index(" ")
                return {"x": x, "y": y}
        # check if 3 values 'x' in diagonal can be prevented
        elif diag_right.count("x") == 2:
            if " " in diag_right:
                x = diag_right.index(" ")
                y = diag_right.index(" ")
                return {"x": x, "y": y}

        k = 2
        diag_left = []
        for row in rows:
            diag_left.append(row[k])
            k -= 1

        # check if 3 values 'o' in diagonal can be reached
        if diag_left.count("o") == 2:
            if " " in diag_left:
                index = diag_left.index(" ")
                if index == 0:
                    x = 2
                elif index == 1:
                    x = 1
                else:
                    x = 0
                y = diag_left.index(" ")
                return {"x": x, "y": y}
        # check if 3 values 'x' in diagonal can be prevented
        elif diag_left.count("x") == 2:
            if " " in diag_left:
                index = diag_left.index(" ")
                if index == 0:
                    x = 2
                elif index == 1:
                    x = 1
                else:
                    x = 0
                y = diag_left.index(" ")
                return {"x": x, "y": y}

        """ go to defense """

        # check if 3 values 'x' row can be prevented
        for row in rows:
            if row.count("x") == 2:
                if " " in row:
                    y = rows.index(row)
                    x = row.index(" ")
                    return {"x": x, "y": y}

        for i in range(3):
            col = []
            # check if 3 values 'x' column can be prevented
            for row in rows:
                col.append(row[i])

            if col.count("x") == 2:
                if " " in col:
                    x = i
                    y = col.index(" ")
                    return {"x": x, "y": y}

        # random selector
        while True:
            # center box is preferred choice to begin, if empty
            if rows[1][1] == " ":
                return {"x": 1, "y": 1}

            x = random.randint(0, 2)
            y = random.randint(0, 2)

            # check if coordinates already exist
            cp_choice = {"x": x, "y": y}
            if cp_choice in coordinates:
                continue
            else:
                return cp_choice


#  print out the table
def print_table():
    print("------------")
    for line in rows:
        for pos in line:
            print("|", end=" ")
            print(pos, end=" ")
        print("|")
        print("------------")

    if check_winner() == 1:
        sys.exit("User wins!")
    elif check_winner() == 2:
        sys.exit("Computer wins!")
    elif len(coordinates) == 9:
        sys.exit("It's a draw!")


# check if there is a winner
def check_winner():
    user_win = ["x", "x", "x"]
    cp_win = ["o", "o", "o"]

    # check rows
    for row in rows:
        if row == user_win:
            return 1
        elif row == cp_win:
            return 2

    # check columns
    columns = [[], [], []]
    for i in range(3):
        for row in rows:
            columns[i].append(row[i])

    for column in columns:
        if column == user_win:
            return 1
        elif column == cp_win:
            return 2

    # check diagonals
    diagonals = [[], []]
    for i in range(3):
        diagonals[0].append(rows[i][i])

    j = 2
    for i in range(3):
        diagonals[1].append(rows[i][j])
        j -= 1

    if diagonals[0] == user_win or diagonals[1] == user_win:
        return 1
    elif diagonals[0] == cp_win or diagonals[1] == cp_win:
        return 2


if __name__ == "__main__":
    main()
