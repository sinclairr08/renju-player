from utility import list_add, list_sub


class Renju:
    def __init__(self):
        self.white = -1
        self.blank = 0
        self.black = 1
        self.edge = 2

        self.is_end = False
        self.message = ""
        self.forbidden_list = []

        self.direc = [[1,0], [0,1], [1,1], [1,-1]]
        self.stones = [[self.blank for i in range(15)] for j in range(15)]

    # If place is out of bounds, returns edge. Else returns the color of that place
    def get_stone_color(self, place):
        x = place[0]
        y = place[1]

        if x > 14 or x < 0 or y > 14 or y < 0:
            return self.edge

        else:
            return self.stones[x][y]

    # Check that the place (x,y) is forbidden or not
    def is_forbidden(self, x, y):
        lengths = []
        for di in self.direc:
            row_cnt = 1
            row_blank_cnt = 1

            is_blank = False
            is_blocked = False

            # If this value is 2, then it is blocked
            half_block_stack = 0

            cur_place = list_add([x, y], di)

            prev_color = self.black
            cur_color = self.get_stone_color(cur_place)

            while True:
                if cur_color == self.edge:
                    is_blocked = True
                    break

                elif cur_color == self.white:
                    if prev_color == self.blank:
                        half_block_stack += 1
                    else:
                        is_blocked = True
                    break

                elif cur_color == self.black:
                    row_blank_cnt += 1
                    if not is_blank: row_cnt += 1

                elif cur_color == self.blank:
                    if not is_blank:
                        is_blank = True
                    else:
                        break

                cur_place = list_add(cur_place, di)

                prev_color = cur_color
                cur_color = self.get_stone_color(cur_place)

            is_blank = False
            cur_place = list_sub([x, y], di)

            prev_color = self.black
            cur_color = self.get_stone_color(cur_place)

            while True:
                if cur_color == self.edge:
                    is_blocked = True
                    break

                elif cur_color == self.white:
                    if prev_color == self.blank:
                        half_block_stack += 1
                    else:
                        is_blocked = True
                    break

                elif cur_color == self.black:
                    row_blank_cnt += 1
                    if not is_blank: row_cnt += 1

                elif cur_color == self.blank:
                    if not is_blank:
                        is_blank = True
                    else:
                        break

                cur_place = list_sub(cur_place, di)

                prev_color = cur_color
                cur_color = self.get_stone_color(cur_place)

            if half_block_stack == 2 and not is_blocked:
                is_blocked = True

            if row_blank_cnt == 3 and row_cnt != 1:
                if not is_blocked:
                    if 3 in lengths:
                        return True
                    else:
                        lengths.append(3)

            if row_blank_cnt == 4 and row_cnt != 1:
                if 4 in lengths:
                    return True
                else:
                    lengths.append(4)

            elif row_blank_cnt >= 6:
                if row_blank_cnt == row_cnt:
                    return True

                elif row_cnt == 1 and row_blank_cnt == 7:
                    return True

        return False

    # Find all forbidden place on the board
    def set_forbidden_list(self):
        for i in range(15):
            for j in range(15):
                if self.stones[i][j] == self.blank:
                    if self.is_forbidden(i, j):
                        self.forbidden_list.append([i, j])

    def check_row(self, x, y, color):
        self.stones[x][y] = color
        for di in self.direc:
            row_cnt = 1
            cur_place = list_add([x,y], di)

            prev_color = color
            cur_color = self.get_stone_color(cur_place)

            while cur_color == prev_color:
                row_cnt += 1
                cur_place = list_add(cur_place, di)

                prev_color = cur_color
                cur_color = self.get_stone_color(cur_place)

            cur_place = list_sub([x,y], di)

            prev_color = color
            cur_color = self.get_stone_color(cur_place)

            while cur_color == prev_color:
                row_cnt += 1
                cur_place = list_sub(cur_place, di)

                prev_color = cur_color
                cur_color = self.get_stone_color(cur_place)

            if row_cnt >= 5:
                self.is_end = True
                if color == self.white:
                    self.message = "White Win! 5 in a row!"

                else:
                    self.message = "Black Win! 5 in a row!"

    def check_forbidden(self, x, y):
        if [x,y] in self.forbidden_list:
            self.is_end = True
            self.message = "White Win! Black took a forbidden place!"

            self.forbidden_list.clear()
            return True

        self.forbidden_list.clear()
        return False

    def put_stone(self, x, y, stone_color):
        if stone_color == "white":
            self.check_row(x, y, self.white)
            self.set_forbidden_list()

        else:
            if not self.check_forbidden(x, y):
                self.check_row(x, y, self.black)

        return self.message, self.forbidden_list
