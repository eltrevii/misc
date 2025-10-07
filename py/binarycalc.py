
def dbgPrint(pText: str, end: str = '\n') -> None:
    try:
        _dbg
    except NameError:
        return
    print(pText, end=end)

def main():
    print("")
    print("INTRODUCE UN NUMERO")
    num1: str = input("> ")
    num2: str = input("> ")

    num1 = num1[::-1]
    num2 = num2[::-1]

    lSums = []
    fIdx = 0
    iCarry = 0
    for i, items in enumerate(zip(num1, num2)):
        iSum = int(items[0]) + int(items[1])
        dbgPrint(f"{items[0]} + {items[1]} ", end="")
        lCarries = []
        match iSum:
            case 0: # 0 + 0
                sToAppend = ['0' if (iCarry == 0) else '1'][0]
                dbgPrint(f"+ {iCarry} = {sToAppend}, carry 0")
                lSums.append(sToAppend) 
                iCarry = 0
            case 1: # 1 + 0 / 0 + 1
                if iCarry == 0:
                    dbgPrint(f"+ {iCarry} = 1, carry 0")
                    lSums.append('1')
                    iCarry = 0
                else:
                    dbgPrint(f"+ {iCarry} = 0, carry 1")
                    lSums.append('0')
                    iCarry = 1
            case 2: # 1 + 1
                sToAppend = ['0' if (iCarry == 0) else '1'][0]
                dbgPrint(f"+ {iCarry} = {sToAppend}, carry 1")
                lSums.append(sToAppend)
                iCarry = 1
    
    if iCarry == 1:
        lSums.append('1')
 
    sFinalSum = ''.join(lSums)[::-1]
    print("\nRESPUESTA: " + sFinalSum)

if __name__=="__main__":
    main()