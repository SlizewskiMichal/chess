import copy


class Piece:
    def __init__(self, pozycja, colour, figure):
        self.alive = True
        self.active = False
        self.moved = False
        self.colour = colour
        self.position = pozycja
        self.figure = figure
        self.coordinates = ((ord(self.position[0]) - 65) * 100, 800 - (int(self.position[1])) * 100)
        self.same_color_pieces_global = []
        self.different_pieces_global = []
        self.check_mode = False
        self.capturing_in_passing = False

    def change_coordinates(self, x, y):
        self.coordinates = (x, y)
        position = chr(x // 100 + 65) + str(8 - y // 100)
        self.position = position
        self.moved = True

    def is_in_available_moves(self, x, y, same_color_pieces, different_color_pieces):
        position = chr(x // 100 + 65) + str(8 - y // 100)

        self.same_color_pieces_global = same_color_pieces
        self.different_pieces_global = different_color_pieces

        same_pieces_positions = []
        different_pieces_positions = []

        for piece in same_color_pieces:
            same_pieces_positions.append(piece.position)

        for piece in different_color_pieces:
            different_pieces_positions.append(piece.position)

        self.available_moves = self.available_moves_func(same_pieces_positions, different_pieces_positions)

        print(self.available_moves)

        if position in self.available_moves:
            print('T')
            return True
        print('N')
        return False

    def return_available_moves(self, same_color_pieces, different_color_pieces):
        self.same_color_pieces_global = same_color_pieces
        self.different_pieces_global = different_color_pieces
        print(self.same_color_pieces_global)

        same_pieces_positions = []
        different_pieces_positions = []

        for piece in same_color_pieces:
            same_pieces_positions.append(piece.position)

        for piece in different_color_pieces:
            different_pieces_positions.append(piece.position)

        self.available_moves = self.available_moves_func(same_pieces_positions, different_pieces_positions)

        check = self.check(same_pieces_positions,different_pieces_positions,self.position)

        return (self.available_moves,check)

    def kill_pawn(self):
        self.position = None
        self.coordinates = None
        self.active = False
        self.alive = False

    def check(self, same_color_pieces_positions, different_color_pieces_positions, position):
        if self.check_mode:
            return False
        different_pieces_local = copy.deepcopy(self.different_pieces_global)
        index = 0
        for i in range(0, len(same_color_pieces_positions)):
            if same_color_pieces_positions[i] == self.position:
                same_color_pieces_positions[i] = position
                index = i
                break

        all_different_pieces_available_moves = []

        if same_color_pieces_positions[15] in different_color_pieces_positions:
            for index2 in range(0, len(different_pieces_local)):
                if same_color_pieces_positions[15] == different_pieces_local[index2].position:
                    print(different_pieces_local[index2].position)
                    print(position)
                    different_pieces_local[index2].position = None
                    different_pieces_local[index2].alive = None
                    different_pieces_local[index2].active = None
                    different_pieces_local[index2].coordinates = None
                    print(self.different_pieces_global[index2].position)
                    print("ssdde")

                    break

        different_color_pieces_positions_local = []

        for piece in different_pieces_local:
            different_color_pieces_positions_local.append(piece.position)

        for piece in different_pieces_local:
            piece.check_mode = True
            if piece.position in same_color_pieces_positions:
                piece.kill_pawn()
            available_moves = piece.available_moves_func(different_color_pieces_positions_local,
                                                         same_color_pieces_positions)
            for move in available_moves:
                all_different_pieces_available_moves.append(move)
            piece.check_mode = False
        if same_color_pieces_positions[15] in all_different_pieces_available_moves:
            same_color_pieces_positions[index] = self.position
            return True
        same_color_pieces_positions[index] = self.position
        return False

    def available_moves_func(self, same_color_pieces, different_color_pieces):
        if not self.alive:
            return []

        if self.figure == "KNIGHT":
            available_moves = self.available_moves_KNIGTHT(same_color_pieces, different_color_pieces)
        elif self.figure == "PAWN":
            available_moves = self.available_moves_PAWN(same_color_pieces, different_color_pieces)
        elif self.figure == "BISHOP":
            available_moves = self.available_moves_BISHOP(same_color_pieces, different_color_pieces)
        elif self.figure == "ROOK":
            available_moves = self.available_moves_ROOK(same_color_pieces, different_color_pieces)
        elif self.figure == "QUEEN":
            available_moves = self.available_moves_QUEEN(same_color_pieces, different_color_pieces)
        elif self.figure == "KING":
            available_moves = self.available_moves_KING(same_color_pieces, different_color_pieces)

        return available_moves

    def check_correctness(self, same_color_pieces, different_color_pieces, position, available_moves):
        if len(position) == 2 and (72 >= ord(position[0]) >= 65) and (56 >= ord(position[1]) >= 49) and (
                position not in same_color_pieces) and not self.check(same_color_pieces,
                                                                      different_color_pieces,
                                                                      position) and position not in available_moves:
            available_moves.append(position)

    def short_castling(self,same_color_pieces,different_color_pieces,all_pieces_position):
        if self.same_color_pieces_global[9].alive and not self.same_color_pieces_global[9].moved:
            if  ('F' + self.same_color_pieces_global[15].position[1] in all_pieces_position or
                'G' + self.same_color_pieces_global[15].position[1] in all_pieces_position):
                return False
            if not (self.check(same_color_pieces,different_color_pieces,'F' + self.same_color_pieces_global[15].position[1]) or
                self.check(same_color_pieces,different_color_pieces,'G' + self.same_color_pieces_global[15].position[1])):
                return True

    def long_castling(self,same_color_pieces,different_color_pieces,all_pieces_position):
        if self.same_color_pieces_global[8].alive and not self.same_color_pieces_global[8].moved:
            if  ('C' + self.same_color_pieces_global[15].position[1] in all_pieces_position or
                'D' + self.same_color_pieces_global[15].position[1] in all_pieces_position):
                return False
            if not (self.check(same_color_pieces,different_color_pieces,'C' + self.same_color_pieces_global[15].position[1]) or
                self.check(same_color_pieces,different_color_pieces,'D' + self.same_color_pieces_global[15].position[1])):
                return True



    def available_moves_KING(self, same_color_pieces, different_color_pieces):
        available_moves = []
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(1, 1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(1, 0), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(1, -1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(0, 1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(0, -1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-1, 1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-1, 0), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-1, -1), available_moves)
        if not self.check_mode and not self.same_color_pieces_global[15].moved and not self.check(same_color_pieces,different_color_pieces,self.position):
            all_pieces_position = []
            for x in same_color_pieces:
                all_pieces_position.append(x)
            for y in different_color_pieces:
                all_pieces_position.append((y))
            if self.short_castling(same_color_pieces,different_color_pieces,all_pieces_position):
                available_moves.append('G'+self.same_color_pieces_global[15].position[1])
            if self.long_castling(same_color_pieces, different_color_pieces, all_pieces_position):
                available_moves.append('C' + self.same_color_pieces_global[15].position[1])
        return available_moves

    def available_moves_QUEEN(self, same_color_pieces, different_color_pieces):
        available_moves = []
        for i in (self.available_moves_ROOK(same_color_pieces, different_color_pieces),
                  self.available_moves_BISHOP(same_color_pieces, different_color_pieces)):
            for pos in i:
                available_moves.append(pos)
        return available_moves

    def available_moves_ROOK(self, same_color_pieces, different_color_pieces):
        available_moves = []
        position = self.position
        iterators = [1, -1]
        for iterator in iterators:
            iterator_variable = 0
            while 1 <= int(position[1]) <= 8:
                if position in same_color_pieces and position != self.position:
                    break
                elif position in different_color_pieces:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                    break
                else:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                iterator_variable = iterator_variable + iterator
                position = self.create_pos(0, iterator_variable)
            position = self.position
        for iterator in iterators:
            iterator_variable = 0
            while 65 <= ord(position[0]) <= 72:
                if position in same_color_pieces and position != self.position:
                    break
                elif position in different_color_pieces:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                    break
                else:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                iterator_variable = iterator_variable + iterator
                position = self.create_pos(iterator_variable, 0)
            position = self.position
        return available_moves

    def available_moves_KNIGTHT(self, same_color_pieces, different_color_pieces):
        available_moves = []
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(2, 1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(2, -1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-2, 1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-2, -1), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(1, 2), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(1, -2), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-1, 2), available_moves)
        self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-1, -2), available_moves)
        return available_moves

    def available_moves_BISHOP(self, same_color_pieces, different_color_pieces):
        available_moves = []
        position = self.position
        iterators = [1, -1]
        for iterator in iterators:
            iterator_variable = 0
            while 65 <= ord(position[0]) <= 72 and 1 <= int(position[1]) <= 8:
                if position in same_color_pieces and position != self.position:
                    break
                elif position in different_color_pieces:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                    break
                else:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                iterator_variable += iterator
                position = self.create_pos(iterator_variable, iterator_variable)
            position = self.position
        for iterator in iterators:
            iterator_variable = 0
            while 65 <= ord(position[0]) <= 72 and 1 <= int(position[1]) <= 8:
                if position in same_color_pieces and position != self.position:
                    break
                elif position in different_color_pieces:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                    break
                else:
                    self.check_correctness(same_color_pieces, different_color_pieces, position, available_moves)
                iterator_variable += iterator
                position = self.create_pos(iterator_variable, -iterator_variable)
            position = self.position
        return available_moves

    def available_moves_PAWN(self, same_color_pieces, different_color_pieces):
        available_moves = []
        i = 1
        if self.colour == "BLACK":
            i = -1

        if self.position != None and int(self.position[1]) == int(4.5 + 0.5*i):
            for index in range(0,8):
                if self.different_pieces_global[index].position != None and int(self.different_pieces_global[index].position[1]) == int(4.5 + 0.5*i):
                    if self.different_pieces_global[index].capturing_in_passing:
                        letter = different_color_pieces[index][0]

                        buffor = [self.different_pieces_global[index].position , self.different_pieces_global[index].coordinates,self.different_pieces_global[index].active,self.different_pieces_global[index].alive]

                        different_color_pieces[index] = None

                        self.different_pieces_global[index].kill_pawn

                        self.check_correctness(same_color_pieces, different_color_pieces,letter + self.create_pos(0, i)[1] ,
                                               available_moves)

                        different_color_pieces[index] = buffor[0]

                        self.different_pieces_global[index].position = buffor[0]

                        self.different_pieces_global[index].coordinates = buffor[1]

                        self.different_pieces_global[index].active = buffor[2]

                        self.different_pieces_global[index].alive = buffor[3]


        if self.create_pos(0, i * 1) not in different_color_pieces:
            self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(0, i * 1),
                                   available_moves)
            if self.create_pos(0, i * 2) not in different_color_pieces and self.create_pos(0,
                                                                                           i * 1) not in same_color_pieces and not self.moved:
                self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(0, i * 2),
                                       available_moves)
        if self.create_pos(1, i * 1) in different_color_pieces:
            self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(1, i * 1),
                                   available_moves)
        if self.create_pos(-1, i * 1) in different_color_pieces:
            self.check_correctness(same_color_pieces, different_color_pieces, self.create_pos(-1, i * 1),
                                   available_moves)
        return available_moves

    def create_pos(self, how_many_letter, how_many_numbers):
        return chr(ord(self.position[0]) + how_many_letter) + str(int(self.position[1]) + how_many_numbers)
