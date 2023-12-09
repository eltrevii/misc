import requests as re, json as js, os

def main():
	nttext = []
	tftext = ""

	clear()

	ogstr = input("texto en el lenguaje original (ingles): ")
	nwstr = ogstr.split(" ")

	print("\ntraduciendo...")

	try:
		print("")
		
		ntext = []


		for i in nwstr:
			if i == "want"  : i = "i want"
			if i == "wanted": i = "i wanted"
			ntext.append(i)

		p_max = len(ntext)
		p_all = [i for i in range(1, p_max + 1)]
		
		pstr  = "[{0:>%d}/{1:>%d}] {2:<%d} =" % (len(str(p_max)), len(str(p_max)), len(max(ntext, key=len)))
		plist = []

		for i in range(len(p_all)):
			plist.append(pstr.format(p_all[i], p_max, ntext[i]))

		for idx, i in enumerate(ntext):
			print(f"{plist[idx]}", end="")
			r = re.post(f"https://libretranslate.org/translate?q={i}&source=en&target=es&format=text&api_key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").text
			
			trtext = js.loads(r)['translatedText']
			if trtext == "i": trtext = "yo"
			print(f" {trtext}")
			nttext.append(trtext)

	except Exception as e:
		print(f"\n\nerror: {e}")
		return 1

	
	otstr = re.post(f"https://libretranslate.org/translate?q={ogstr}&source=en&target=es&format=text&api_key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").text

	for i in nttext:
		tftext += i + " "

	print("")
	print(f"texto traducido: {tftext}")
	print(f"texto original : {js.loads(otstr)['translatedText']}")
	print("\nadvertencia: el texto original traducido podria no ser 100% preciso")

def clear(): os.system("cls") if os.name == "nt" else os.system("clear")

if __name__ == '__main__':
	main()