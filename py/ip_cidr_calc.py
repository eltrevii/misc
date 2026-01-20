import sys

# LAMBDA FUNCTIONS
##################
# ONLY next line: https://stackoverflow.com/a/13673133
    split_bytes = lambda x, c_chunks=None, c_size=8: [ x[i:i+c_size] for i in range(0, c_chunks or len(x), c_size) ]
    binFloodToDots = lambda x: '.'.join([ str(int(i, 2)) for i in x ])

def main(isDebug:bool=False)->None:
    try:    ipInput = sys.argv[1]
    except: ipInput = input("Formato de ejemplo: 192.168.12.22/16\nEspecifique Dirección IP con CIDR: ")

    inSplit = ipInput.split('/')
    ipAddr  =     inSplit[0]
    ipCidr  = int(inSplit[1])

    if (ipCidr > 32): return

    maxCIDR   = 32
    blankCidr = maxCIDR - ipCidr
    netMaxHosts = (2**blankCidr) - 2

    netMaskBin = ("1" * ipCidr) + ("0" * blankCidr)

    ipSplits = [ int(i) for i in ipAddr.split(".") ]

    maskBinSplit = split_bytes(netMaskBin)
    netMaskDec = binFloodToDots(maskBinSplit)

    ipBinFull = [ bin(i).replace('0b', '').zfill(8) for i in ipSplits ]

    calc_netIp = []
    calc_broadIp = []
    for a, b in zip(ipBinFull, maskBinSplit):
        for a, b in zip(a, b):
            curIpBit   = int(a)
            curMaskBit = int(b)

            curNetIp = curIpBit and curMaskBit
            calc_netIp.append(str(curNetIp))
            calc_broadIp.append(str(curNetIp or int(not curMaskBit)))

    joinNetIp   = ''.join(calc_netIp)
    joinBroadIp = ''.join(calc_broadIp)

    splitNetIp   = split_bytes(joinNetIp)
    splitBroadIp = split_bytes(joinBroadIp)

    newNetIp   = binFloodToDots(splitNetIp)
    newBroadIp = binFloodToDots(splitBroadIp)

    results = [
        ("Max hosts",    str(netMaxHosts)),
        ("Subnet mask",  str(netMaskDec) ),
        ("Network IP",   str(newNetIp)   ),
        ("Broadcast IP", str(newBroadIp) )
    ]

    maxLen_results = [ max([len(i[0]) for i in results]),
                       max([len(i[1]) for i in results]) ]

    [ print(i[0].rjust(maxLen_results[0]), ":", i[1]) for i in results ]

if __name__=="__main__":
    main()