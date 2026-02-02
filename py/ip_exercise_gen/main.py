import sys
import random
import copy
import pandas as pd

# LAMBDA FUNCTIONS
split_bytes = lambda x, c_chunks=None, c_size=8: [ x[i:i+c_size] for i in range(0, c_chunks or len(x), c_size) ]
binFloodToDots = lambda x: '.'.join([ str(int(i, 2)) for i in x ])

def getIpSplits() -> list:
    newIpSegments  = []
    ipFirstSegment = random.randint(10, 200)
    newIpSegments.append(ipFirstSegment)
    for i in range(3):
        otherIpSegments = random.randint(0, 255)
        newIpSegments.append(otherIpSegments)
    #finalIp = '.'.join(newIpSegments)
    return newIpSegments

def getMaskFromCidr(pCidr, pBlankCidr) -> tuple[str, list, str]:
    newMaskBin = "1" * pCidr + "0" * pBlankCidr
    maskBinSplit = split_bytes(newMaskBin)
    maskDecFinal = binFloodToDots(maskBinSplit)
    return newMaskBin, maskBinSplit, maskDecFinal

def getNetAndBroadIp(pMaskBinSplit, pIpSplits):
    ipBinFull = [ bin(curIpChunk).replace('0b', '').zfill(8) for curIpChunk in pIpSplits ]

    calc_netIp = []
    calc_broadIp = []
    for a, b in zip(ipBinFull, pMaskBinSplit):
        for a, b in zip(a, b):
            curIpBit   = int(a)
            curMaskBit = int(b)

            curNetIp = curIpBit and curMaskBit
            calc_netIp.append(str(curNetIp))
            calc_broadIp.append(str(curNetIp or int(not curMaskBit)))

    joinNetIp    = ''.join(calc_netIp)
    joinBroadIp  = ''.join(calc_broadIp)

    splitNetIp    = split_bytes(joinNetIp)
    splitBroadIp  = split_bytes(joinBroadIp)

    splitMinIp    = copy.deepcopy(splitNetIp)
    splitMaxIp    = copy.deepcopy(splitBroadIp)

    decSplitMin   = int(splitMinIp[3], 2)
    decSplitMax   = int(splitMaxIp[3], 2)

    newDecMinIp   = bin(decSplitMin + 1).replace('0b', '').zfill(8)
    newDecMaxIp   = bin(decSplitMax - 1).replace('0b', '').zfill(8)

    splitMinIp[3] = newDecMinIp
    splitMaxIp[3] = newDecMaxIp

    newNetIp   = binFloodToDots(splitNetIp)
    newBroadIp = binFloodToDots(splitBroadIp)

    newMinIp   = binFloodToDots(splitMinIp)
    newMaxIp   = binFloodToDots(splitMaxIp)

    return newNetIp, newBroadIp, newMinIp, newMaxIp

def main(isDebug:bool=False)->None:
    try:    argIpAmount = sys.argv[1]
    except: argIpAmount = input("¿Cuántos ejercicios desea? (mínimo 1, máximo 1.000.000) ")

    ipAmount = int(argIpAmount)

    dExerciseFullData = {
        "IP/Rangos IP": [],
        "CIDR":         [],
        "Máscara":      [],
        "IP Red":       [],
        "IP Broadcast": [],
        "IP Mínima":    [],
        "IP Máxima":    [],
        "Número hosts": []
    }
    dExercisePartData = copy.deepcopy(dExerciseFullData)

    for i in range(ipAmount):
        # IP Address
        newIpSplits = getIpSplits()
        exerciseIp = '.'.join([str(curIpChunk) for curIpChunk in newIpSplits])
        # CIDR
        newCidr      = random.randint(4, 31)
        blankCidr    = 32 - newCidr
        exerciseCidr = "/" + str(newCidr)
        # Subnet mask
        maskBin, maskSplitBin, exerciseMask = getMaskFromCidr(newCidr, blankCidr)
        # Net, Broadcast, Min and Max IP
        exerciseNetIp, exerciseBroadIp, exerciseMinIp, exerciseMaxIp = getNetAndBroadIp(maskSplitBin, newIpSplits)
        # Hosts #
        exerciseMaxHosts  = 2**blankCidr - 2

        if (newCidr >= 31):
            exerciseMinIp    = exerciseMaxIp = "[No hay IPs utilizables]"
            exerciseMaxHosts = "0 (CIDR /31)"

        dExerciseFullData["IP/Rangos IP"].append(exerciseIp)
        dExerciseFullData["CIDR"].append(exerciseCidr)
        dExerciseFullData["Máscara"].append(exerciseMask)
        dExerciseFullData["IP Red"].append(exerciseNetIp)
        dExerciseFullData["IP Broadcast"].append(exerciseBroadIp)
        dExerciseFullData["IP Mínima"].append(exerciseMinIp)
        dExerciseFullData["IP Máxima"].append(exerciseMaxIp)
        dExerciseFullData["Número hosts"].append(exerciseMaxHosts)

        #print(str(exerciseIp) + str(exerciseCidr), exerciseNetIp, exerciseBroadIp, exerciseMinIp, exerciseMaxIp, exerciseMaxHosts)
    selective_keep_patterns = [
        '10100000',
        '11000000',
        '10000001',
        '01010000',
        '00110000',
        '00010001',
        '01001000',
        '00101000'
    ]

    key_names = list(dExerciseFullData.keys())
    for cur_row in zip(*dExerciseFullData.values()):
        random_pattern = list(random.choice(selective_keep_patterns))
        for cur_key, cur_val, cur_pattern in zip(key_names, cur_row, random_pattern):
            if cur_pattern == '1':
                dExercisePartData[cur_key].append(cur_val)
            elif cur_pattern == '0':
                dExercisePartData[cur_key].append("")

    df_all = {
        "Ejercicios IP EN BLANCO":  pd.DataFrame(dExercisePartData),
        "Ejercicios IP CORREGIDOS": pd.DataFrame(dExerciseFullData)
    }

    file_name = "EJERCICIOS_IP.xlsx"

    # https://stackoverflow.com/a/40535454
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as pdWriter:
        for cur_sheet_name, cur_df in df_all.items():
            cur_df.to_excel(pdWriter, sheet_name=cur_sheet_name, index=False)
            gotWorksheet = pdWriter.sheets[cur_sheet_name]
            for idx, col in enumerate(cur_df):
                series  = cur_df[col]
                max_len = max((
                    series.astype(str).map(len).max(), # len of largest item
                    len(str(series.name)),             # len of header
                )) + 1
                gotWorksheet.set_column(idx, idx, max_len)

if __name__=="__main__":
    main()
