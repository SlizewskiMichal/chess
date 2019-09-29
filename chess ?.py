from PyQt5.QtWidgets import (QWidget, QToolTip, QApplication, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
import sys


class pion:
    def __init__(self, pozycja, colour, figure):
        self.alive = True
        self.position = pozycja
        self.active = False
        self.colour = colour
        self.moved = False
        self.figure = figure
        self.coordinates = ((ord(self.position[0]) - 65) * 100, 800 - (int(self.position[1])) * 100)

    def changecoordinates(self,x,y):
        self.coordinates=(x,y)
        position=chr(x//100+65)+str(8-y//100)
        self.position=position
        self.moved = True

    def killpawn(self):
        self.position=None
        self.coordinates=None
        self.active=False
        self.alive=False

    def availablemovesfunc(self , WPIECES, BPIECES):
        if self.figure == "KNIGHT":
            availablemoves=self.availablemovesKNIGTHT()
        elif self.figure == "PAWN":
            availablemoves=self.availablemovesPAWN(WPIECES,BPIECES)
        elif self.figure == "BISHOP":
            availablemoves=self.availablemovesBISHOP(WPIECES,BPIECES)
        elif self.figure == "ROOK":
            availablemoves=self.availablemovesROOK(WPIECES,BPIECES)
        elif self.figure == "QUEEN":
            availablemoves=self.availablemovesQUEEN(WPIECES,BPIECES)
        elif self.figure == "KING":
            availablemoves=self.availablemovesKING(WPIECES,BPIECES)
        return availablemoves


    def isinavailablemoves(self, x, y, WPIECES, BPIECES):
        position=chr(x//100+65)+str(8-y//100)
        if self.colour == "WHITE":
            self.availablemoves = self.availablemovesfunc(WPIECES, BPIECES)
        else:
            self.availablemoves = self.availablemovesfunc(BPIECES, WPIECES)
        if position in self.availablemoves:
            if (self.colour == "WHITE" and position not in WPIECES) or (self.colour == "BLACK" and position not in BPIECES):
                return True
        return False


    def availablemovesKNIGTHT(self):
        avalablepositions = []
        avalablepositions.append(chr(ord(self.position[0]) + 2) + str(int(self.position[1]) + 1))
        avalablepositions.append(chr(ord(self.position[0]) + 2) + str(int(self.position[1]) - 1))
        avalablepositions.append(chr(ord(self.position[0]) - 2) + str(int(self.position[1]) + 1))
        avalablepositions.append(chr(ord(self.position[0]) - 2) + str(int(self.position[1]) - 1))
        avalablepositions.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 2))
        avalablepositions.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 2))
        avalablepositions.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 2))
        avalablepositions.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 2))
        print(avalablepositions)
        return avalablepositions

    def availablemovesPAWN(self, SAMECOLOURPIECES, DIFFERENTCOLOURPIECES):
        availablemoves = []
        if self.colour == "WHITE":
            if self.position[0] + str(int(self.position[1]) + 1) not in DIFFERENTCOLOURPIECES:
                availablemoves.append(self.position[0] + str(int(self.position[1]) + 1))
                if self.position[0] + str(int(self.position[1]) + 2) not in DIFFERENTCOLOURPIECES and self.position[0] + str(int(self.position[1]) + 1) not in SAMECOLOURPIECES and not self.moved:
                    availablemoves.append(self.position[0] + str(int(self.position[1]) + 2))
            if chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1) in DIFFERENTCOLOURPIECES:
                availablemoves.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1))
            if chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1) in DIFFERENTCOLOURPIECES:
                availablemoves.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1))
        else:
            if self.position[0] + str(int(self.position[1]) - 1) not in DIFFERENTCOLOURPIECES:
                availablemoves.append(self.position[0] + str(int(self.position[1]) - 1))
                if self.position[0] + str(int(self.position[1]) - 2) not in DIFFERENTCOLOURPIECES and self.position[0] + str(int(self.position[1]) - 1) not in SAMECOLOURPIECES and not self.moved:
                    availablemoves.append(self.position[0] + str(int(self.position[1]) - 2))
            if chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1) in DIFFERENTCOLOURPIECES:
                availablemoves.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1))
            if chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1) in DIFFERENTCOLOURPIECES:
                availablemoves.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1))
        return availablemoves

    def availablemovesBISHOP(self, SAMECOLOURPIECES, DIFFERENTCOLOURPIECES):
        availablemoves = []
        position = self.position
        iterators = [1,-1]
        for iterator in iterators:
            while ord(position[0]) >= 65 and ord(position[0]) <= 72 and int(position[1]) >= 1 and int(position[1]) <= 8:
                if position in SAMECOLOURPIECES and position != self.position:
                    print(position)
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = chr(ord(position[0]) + iterator) + str(int(position[1]) + iterator)
            position = self.position
        for iterator in iterators:
            while ord(position[0]) >= 65 and ord(position[0]) <= 72 and int(position[1]) >= 1 and int(position[1]) <= 8:
                if position in SAMECOLOURPIECES and position != self.position:
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = chr(ord(position[0]) + iterator) + str(int(position[1]) - iterator)
            position = self.position
        print(availablemoves)
        return availablemoves


    def availablemovesROOK(self, SAMECOLOURPIECES, DIFFERENTCOLOURPIECES):
        availablemoves = []
        position = self.position
        iterators = [1, -1]
        for iterator in iterators:
            while int(position[1]) >= 1 and int(position[1]) <= 8:
                if position in SAMECOLOURPIECES and position != self.position:
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = position[0] + str(int(position[1]) + iterator)
            position = self.position
        for iterator in iterators:
            while ord(position[0]) >= 65 and ord(position[0]) <= 72 :
                if position in SAMECOLOURPIECES and position != self.position:
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = chr(ord(position[0]) + iterator) + position[1]
            position = self.position
        print(availablemoves)
        return availablemoves

    def availablemovesQUEEN(self, SAMECOLOURPIECES, DIFFERENTCOLOURPIECES):
        availablemoves = []
        position = self.position
        iterators = [1, -1]
        for iterator in iterators:
            while ord(position[0]) >= 65 and ord(position[0]) <= 72 and int(position[1]) >= 1 and int(position[1]) <= 8:
                if position in SAMECOLOURPIECES and position != self.position:
                    print(position)
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = chr(ord(position[0]) + iterator) + str(int(position[1]) + iterator)
            position = self.position
        for iterator in iterators:
            while ord(position[0]) >= 65 and ord(position[0]) <= 72 and int(position[1]) >= 1 and int(position[1]) <= 8:
                if position in SAMECOLOURPIECES and position != self.position:
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = chr(ord(position[0]) + iterator) + str(int(position[1]) - iterator)
            position = self.position
        for iterator in iterators:
            while int(position[1]) >= 1 and int(position[1]) <= 8:
                if position in SAMECOLOURPIECES and position != self.position:
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = position[0] + str(int(position[1]) + iterator)
            position = self.position
        for iterator in iterators:
            while ord(position[0]) >= 65 and ord(position[0]) <= 72:
                if position in SAMECOLOURPIECES and position != self.position:
                    break
                elif position in DIFFERENTCOLOURPIECES:
                    availablemoves.append(position)
                    break
                else:
                    availablemoves.append(position)
                position = chr(ord(position[0]) + iterator) + position[1]
            position = self.position
        print(availablemoves)
        return availablemoves

    def availablemovesKING(self, WPIECES, BPIECES):
        availablemoves=[]
        availablemoves.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1))
        availablemoves.append(chr(ord(self.position[0]) + 1) + self.position[1])
        availablemoves.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1))
        availablemoves.append(self.position[0] + str(int(self.position[1]) + 1))
        availablemoves.append(self.position[0] + str(int(self.position[1]) - 1))
        availablemoves.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1))
        availablemoves.append(chr(ord(self.position[0]) - 1) + self.position[1])
        availablemoves.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1))
        return availablemoves



class gracz:
    def __init__(self, ktory):
        self.PieceChoosed = False
        self.pawns = []
        self.ktory = ktory
        if ktory == "WHITE":
            for i in "ABCDEFGH":
                self.pawns.append(pion(i + "2", ktory, "PAWN"))
            self.ROOK1 = pion("A1", ktory, "ROOK")
            self.ROOK2 = pion("H1", ktory, "ROOK")
            self.KNIGHT1 = pion("B1", ktory, "KNIGHT")
            self.KNIGHT2 = pion("G1", ktory, "KNIGHT")
            self.BISHOP1 = pion("C1", ktory, "BISHOP")
            self.BISHOP2 = pion("F1", ktory, "BISHOP")
            self.QUEEN = pion("D1", ktory, "QUEEN")
            self.KING = pion("E1", ktory, "KING")
        elif ktory == "BLACK":
            for i in "ABCDEFGH":
                self.pawns.append(pion(i + "7", ktory, "PAWN"))
            self.ROOK1 = pion("A8", ktory, "ROOK")
            self.ROOK2 = pion("H8", ktory, "ROOK")
            self.KNIGHT1 = pion("B8", ktory, "KNIGHT")
            self.KNIGHT2 = pion("G8", ktory, "KNIGHT")
            self.BISHOP1 = pion("C8", ktory, "BISHOP")
            self.BISHOP2 = pion("F8", ktory, "BISHOP")
            self.QUEEN = pion("D8", ktory, "QUEEN")
            self.KING = pion("E8", ktory, "KING")
        self.pieces = []
        for pawn in self.pawns:
            self.pieces.append(pawn)
        self.pieces.append(self.ROOK1)
        self.pieces.append(self.ROOK2)
        self.pieces.append(self.KNIGHT1)
        self.pieces.append(self.KNIGHT2)
        self.pieces.append(self.BISHOP1)
        self.pieces.append(self.BISHOP2)
        self.pieces.append(self.QUEEN)
        self.pieces.append(self.KING)

    def update_pos(self):
        self.pawns[0] = self.pieces[0]
        self.pawns[1] = self.pieces[1]
        self.pawns[2] = self.pieces[2]
        self.pawns[3] = self.pieces[3]
        self.pawns[4] = self.pieces[4]
        self.pawns[5] = self.pieces[5]
        self.pawns[6] = self.pieces[6]
        self.pawns[7] = self.pieces[7]
        self.ROOK1 = self.pieces[8]
        self.ROOK2 = self.pieces[9]
        self.KNIGHT1 = self.pieces[10]
        self.KNIGHT2 = self.pieces[11]
        self.BISHOP1 = self.pieces[12]
        self.BISHOP2 = self.pieces[13]
        self.QUEEN = self.pieces[14]
        self.KING = self.pieces[15]


class board(QWidget):

    def __init__(self):
        super().__init__()

        self.WHITE = gracz('WHITE')

        self.BLACK = gracz('BLACK')

        self.Players = [self.WHITE, self.BLACK]

        self.label = QLabel

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(800, 800, 800, 800)

        self.setWindowTitle('chess')

        self.loadpics()

        self.show()

    def loadpics(self):
        self.piecelabels = []
        i = 0
        for player in self.Players:
            for piece in player.pieces:
                self.piecelabels.append(i)
                self.piecelabels[i] = QLabel(player.ktory + piece.figure, self)
                self.piecelabels[i].setPixmap(QPixmap(player.ktory[0] + piece.figure + ".png"))
                self.piecelabels[i].move(piece.coordinates[0], piece.coordinates[1])
                i = i + 1

    def updatelabels(self):
        playerindex = 0
        for player in self.Players:
            pieceindex = 0
            for piece in player.pieces:
                if piece.active:
                    self.piecelabels[playerindex * 16 + pieceindex].move(
                        self.Players[playerindex].pieces[pieceindex].coordinates[0],
                        self.Players[playerindex].pieces[pieceindex].coordinates[1])
                    self.show()
                    self.Players[playerindex].pieces[pieceindex].active = False
                    break
                pieceindex = pieceindex + 1
            playerindex = playerindex + 1

    def mouse_in(self, x, y, coordinates):
        if ((coordinates[0] < x and coordinates[0] + 100 > x) and (coordinates[1] < y and coordinates[1] + 100 > y)):
            return True
        return False

    def killpawn(self, playerindex, pieceindex):
        self.piecelabels[playerindex * 16 + pieceindex].deleteLater()


    def mouseReleaseEvent(self, QmouseEvent):
        x, y = QmouseEvent.x(), QmouseEvent.y()
        playerindex = 0
        if self.Players[0].PieceChoosed or self.Players[1].PieceChoosed:
            for player in self.Players:
                pieceindex = 0
                if player.PieceChoosed:
                    for piece in player.pieces:
                        if piece.active:
                            if piece.coordinates == (x-x%100,y-y%100):
                                print("CHANGE")
                                self.Players[playerindex].pieces[pieceindex].active=False
                                self.Players[playerindex].PieceChoosed = False
                                break
                            WPIECES = []
                            BPIECES = []
                            for WPIECE in self.Players[0].pieces:
                                WPIECES.append(WPIECE.position)
                            for BPIECE in self.Players[1].pieces:
                                BPIECES.append(BPIECE.position)
                            if piece.isinavailablemoves(x - (x % 100), y - (y % 100), WPIECES, BPIECES):
                                self.Players[playerindex].pieces[pieceindex].changecoordinates(x - (x % 100), y - (y % 100))
                                indexofpiece=0
                                for PIECE in self.Players[abs(playerindex-1)].pieces :
                                    if PIECE.position == self.Players[playerindex].pieces[pieceindex].position:
                                        self.killpawn(abs(playerindex-1),indexofpiece)
                                        self.Players[abs(playerindex-1)].pieces[indexofpiece].killpawn()
                                        break
                                    indexofpiece = indexofpiece + 1

                                self.Players[playerindex].update_pos()
                                self.Players[playerindex].PieceChoosed = False
                                self.updatelabels()
                        pieceindex = pieceindex + 1
                playerindex = playerindex + 1
        else:
            for player in self.Players:
                player.PieceChoosed = False
                for pawn in player.pawns:
                    if pawn.alive and self.mouse_in(x, y, pawn.coordinates):
                        print(player.ktory + "Pawn")
                        pawn.active = True
                        player.PieceChoosed = True
                if  player.ROOK1.alive and self.mouse_in(x, y, player.ROOK1.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "ROOK")
                    player.ROOK1.active = True
                    player.PieceChoosed = True
                elif player.ROOK2.alive and self.mouse_in(x, y, player.ROOK2.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "ROOK")
                    player.ROOK2.active = True
                    player.PieceChoosed = True
                elif player.KNIGHT1.alive and self.mouse_in(x, y, player.KNIGHT1.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "KNIGHT")
                    player.KNIGHT1.active = True
                    player.PieceChoosed = True
                elif player.KNIGHT2.alive and self.mouse_in(x, y, player.KNIGHT2.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "KNIGHT")
                    player.KNIGHT2.active = True
                    player.PieceChoosed = True
                elif player.BISHOP1.alive and self.mouse_in(x, y, player.BISHOP1.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "BISHOP")
                    player.BISHOP1.active = True
                    player.PieceChoosed = True
                elif player.BISHOP2.alive and self.mouse_in(x, y, player.BISHOP2.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "BISHOP")
                    player.BISHOP2.active = True
                    player.PieceChoosed = True
                elif player.KING.alive and self.mouse_in(x, y, player.KING.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "KING")
                    player.KING.active = True
                    player.PieceChoosed = True
                elif player.QUEEN.alive and self.mouse_in(x, y, player.QUEEN.coordinates) and not player.PieceChoosed:
                    print(player.ktory + "QUEEN")
                    player.QUEEN.active = True
                    player.PieceChoosed = True

    def drawRect(self, qp, r, g, b, x, y, width, height):
        qp.setBrush(QColor(r, g, b))
        qp.drawRect(x, y, width, height)

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
        qp.end()

    def closeEvent(self, event):
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    boardd = board()
    sys.exit(app.exec_())
