import copy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPixmap, QPainter
from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel)

from player import Player

choosen_figure = ''

pawn_promotion = False


class Board(QWidget):

    def __init__(self):
        super().__init__()

        self.piece_labels = []
        self.WHITE = Player('WHITE')
        self.BLACK = Player('BLACK')
        self.Players = [self.WHITE, self.BLACK]
        self.label = QLabel
        self.initUI()
        self.whoPlayNow = "W"
        self.available_moves = []

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(2800, 2800, 800, 800)

        self.setWindowTitle('chess')

        self.load_images()

        self.show()

    def load_images(self):
        i = 0
        for player in self.Players:
            for piece in player.pieces:
                self.piece_labels.append(i)
                self.piece_labels[i] = QLabel(player.which + piece.figure, self)
                self.piece_labels[i].setPixmap(QPixmap("./models/" + player.which[0] + piece.figure + ".png"))
                self.piece_labels[i].move(piece.coordinates[0], piece.coordinates[1])
                i = i + 1

    def change_player(self):
        if self.whoPlayNow == "W":
            self.whoPlayNow = "B"
        else:
            self.whoPlayNow = "W"

    def updatelabels(self):
        player_index = 0
        for player in self.Players:
            piece_index = 0
            for piece in player.pieces:
                if piece.active:
                    self.piece_labels[player_index * 16 + piece_index].move(
                        self.Players[player_index].pieces[piece_index].coordinates[0],
                        self.Players[player_index].pieces[piece_index].coordinates[1])
                    self.show()
                    self.Players[player_index].pieces[piece_index].active = False
                    break
                piece_index = piece_index + 1
            player_index = player_index + 1

    @staticmethod
    def mouse_in(x, y, coordinates):
        if (coordinates[0] < x < coordinates[0] + 100) and (coordinates[1] < y < coordinates[1] + 100):
            return True
        return False

    def erase_pawn_image(self, player_index, piece_index):
        self.piece_labels[player_index * 16 + piece_index].deleteLater()

    def find_active_piece(self):
        player_index = 0
        for player in self.Players:
            piece_index = 0
            if player.piece_chosen:
                for piece in player.pieces:
                    if piece.active:
                        return player_index, piece_index
                    piece_index = piece_index + 1
            player_index = player_index + 1
        return -100, -100

    def if_player_cant_move(self, playerindex):
        for piece in self.Players[playerindex].pieces:
            same_colour_pieces = self.Players[playerindex].pieces
            different_colour_pieces = self.Players[abs(playerindex - 1)].pieces
            available_moves_and_check = piece.return_available_moves(same_colour_pieces, different_colour_pieces)
            if available_moves_and_check[0] != []:
                return False, available_moves_and_check[1]
        return True, available_moves_and_check[1]

    def release_figure(self, player_index, piece_index, x, y):
        if self.Players[player_index].pieces[piece_index].coordinates == (x - x % 100, y - y % 100):
            print("CHANGE")
            self.Players[player_index].pieces[piece_index].active = False
            self.Players[player_index].piece_chosen = False
            self.available_moves = []
            self.update()
            return True
        return False

    def should_i_kill(self, player_index, piece_index):
        index_of_piece = 0
        for PIECE in self.Players[abs(player_index - 1)].pieces:
            if PIECE.position == self.Players[player_index].pieces[piece_index].position:
                self.erase_pawn_image(abs(player_index - 1), index_of_piece)
                self.Players[abs(player_index - 1)].pieces[index_of_piece].kill_pawn()
                break
            index_of_piece = index_of_piece + 1

    def change_piece_pos(self, x, y):
        player_index, piece_index = self.find_active_piece()

        change_piece = self.release_figure(player_index, piece_index, x, y)

        available_positions = []
        for piece in self.Players[player_index].pieces:
            available_positions.append(piece.coordinates)
            piece.capturing_in_passing = False

        if (x - (x % 100), y - (y % 100)) in available_positions and not change_piece:
            print("yolo")
            self.Players[player_index].pieces[piece_index].active = False
            self.Players[player_index].piece_chosen = False
            self.chosefigure(x, y)

        if not change_piece and self.Players[player_index].pieces[piece_index].is_in_available_moves(x - (x % 100),
                                                                                                     y - (y % 100),
                                                                                                     self.Players[
                                                                                                         player_index].pieces,
                                                                                                     self.Players[abs(
                                                                                                         player_index - 1)].pieces):

            position_before_move = self.Players[player_index].pieces[piece_index].position
            position_after_move = chr((x - (x % 100)) // 100 + 65) + str(8 - (y - (y % 100)) // 100)

            if piece_index < 8 and int(
                    self.Players[player_index].pieces[piece_index].position[1]) == 2 + 5 * player_index:
                self.Players[player_index].pieces[piece_index].capturing_in_passing = True
                print("tak0")

            self.Players[player_index].pieces[piece_index].change_coordinates(x - (x % 100), y - (y % 100))

            if int(self.Players[player_index].pieces[piece_index].position[1]) != 4 + player_index:
                self.Players[player_index].pieces[piece_index].capturing_in_passing = False
                print("nie0")

            if piece_index < 8 and position_after_move[0] != position_before_move[0]:
                capturing_in_passing = True
                for index in range(0, 8):
                    if self.Players[abs(player_index - 1)].pieces[index].position == position_after_move:
                        capturing_in_passing = False
                if capturing_in_passing:
                    for index in range(0, 8):
                        if self.Players[abs(player_index - 1)].pieces[index].position is not None and \
                                self.Players[abs(player_index - 1)].pieces[index].position[0] == position_after_move[
                            0] and int(self.Players[abs(player_index - 1)].pieces[index].position[1]) == int(
                            position_after_move[1]) - 1 + player_index * 2:
                            self.erase_pawn_image(abs(player_index - 1), index)
                            self.Players[abs(player_index - 1)].pieces[index].kill_pawn()

            if piece_index == 15 and position_before_move == 'E' + str(
                    player_index * 7 + 1) and position_after_move == 'G' + str(player_index * 7 + 1):
                self.Players[player_index].pieces[9].change_coordinates(500, 700 * abs(player_index - 1))
                self.piece_labels[player_index * 16 + 9].move(
                    self.Players[player_index].pieces[9].coordinates[0],
                    self.Players[player_index].pieces[9].coordinates[1])

            if piece_index == 15 and position_before_move == 'E' + str(
                    player_index * 7 + 1) and position_after_move == 'C' + str(player_index * 7 + 1):
                self.Players[player_index].pieces[8].change_coordinates(300, 700 * abs(player_index - 1))
                self.piece_labels[player_index * 16 + 8].move(
                    self.Players[player_index].pieces[8].coordinates[0],
                    self.Players[player_index].pieces[8].coordinates[1])

            if piece_index < 8 and position_after_move[1] == str(abs(player_index-1)*7+1) and self.Players[player_index].pieces[piece_index].figure == "PAWN":
                global pawn_promotion
                pawn_promotion = True
                self.x = pawn_promotion_class(self.Players[player_index].which, player_index, piece_index, parent=self)
                self.x.show()
                print('halohalohlao')

            self.should_i_kill(player_index, piece_index)

            self.Players[player_index].update_pos()

            self.Players[player_index].piece_chosen = False

            self.updatelabels()

            availablemoves, check = self.if_player_cant_move(abs(player_index - 1))

            if availablemoves:
                if check:
                    print("Check Mate!! player " + self.Players[player_index].which + " won !")
                else:
                    print("PAT!")

            self.change_player()

    def pawn_promotion_func(self, playerindex, pieceindex):
        print("HI")
        global choosen_figure
        self.Players[playerindex].pieces[pieceindex].figure = choosen_figure
        filepath = "./models/" + self.Players[playerindex].which[0] + choosen_figure + ".png"
        self.piece_labels[playerindex * 16 + pieceindex].setPixmap(QPixmap(filepath))
        availablemoves, check = self.if_player_cant_move(abs(playerindex - 1))

        if availablemoves:
            if check:
                print("Check Mate!! player " + self.Players[playerindex].which + " won !")
            else:
                print("PAT!")

        choosen_figure = ''

    def mouseReleaseEvent(self, QmouseEvent):
        global pawn_promotion
        print(pawn_promotion)
        if not pawn_promotion:
            x, y = QmouseEvent.x(), QmouseEvent.y()
            print(x, y)
            self.available_moves = []
            self.update()
            if self.Players[0].piece_chosen or self.Players[1].piece_chosen:
                self.available_moves = []
                self.update()
                self.change_piece_pos(x, y)
            else:
                self.chosefigure(x, y)

    def drawRect(self, qp, r, g, b, x, y, width, height):
        qp.setBrush(QColor(r, g, b))
        qp.drawRect(x, y, width, height)

    def drawavailable_moves(self, qp):
        for move in self.available_moves:
            qp.setPen(QPen(Qt.green, 8, Qt.SolidLine))

            qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            x = (ord(move[0]) - 65) * 100 + 45

            y = (ord(move[1]) - 49) * 100 + 45

            print(x)
            print(y)

            qp.drawEllipse(x, 800 - y, 10, 10)

    def chosefigure(self, x, y):
        for player_index in range(0, len(self.Players)):
            for piece_index in range(0, len(self.Players[player_index].pieces)):
                if not (not self.Players[player_index].pieces[piece_index].alive or not self.mouse_in(x, y,
                                                                                                      self.Players[
                                                                                                          player_index].pieces[
                                                                                                          piece_index].coordinates)) and not \
                        self.Players[player_index].piece_chosen and \
                        self.Players[player_index].which[0] == self.whoPlayNow:
                    print(self.Players[player_index].which + self.Players[player_index].pieces[piece_index].figure)
                    self.Players[player_index].pieces[piece_index].active = True
                    self.Players[player_index].piece_chosen = True
                    activePlayer = copy.deepcopy(self.Players[player_index])
                    activePlayerpieces = []
                    secondPlayerpieces = []
                    for piece in self.Players[player_index].pieces:
                        activePlayerpieces.append(piece)
                        activePlayer.pieces[piece_index].same_color_pieces_global.append(piece)
                    for piece in self.Players[abs(player_index - 1)].pieces:
                        secondPlayerpieces.append(piece)
                        activePlayer.pieces[piece_index].different_pieces_global.append(piece)
                    self.available_moves = activePlayer.pieces[piece_index].return_available_moves(activePlayerpieces,
                                                                                                   secondPlayerpieces)[
                        0]
                    print(self.available_moves)
                    self.update()
                    break

    def calculate_x_y(self, position):
        x = (ord(position[0]) - 65) * 100
        y = int(position[1]) * 100
        return [x, 800 - y]

    def loadpic(self, file, coordinates):
        pic = QLabel(self)
        pic.setPixmap(QPixmap(file))
        pic.move(coordinates[0], coordinates[1])
        pic.resize(100, 100)
        pic.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        for i in range(0, 8):
            for j in range(0, 8):
                if (i + j) % 2 == 0:
                    self.drawRect(qp, 232, 235, 239, j * 100, i * 100, 100, 100)
                else:
                    self.drawRect(qp, 125, 135, 150, j * 100, i * 100, 100, 100)
        self.drawavailable_moves(qp)
        qp.end()

    def closeEvent(self, event):
        exit()


class pawn_promotion_class(QWidget):
    def __init__(self, color, player_index, piece_index, parent):
        super().__init__()
        self.parent = parent
        self.color = color
        self.player_index = player_index
        self.piece_index = piece_index
        self.piece_labels = []
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(3000, 400, 400, 100)

        self.setWindowTitle('chose figure')

        self.load_images()

    def load_images(self):
        self.piece_labels.append(QLabel(self.color[0] + 'QUEEN', self))
        self.piece_labels[0].setPixmap(QPixmap("./models/" + self.color[0] + 'QUEEN.png'))

        self.piece_labels.append(QLabel(self.color[0] + 'ROOK', self))
        self.piece_labels[1].setPixmap(QPixmap("./models/" + self.color[0] + 'ROOK.png'))

        self.piece_labels.append(QLabel(self.color[0] + 'BISHOP', self))
        self.piece_labels[2].setPixmap(QPixmap("./models/" + self.color[0] + 'BISHOP.png'))

        self.piece_labels.append(QLabel(self.color[0] + 'KNIGHT', self))
        self.piece_labels[3].setPixmap(QPixmap("./models/" + self.color[0] + 'KNIGHT.png'))

        self.piece_labels[0].move(0, 0)
        self.piece_labels[1].move(100, 0)
        self.piece_labels[2].move(200, 0)
        self.piece_labels[3].move(300, 0)

    def mouseReleaseEvent(self, QmouseEvent):
        x, y = QmouseEvent.x(), QmouseEvent.y()
        print(x, y)
        x = x - x % 100
        y = y - y % 100
        global choosen_figure
        if x == 0 and y == 0:
            choosen_figure = 'QUEEN'
        elif x == 100 and y == 0:
            choosen_figure = 'ROOK'
        elif x == 200 and y == 0:
            choosen_figure = 'BISHOP'
        elif x == 300 and y == 0:
            choosen_figure = 'KNIGHT'
        print(choosen_figure)
        global pawn_promotion
        pawn_promotion = False
        self.parent.pawn_promotion_func(self.player_index, self.piece_index)
        self.hide()
