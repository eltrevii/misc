import copy
import sys

def main(isDebug:bool=False)->None:
    try:
        ipInput = sys.argv[1]
    except:
        ipInput = input("Formato de ejemplo: 192.168.12.22/16\nEspecifique Dirección IP con CIDR: ") or "203.0.113.18/27"

    inSplit = ipInput.split('/')
    ipAddr =     inSplit[0]
    ipCidr = int(inSplit[1])

    maxCIDR = 32
    blankCidr = maxCIDR - ipCidr

    results = []
    netMaxHosts = (2**blankCidr) - 2
    results.append("Net max hosts: " + str(netMaxHosts))

    if (ipCidr <= 8):
        maskAndSplit = 0
    elif (ipCidr <= 16):
        maskAndSplit = 1
    elif (ipCidr <= 24):
        maskAndSplit = 2
    elif (ipCidr <= 32):
        maskAndSplit = 3
    else:
        # TODO ADD ERROR
        return

    netMaskBin = ("1" * ipCidr) + ("0" * blankCidr)
    maskSplitChunks, maskSplitChunkSize = len(netMaskBin), 8

    ipSplits = [ int(i) for i in ipAddr.split(".") ]

    # https://stackoverflow.com/a/13673133
    netMaskBinSplit = [ netMaskBin[i:i+maskSplitChunkSize] for i in range(0, maskSplitChunks, maskSplitChunkSize) ]

    netMaskDec = [ int(i, 2) for i in netMaskBinSplit ]
    results.append("Net mask (decimal): " + str(netMaskDec))

    ipBinFull = [ bin(i).replace('0b', '').rjust(8, "0") for i in ipSplits ]

    calc_netIp = []
    calc_broadIp = []
    for a, b in zip(ipBinFull[maskAndSplit], netMaskBinSplit[maskAndSplit]):
        for a, b in zip(a, b):
            curIpBit   = int(a)
            curMaskBit = int(b)
            print(curMaskBit, end='')
            curNetIp = curIpBit and curMaskBit
            calc_netIp.append(str(curNetIp))
            calc_broadIp.append(str(curNetIp or (1 - curMaskBit) % 2))
    
    netIpCopy = copy.deepcopy(ipSplits)
    netIpCopy[maskAndSplit] = int(''.join(calc_netIp), 2)
    results.append("Net IP: " + str(netIpCopy))

    # netIpBin = [ bin(i).replace('0b', '').rjust(8, "0") for i in netIpCopy ]

    # calc_broadIp = []
    # for a, b in zip(netIpBin[maskAndSplit], netMaskBinSplit[maskAndSplit]):
    #     for a, b in zip(a, b):
    #         curIpBit   = int(a)
    #         curMaskBit = int(b)

    #         calc_broadIp.append(str(curIpBit or curMaskBit))

    newBroadIp = copy.deepcopy(ipSplits)
    newBroadIp[maskAndSplit] = int(''.join(calc_broadIp), 2)

    results.append("Broadcast IP: " + str(newBroadIp))

    print(results)

if __name__=="__main__":
    main()