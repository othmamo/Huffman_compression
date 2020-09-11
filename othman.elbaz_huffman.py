__license__ = 'Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2019-04-01'

"""
Huffman homework
2019
@author: othman.elbaz
"""

from algopy import bintree
from algopy import heap


###############################################################################
# Do not change anything above this line, except your login!
# Do not add any import

###############################################################################
## COMPRESSION

def __search_el(L,i):
    for c in range (len(L)):
        if (L[c][1]==i):
            return (True, c)
    return (False,0)


def buildfrequencylist(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    L = []
    for i in dataIN:
        b = __search_el(L,i)
        if(b[0]):
            L[b[1]] = (L[b[1]][0]+1,i)
        else:
            L.append((1,i))
    return L

def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    H = heap.Heap()
    l = len(inputList)
    for i in inputList:
        H.push((i[0],bintree.BinTree(i[1],None,None)))
    while(l>1):
        B = H.pop()
        B1 = H.pop()
        H.push((B[0]+B1[0],bintree.BinTree(None,B[1],B1[1])))
        l=l-1
    return(H.pop()[1])


def __encodeLetter(B,L,msg=""):
    if(B.key != None):
        L.append((B.key,msg))
    if(B.left != None):
        __encodeLetter(B.left,L, msg+"0")
    if(B.right != None):
        __encodeLetter(B.right,L,msg+"1")

def __poidsLetter(L,e):
    for i in L:
        if (i[0]==e):
            return i[1]
    return ""



def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    res = ""
    L=[]
    __encodeLetter(huffmanTree,L)
    for i in dataIN :
        res += str(__poidsLetter(L,i))
    return res

def __toBinary(n):
    L =  [0,0,0,0,0,0,0,0]
    i=7
    res = ""
    while(n>0 and i>=0):
        L[i] = n%2
        n = n//2
        i-=1
    for i in L:
        res += str(i)
    return res


def __encodeAux(B ,L ):
    if(B.left != None or B.right !=None):
        L.append("0")
    else:
        L.append("1")
    if(B.key != None):
        L.append(__toBinary(ord(B.key)))
    if(B.left != None):
        __encodeAux(B.left, L)
    if(B.right != None):
        __encodeAux(B.right,L)


def encodetree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    L = []
    r = ""
    __encodeAux(huffmanTree,L)
    for i in L:
        r+=i
    return(r)


def __todecimal(n):
    e = 0
    exp = len(n)-1
    for i in n:
        if(i == "1"):
            e += 2**exp
        exp -= 1
    return e

def tobinary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    msg = ""
    res = ""
    for i in range(len(dataIN)):
        msg += dataIN[i]
        if(len(msg) == 8):
            res += chr(__todecimal(msg))
            msg = ""
    if(msg != ""):
        res += chr(__todecimal(msg))
    return (res,8-len(msg))


def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    freq = buildfrequencylist(dataIn)
    Tree = buildHuffmantree(freq)
    EncData = encodedata(Tree,dataIn)
    EncTree = encodetree(Tree)
    return((tobinary(EncData),tobinary(EncTree)))


################################################################################
## DECOMPRESSION

def __poidsToLetter(L,i):
    for e in L:
        if (e[1]==i):
            return e[0]
    return ""

def decodedata(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    res = ""
    msg = ""
    L=[]
    __encodeLetter(huffmanTree,L)
    for i in dataIN:
        if (__poidsToLetter(L,msg) == ""):
            msg += i
        else:
            res+= __poidsToLetter(L,msg)
            msg = i
    if(msg!=""):
        res+= __poidsToLetter(L,msg)
    return res


def __parcours(L,i = 0):
    res = ""
    if (L[i]=='1'):
        for j in range(8):
            res += L[i+j+1]
        temp = chr(__todecimal(res))
        return (bintree.BinTree(temp,None,None) , i+9)
    else:
        (a,x) = __parcours(L,i+1)
        (c,x2) = __parcours(L,x)
        return (bintree.BinTree(None,a,c), x2)

def decodetree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf
    """
    res = __parcours(dataIN,0)
    return res[0]

def frombinary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    if (len(dataIN) != 0):
        res = ""
        for i in range(len(dataIN)-1):
            res += __toBinary(ord(dataIN[i]))
        last = __toBinary(ord(dataIN[len(dataIN)-1]))
        for j in range (align,8):
            res += last[j]
    return res

def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    a = frombinary(data,dataAlign)
    b = frombinary(tree,treeAlign)
    return (decodedata(decodetree(b),a))
