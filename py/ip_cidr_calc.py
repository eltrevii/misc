import copy
import sys

def main(isDebug:bool=False)->None:
    try:
        ipInput = sys.argv[1]
    except:
        ipInput = input("Formato de ejemplo: 192.168.12.22/16\nEspecifique Dirección IP con CIDR: ") or "203.0.113.18/27"

    inSplit = ipInput.split('/')
    ipAddr  =     inSplit[0]
    ipCidr  = int(inSplit[1])

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
    

    ipSplits = [ int(i) for i in ipAddr.split(".") ]

    # https://stackoverflow.com/a/13673133
    split_bytes = lambda x, c_chunks=None, c_size=8: [ x[i:i+c_size] for i in range(0, c_chunks or len(x), c_size) ]

    maskBinSplit = split_bytes(netMaskBin)
    
    netMaskDec = '.'.join([ str(int(i, 2)) for i in maskBinSplit ])
    results.append("Net mask (decimal): " + str(netMaskDec))

    ipBinFull = [ bin(i).replace('0b', '').rjust(8, "0") for i in ipSplits ]

    calc_netIp = []
    calc_broadIp = []
    for a, b in zip(ipBinFull, maskBinSplit):
        for a, b in zip(a, b):
            curIpBit      = int(a)
            curMaskBit    = int(b)
            curMaskInvert = (1 - curMaskBit) % 2
            
            curNetIp = curIpBit and curMaskBit
            calc_netIp.append(str(curNetIp))
            calc_broadIp.append(str(curNetIp or curMaskInvert))

    joinNetIp   = ''.join(calc_netIp)
    joinBroadIp = ''.join(calc_broadIp)

    splitNetIp   = split_bytes(joinNetIp)
    splitBroadIp = split_bytes(joinBroadIp)

    newNetIp   = '.'.join([ str(int(i, 2)) for i in splitNetIp ])
    newBroadIp = '.'.join([ str(int(i, 2)) for i in splitBroadIp ])

    results.extend([
        "Net IP: "       + str(newNetIp),
        "Broadcast IP: " + str(newBroadIp)
    ])

    print(results)

if __name__=="__main__":
    main()