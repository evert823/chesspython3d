import sys
sys.path.append("..\\chess_variant_boardpainter\\classes")
from os import listdir
from os.path import isfile, join
from chess_position import ChessPosition
from chess_position_3d import ChessPosition3D
import json

def GetFiles(mypath):
    myfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return myfiles

def ConvertFile(pfilename):
    if pfilename.upper().find("TIMETHIEF") > -1:
        return
    if pfilename.upper().find("WITCH") > -1:
        return
    if pfilename.upper().find("JOKER") > -1:
        return
    if pfilename.upper().find("FEMMEFATALE") > -1:
        return
    if pfilename.upper().find("_ELF_") > -1:
        return
    if pfilename.upper().find("_ELF0") > -1:
        return
    if pfilename.upper().find("CASTLE") > -1:
        return
    if pfilename.upper().find("13A") == 0:
        return
    if pfilename.upper().find("2D") == 0:
        return

    extrafile = open(f"{infolder}\\{pfilename}", 'r')
    extradict = json.load(extrafile)
    colourtomove = extradict["colourtomove"]

    MyChessPosition.load_from_json(f"{infolder}\\{pfilename}")
    convert_object()
    write_3D_json(pfilename, colourtomove)

def convert_object():
    MyChessPosition3D.reset_boardsize(MyChessPosition.boardwidth, MyChessPosition.boardheight, 1)
    for j in range(MyChessPosition3D.boardheight):
        for i in range(MyChessPosition3D.boardwidth):
            MyChessPosition3D.squares[0][j][i] = MyChessPosition.squares[j][i]

def write_3D_json(pfilename, colourtomove):
    positionfile = open(f"{outfolder}\\{pfilename}", 'w')
    positiondict = {}
    positiondict["boardwidth"] = MyChessPosition3D.boardwidth
    positiondict["boardheight"] = MyChessPosition3D.boardheight
    positiondict["depth_3d"] = MyChessPosition3D.depth_3d
    positiondict["colourtomove"] = colourtomove

    positiondict["layers"] = []
    for z in range(MyChessPosition3D.depth_3d):
        squaresdict = {}
        squaresdict["squares"] = []
        for j in range(MyChessPosition3D.boardheight):
            rj = (MyChessPosition3D.boardheight - 1) - j
            myvisualrank = ""
            for i in range(MyChessPosition3D.boardwidth):
                mysymbol = MyChessPosition3D.squares[z][rj][i]
                while len(mysymbol) < 2:
                    mysymbol = " " + mysymbol
                myvisualrank += mysymbol
                if i < MyChessPosition3D.boardwidth - 1:
                    myvisualrank += "|"
            squaresdict["squares"].append(myvisualrank)
        positiondict["layers"].append(squaresdict)

    json.dump(positiondict, positionfile, indent=4)
    positionfile.close()


MyChessPosition = ChessPosition()
MyChessPosition3D = ChessPosition3D()

infolder = "C:\\Users\\Evert Jan\\Documents\\GitHub\\chesspython\\unittests"
outfolder = ".\\unittests"
a = GetFiles(infolder)

for myfile in a:
    ConvertFile(myfile)
