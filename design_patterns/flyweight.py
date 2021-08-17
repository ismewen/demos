class ChessPieceUnit(object):

    def __init__(self, name, color):
        self.name = name
        assert color in ["Red", "Black"]
        self.color = color


class ChessPosition(object):

    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y


class ChessPiece(object):

    def __init__(self, unit: ChessPieceUnit, position: ChessPosition):
        self.chess_unit = unit
        self.position = position


class ChessPieceUnitFactory(object):
    chess_mapping = dict()

    name_enum = ["车", "马", "象", "士", "将", "兵", "炮"]

    for name in name_enum:
        for color in ["Red", "Black"]:
            cp = ChessPieceUnit(name=name, color=color)
            key = "%s-%s" % (name, color)
            chess_mapping[key] = cp

    @classmethod
    def get_chess_piece(cls, name, color):
        key = "%s-%s" % (name, color)
        return cls.chess_mapping[key]


class ChessBoard(object):
    chess_pieces = dict()

    def __init__(self):
        # 摆放棋子
        chess_unit = ChessPieceUnitFactory.get_chess_piece(name="车", color="Red")
        key = "%s-%s" % (chess_unit.name, chess_unit.color)
        position = ChessPosition(position_x=0, position_y=0)
        self.chess_pieces[key] = ChessPiece(unit=chess_unit, position=position)

        chess_unit = ChessPieceUnitFactory.get_chess_piece(name="马", color="Red")
        key = "%s-%s" % (chess_unit.name, chess_unit.color)
        position = ChessPosition(position_x=0, position_y=1)
        self.chess_pieces[key] = ChessPiece(unit=chess_unit, position=position)

    def move(self, from_position, target_position):
        # 移动棋子
        pass
