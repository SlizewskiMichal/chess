from PyQt5.QtWidgets import (QWidget, QToolTip, QApplication, QLabel)
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
import sys


class pion:
    def __init__(self, pozycja, colour, figure):
        self.alive = True
        self.active = False
        self.moved = False
        self.colour = colour
        self.position = pozycja
        self.figure = figure
        self.coordinates = ((ord(self.position[0]) - 65) * 100, 800 - (int(self.position[1])) * 100)

    def changecoordinates(self, x, y):
        self.coordinates = (x, y)
        position = chr(x // 100 + 65) + str(8 - y // 100)
        self.position = position
        self.moved = True

    def isinavailablemoves(self, x, y, samecolourpieces, differentcolourpieces):
        position = chr(x // 100 + 65) + str(8 - y // 100)

        samepiecespositions = []
        differentpiecespositions = []

        for piece in samecolourpieces:
            samepiecespositions.append(piece.position)

        for piece in differentcolourpieces:
            differentpiecespositions.append(piece.position)

        self.availablemoves = self.availablemovesfunc(samepiecespositions, differentpiecespositions)

        if position in self.availablemoves and position not in samepiecespositions:
            return True

        return False

    def killpawn(self):
        self.position = None
        self.coordinates = None
        self.active = False
        self.alive = False

    def availablemovesfunc(self, samecolourpieces, differentcolourpieces):
        if self.figure == "KNIGHT":
            availablemoves = self.availablemovesKNIGTHT()
        elif self.figure == "PAWN":
            availablemoves = self.availablemovesPAWN(samecolourpieces, differentcolourpieces)
        elif self.figure == "BISHOP":
            availablemoves = self.availablemovesBISHOP(samecolourpieces, differentcolourpieces)
        elif self.figure == "ROOK":
            availablemoves = self.availablemovesROOK(samecolourpieces, differentcolourpieces)
        elif self.figure == "QUEEN":
            availablemoves = self.availablemovesQUEEN(samecolourpieces, differentcolourpieces)
        elif self.figure == "KING":
            availablemoves = self.availablemovesKING()
        return availablemoves


    def availablemovesKING(self):
        availablemoves = []
        availablemoves.append(self.createpos(1, 1))
        availablemoves.append(self.createpos(1, 0))
        availablemoves.append(self.createpos(1, -1))
        availablemoves.append(self.createpos(0, 1))
        availablemoves.append(self.createpos(0, -1))
        availablemoves.append(self.createpos(-1, 1))
        availablemoves.append(self.createpos(-1, 0))
        availablemoves.append(self.createpos(-1, -1))
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
                position = self.createpos(iterator, iterator)
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
                position = self.createpos(iterator, -iterator)
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
                position = self.createpos(0, iterator)
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
                position = self.createpos(iterator, 0)
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
                position = self.createpos(0, iterator)
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
                position = self.createpos(iterator, 0)
            position = self.position
        print(availablemoves)
        return availablemoves


    def availablemovesKNIGTHT(self):
        avalablepositions = []
        avalablepositions.append(self.createpos( 2,  1))
        avalablepositions.append(self.createpos( 2, -1))
        avalablepositions.append(self.createpos(-2,  1))
        avalablepositions.append(self.createpos(-2, -1))
        avalablepositions.append(self.createpos( 1,  2))
        avalablepositions.append(self.createpos( 1, -2))
        avalablepositions.append(self.createpos(-1,  2))
        avalablepositions.append(self.createpos(-1, -2))
        return avalablepositions

    def availablemovesBISHOP(self, SAMECOLOURPIECES, DIFFERENTCOLOURPIECES):
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
                position = self.createpos(iterator, iterator)
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
                position = self.createpos(iterator, -iterator)
            position = self.position
        print(availablemoves)
        return availablemoves
        print(avalablepositions)

    def availablemovesPAWN(self, SAMECOLOURPIECES, DIFFERENTCOLOURPIECES):
        availablemoves = []
        i=1
        if self.colour == "BLACK":
            i=-1
        if self.createpos(0, i*1) not in DIFFERENTCOLOURPIECES:
            availablemoves.append(self.createpos(0, i*1))
            if self.createpos(0, i*2) not in DIFFERENTCOLOURPIECES and self.createpos(0, i*1) not in SAMECOLOURPIECES and not self.moved:
                availablemoves.append(self.createpos(0, i*2))
        if self.createpos(1, i*1) in DIFFERENTCOLOURPIECES:
            availablemoves.append(self.createpos(1, i*1))
        if self.createpos(-1, i*1) in DIFFERENTCOLOURPIECES:
            availablemoves.append(self.createpos(-1, i*1))
        print(availablemoves)
        return availablemoves

    def createpos(self,howmanyletter,howmanynumbers):
        return chr(ord(self.position[0]) + howmanyletter) + str(int(self.position[1]) + howmanynumbers)


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

    def eresepawnimage(self, playerindex, pieceindex):
        self.piecelabels[playerindex * 16 + pieceindex].deleteLater()

    def findactivepiece(self):
        playerindex = 0
        for player in self.Players:
            pieceindex = 0
            if player.PieceChoosed:
                for piece in player.pieces:
                    if piece.active:
                        return playerindex, pieceindex
                    pieceindex = pieceindex + 1
            playerindex = playerindex + 1
        return -100, -100

    def releasefigure(self, playerindex, pieceindex, x, y):
        if self.Players[playerindex].pieces[pieceindex].coordinates == (x - x % 100, y - y % 100):
            print("CHANGE")
            self.Players[playerindex].pieces[pieceindex].active = False
            self.Players[playerindex].PieceChoosed = False

    def shouldikill(self, playerindex, pieceindex):
        indexofpiece = 0
        for PIECE in self.Players[abs(playerindex - 1)].pieces:
            if PIECE.position == self.Players[playerindex].pieces[pieceindex].position:
                self.eresepawnimage(abs(playerindex - 1), indexofpiece)
                self.Players[abs(playerindex - 1)].pieces[indexofpiece].killpawn()
                break
            indexofpiece = indexofpiece + 1

    def changepiecepos(self, x, y):
        playerindex, pieceindex = self.findactivepiece()

        self.releasefigure(playerindex, pieceindex, x, y)

        if self.Players[playerindex].pieces[pieceindex].isinavailablemoves(x - (x % 100), y - (y % 100),
                                                                           self.Players[playerindex].pieces,
                                                                           self.Players[abs(playerindex - 1)].pieces):
            self.Players[playerindex].pieces[pieceindex].changecoordinates(x - (x % 100), y - (y % 100))

            self.shouldikill(playerindex, pieceindex)

            self.Players[playerindex].update_pos()

            self.Players[playerindex].PieceChoosed = False

            self.updatelabels()

    def mouseReleaseEvent(self, QmouseEvent):
        x, y = QmouseEvent.x(), QmouseEvent.y()
        if self.Players[0].PieceChoosed or self.Players[1].PieceChoosed:
            self.changepiecepos(x, y)
        else:
            self.chosefigure(x, y)

    def drawRect(self, qp, r, g, b, x, y, width, height):
        qp.setBrush(QColor(r, g, b))
        qp.drawRect(x, y, width, height)

    def chosefigure(self, x, y):
        for playerindex in range(0, len(self.Players)):
            for pieceindex in range(0, len(self.Players[playerindex].pieces)):
                if not (not self.Players[playerindex].pieces[pieceindex].alive or not self.mouse_in(x, y, self.Players[
                    playerindex].pieces[pieceindex].coordinates)) and not self.Players[playerindex].PieceChoosed:
                    print(self.Players[playerindex].ktory + self.Players[playerindex].pieces[pieceindex].figure)
                    self.Players[playerindex].pieces[pieceindex].active = True
                    self.Players[playerindex].PieceChoosed = True
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
        qp.end()

    def closeEvent(self, event):
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    boardd = board()
    sys.exit(app.exec_())
