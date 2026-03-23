import copy
import random

def split_bytes(str x, int c_chunks=0, int c_size=8):
    cdef char* bytelist[4] # list of strings like ["11111111", "00000000", "11111111", "00000000"]
    l = [ x[i:i+c_size] for i in range(0, c_chunks or len(x), c_size) ]
    return l

def binFloodToDots(list x) -> str: # '192.168.1.1'
    return '.'.join([ str(int(i, 2)) for i in x ])

def getMaskFromCidr(int pCidr, int pBlankCidr) -> tuple(list[str], str):
    cdef str newMaskBin   = "1" * pCidr + "0" * pBlankCidr
    cdef list[str] maskBinSplit = split_bytes(newMaskBin)
    cdef str maskDecFinal = binFloodToDots(maskBinSplit)
    return maskBinSplit, maskDecFinal

def getNetAndBroadIp(list[str] pMaskBinSplit, list[int] pIpSplits):
    cdef list[str] ipBinFull = [ bin(curIpChunk).replace('0b', '').zfill(8) for curIpChunk in pIpSplits ]

    cdef list[int] calc_netIp   = []
    cdef list[int] calc_broadIp = []

    cdef int idx_abs
    cdef int curIpBit
    cdef int curMaskBit
    cdef int curNetIp

    cdef int i, j
    cdef int res1, res2

    cdef str a1, b1
    cdef str a2, b2

    for i, (a1, b1) in enumerate(zip(ipBinFull, pMaskBinSplit)):
        for j, (a2, b2) in enumerate(zip(a1, b1)):
            idx_abs    = i * len(ipBinFull[0]) + j

            curIpBit   = int(a2)
            curMaskBit = int(b2)

            curNetIp   = int(curIpBit and curMaskBit)
            res1 = curNetIp
            res2 = curNetIp or int(not curMaskBit)
            calc_netIp.append(res1)
            calc_broadIp.append(res2)

    cdef str joinNetIp    = ''.join(str(x) for x in calc_netIp)
    cdef str joinBroadIp  = ''.join(str(x) for x in calc_broadIp)

    #region RESULTS SPLIT
    cdef list[str] splitNetIp   = split_bytes(joinNetIp)
    cdef list[str] splitBroadIp = split_bytes(joinBroadIp)

    cdef list[str] splitMinIp   = copy.deepcopy(splitNetIp)
    cdef list[str] splitMaxIp   = copy.deepcopy(splitBroadIp)

    cdef int decSplitMinIp = int(splitMinIp[3], 2) + 1
    cdef int decSplitMaxIp = int(splitMaxIp[3], 2) - 1

    splitMinIp[3] = format(decSplitMinIp, '08b') # convert to 8bit binary with zero padding
    splitMaxIp[3] = format(decSplitMaxIp, '08b')
    #endregion

    cdef str newNetIp   = binFloodToDots(splitNetIp)
    cdef str newBroadIp = binFloodToDots(splitBroadIp)

    cdef str newMinIp   = binFloodToDots(splitMinIp)
    cdef str newMaxIp   = binFloodToDots(splitMaxIp)

    return newNetIp, newBroadIp, newMinIp, newMaxIp

def generateCidr(max_cidr=32) -> tuple(int, int):
    cdef int newCidr = random.randint(4, 31)
    cdef int blankCidr = max_cidr - newCidr

    return (newCidr, blankCidr)

def generateIpSplits() -> list[int]:
    cdef int ipFirstSeg = random.randint(10, 200)
    cdef list[int] newIpSegments = [ipFirstSeg]
    cdef int curIpSegment

    for i in range(3):
        curIpSegment = random.randint(0, 255)
        newIpSegments.append(curIpSegment)

    return newIpSegments

def add_selective(dict[str, list[str]] full_dict, dict[str, list[str]] part_dict, list[str] patterns) -> None:
    cdef list[str] key_names = list(full_dict.keys())
    cdef tuple cur_row
    cdef list[str] random_pattern
    #cdef str cur_key, cur_val, cur_pattern
    for cur_row in zip(*full_dict.values()):
        random_pattern = list(random.choice(patterns))
        for cur_key, cur_val, cur_pattern in zip(key_names, cur_row, random_pattern):
            if cur_pattern == '1':
                part_dict[cur_key].append(cur_val)
            elif cur_pattern == '0':
                part_dict[cur_key].append("")

def genExercise() -> tuple(str):
    # IP Address
    cdef list[int] newIpSplits = generateIpSplits()
    cdef str exIp = ".".join(str(x) for x in newIpSplits)

    # CIDR
    cdef int newCidr, blankCidr
    newCidr, blankCidr = generateCidr()
    cdef str exCidr = '/' + str(newCidr)

    # Subnet mask
    cdef list[str] maskSplitBin
    cdef str exMask
    maskSplitBin, exMask = getMaskFromCidr(newCidr, blankCidr)

    # Net, Broadcast, Min and Max IP
    cdef str exNetIp, exBroadIp, exMinIp, exMaxIp
    exNetIp, exBroadIp, exMinIp, exMaxIp = getNetAndBroadIp(maskSplitBin, newIpSplits)

    # Host number
    cdef str exMaxHosts = str((2**blankCidr) - 2)

    if newCidr >= 31:
        exMinIp = exMaxIp = "[Sin IP utilizables]"
        exMaxHosts = "0 [CIDR /31]"

    return (exIp, exCidr, exMask, exNetIp, exBroadIp, exMinIp, exMaxIp, exMaxHosts)
