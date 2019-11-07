from piece import Piece


class Player:
    def __init__(self, which):
        self.piece_chosen = False
        self.pawns = []
        self.which = which
        if which == "WHITE":
            for i in "ABCDEFGH":
                self.pawns.append(Piece(i + "2", which, "PAWN"))
            self.ROOK1 = Piece("A1", which, "ROOK")
            self.ROOK2 = Piece("H1", which, "ROOK")
            self.KNIGHT1 = Piece("B1", which, "KNIGHT")
            self.KNIGHT2 = Piece("G1", which, "KNIGHT")
            self.BISHOP1 = Piece("C1", which, "BISHOP")
            self.BISHOP2 = Piece("F1", which, "BISHOP")
            self.QUEEN = Piece("D1", which, "QUEEN")
            self.KING = Piece("E1", which, "KING")
        elif which == "BLACK":
            for i in "ABCDEFGH":
                self.pawns.append(Piece(i + "7", which, "PAWN"))
            self.ROOK1 = Piece("A8", which, "ROOK")
            self.ROOK2 = Piece("H8", which, "ROOK")
            self.KNIGHT1 = Piece("B8", which, "KNIGHT")
            self.KNIGHT2 = Piece("G8", which, "KNIGHT")
            self.BISHOP1 = Piece("C8", which, "BISHOP")
            self.BISHOP2 = Piece("F8", which, "BISHOP")
            self.QUEEN = Piece("D8", which, "QUEEN")
            self.KING = Piece("E8", which, "KING")
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
