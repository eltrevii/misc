import requests
import re
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from rich import print as rprint
from rich.prompt import IntPrompt

own_path = Path(__file__).resolve()

munic_filepath = (own_path.parent / "municipalities.json")
all_munic = json.loads(munic_filepath.read_text(encoding="utf-8"))

rprint("[green]BIZKAIBUS STOP TOOL [yellow]-[/yellow] by [cyan]eltrevii")
print()

api_baseurl = 'http://apli.bizkaia.net/APPS/DANOK/TQWS/TQ.ASMX/'

def mp(patname):
    """Returns regex pattern from html tag name as in: <tag>(.*)</tag>"""
    return f"<{patname}>(.*?)</{patname}>"

def cmd_browse(args):
    maxlen_allmun = len(max(all_munic.keys(), key=len))
    maxlen_am_val = len(str(max(all_munic.values(), key=lambda x: len(str(x)))))
    txt_allmun = "Municipios de Bizkaia:"
    txt_enter_num = "Por favor, introduzca el número correspondiente a su municipio"
    sep = "[blue]" + "=" * (maxlen_allmun + 2 + maxlen_am_val)

    rprint(f"[green]{txt_allmun}")
    rprint(sep)
    for k, v in sorted(all_munic.items(), key=lambda x: x[0]):
        k_padded = f"{k:>{maxlen_allmun}}"
        rprint(f"[yellow][green]{k_padded}[/green]: [cyan]{v}[/cyan]")

    rprint(sep + '\n')
    api_mun_id = IntPrompt.ask(f"[yellow]{txt_enter_num}")

    api_url = api_baseurl + '/GetParadasMunicipio_JSON'
    api_params = {
        'callback': '', # or jsonParadas
        'iCodigoProvincia': 48, # bizkaia
        'iCodigoMunicipio': api_mun_id
    }

    r = requests.get(api_url, params=api_params)
    if not r.ok: return

    sel_stop = list(all_munic.keys())[list(all_munic.values()).index(api_mun_id)]
    rprint(f"[green]Paradas en [cyan]{sel_stop}[/cyan]:")
    rprint(sep)

    reqp1 = r.text.lstrip("(").rstrip(");")
    reqp1 = json.loads(reqp1.replace("'", "\""))["Consulta"]["Paradas"]

    req_stops = [ x["DENOMINACION"] for x in reqp1 ]
    maxlen_stops = len(max(req_stops, key=len))

    for stop in sorted(reqp1, key=lambda x: x["DENOMINACION"]):
        data_stop = stop["CODIGOREDUCIDOPARADA"]
        data_stopname = stop["DENOMINACION"].replace("( ", "(").replace(") ", ")")
        data_stopname = f"{data_stopname:<{maxlen_stops}}"
        data_address = stop["DIRECCION"].replace("¦", "º")
        rprint(f"[yellow] * [green]ID: {data_stop}[/green] :: [green]{data_stopname}[/green] :: [green]DONDE:[/green] [cyan]{data_address}[/cyan]")

def cmd_stoptimes(args):
    api_url = api_baseurl + '/GetPasoParadaMobile_JSON'
    api_params = {
        'callback': '',
        'strLinea': '',
        'strParada': int(args.stop_number)
    }

    pattern_base = mp("GetPasoParadaResult")

    pattern_stopname = mp("DenominacionParada")
    pattern_stops = mp("PasoParada")

    pattern_mins = mp("minutos")
    pattern_line = mp("linea")
    pattern_dest = mp("ruta")

    rprint(f"[yellow]Sending request for stop [cyan]{api_params['strParada']}[/cyan]...")

    r = requests.get(api_url, params=api_params)
    if not r.ok: return

    reqp1 = r.text.lstrip("(").rstrip(");")
    reqp1 = json.loads(reqp1.replace("'", "\""))["Resultado"]

    busdata = re.search(pattern_base, reqp1).group(1) # filter out the result tag
    data_stopname = re.search(pattern_stopname, busdata).group(1)
    data_stops = re.findall(pattern_stops, busdata, re.DOTALL)

    txt_stop = "PARADA:"
    sep = "[blue]" + "=" * max(35, 3 + (len(txt_stop) + 1 + len(data_stopname)))
    rprint(sep)
    rprint(f"[yellow]== [green]{txt_stop}[/green] [cyan]{data_stopname}")
    for stop in data_stops:
        data_mins = re.search(pattern_mins, stop).group(1)
        data_line = re.search(pattern_line, stop).group(1)
        data_dest = re.search(pattern_dest, stop).group(1)

        rprint(f"[yellow] * [green]BUS [cyan]{data_line}[/cyan][/green] :: [green]{data_dest}[/green] :: [green][cyan]{data_mins}[/cyan] MIN[/green]")

    rprint(sep)

#region COMMAND PARSING
parser = ArgumentParser(prog=Path(__file__).name)
parser.set_defaults(func=lambda *a, **b: parser.parse_args(["--help"]))
subp = parser.add_subparsers()

sp_browse = subp.add_parser("browse", help="Browses all Bizkaibus stops")
sp_browse.set_defaults(func=cmd_browse)

sp_stopnum = subp.add_parser("stoptimes", help="Gets remaining time for a stop number")
sp_stopnum.add_argument('stop_number', help="The number for the stop")
sp_stopnum.set_defaults(func=cmd_stoptimes)

args = parser.parse_args()

try:
    args.func(args)
except KeyboardInterrupt:
    pass
#endregion
