import copy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPixmap, QPainter
from PyQt5.QtWidgets import (QWidget, QToolTip, QLabel)

from player import Player


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
            self.Players[player_index].pieces[piece_index].change_coordinates(x - (x % 100), y - (y % 100))

            self.should_i_kill(player_index, piece_index)

            self.Players[player_index].update_pos()

            self.Players[player_index].piece_chosen = False

            self.updatelabels()

            self.change_player()

    def mouseReleaseEvent(self, QmouseEvent):
        x, y = QmouseEvent.x(), QmouseEvent.y()
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
                                                                                                 secondPlayerpieces)
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
