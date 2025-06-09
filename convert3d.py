import sys
sys.path.append("..\\chess_variant_boardpainter\\classes")
from os import listdir
from os.path import isfile, join
from chess_position_3d import ChessPosition3D
import json

def GetFiles(mypath):
    myfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return myfiles

def ConvertFile(pfilename):
    print(pfilename)
    extrafile = open(f"{infolder}\\{pfilename}", 'r')
    extradict = json.load(extrafile)
    colourtomove = extradict["colourtomove"]
    MyChessPosition3D.load_from_json(f"{infolder}\\{pfilename}")
    convert_object()
    write_3D_json(obj=MyChessPosition3D_new, pfilename=pfilename.replace(".json", "_swap_xz.json"), colourtomove=colourtomove)

def convert_object():
    swap_xz()
    #swap_yz()

def swap_xz():
    MyChessPosition3D_new.reset_boardsize(MyChessPosition3D.depth_3d, MyChessPosition3D.boardheight, MyChessPosition3D.boardwidth)
    for z in range(MyChessPosition3D_new.depth_3d):
        for j in range(MyChessPosition3D_new.boardheight):
            for i in range(MyChessPosition3D_new.boardwidth):
                MyChessPosition3D_new.squares[z][j][i] = MyChessPosition3D.squares[i][j][z]

def swap_yz():
    MyChessPosition3D_new.reset_boardsize(MyChessPosition3D.boardwidth, MyChessPosition3D.depth_3d, MyChessPosition3D.boardheight)
    for z in range(MyChessPosition3D_new.depth_3d):
        for j in range(MyChessPosition3D_new.boardheight):
            for i in range(MyChessPosition3D_new.boardwidth):
                MyChessPosition3D_new.squares[z][j][i] = MyChessPosition3D.squares[j][z][i]

def write_3D_json(obj, pfilename, colourtomove):
    positionfile = open(f"{outfolder}\\{pfilename}", 'w')
    positiondict = {}
    positiondict["boardwidth"] = obj.boardwidth
    positiondict["boardheight"] = obj.boardheight
    positiondict["depth_3d"] = obj.depth_3d
    positiondict["colourtomove"] = colourtomove

    positiondict["layers"] = []
    for z in range(obj.depth_3d):
        squaresdict = {}
        squaresdict["squares"] = []
        for j in range(obj.boardheight):
            rj = (obj.boardheight - 1) - j
            myvisualrank = ""
            for i in range(obj.boardwidth):
                mysymbol = obj.squares[z][rj][i]
                while len(mysymbol) < 2:
                    mysymbol = " " + mysymbol
                myvisualrank += mysymbol
                if i < obj.boardwidth - 1:
                    myvisualrank += "|"
            squaresdict["squares"].append(myvisualrank)
        positiondict["layers"].append(squaresdict)

    json.dump(positiondict, positionfile, indent=4)
    positionfile.close()


MyChessPosition3D = ChessPosition3D()
MyChessPosition3D_new = ChessPosition3D()

infolder = ".\\positions"
outfolder = ".\\temppositions"

a = GetFiles(infolder)
selection = ["mate_in_6_for_white_BN.json"]

for myfile in a:
    if myfile in selection:
        ConvertFile(myfile)
