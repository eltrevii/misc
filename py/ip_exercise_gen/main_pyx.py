import sys
import copy
import random

import pandas as pd
from xlsxwriter.workbook import Workbook

import time
import ip_data_manip as ip

SELECTIVE_KEEP_PATTERNS = [
    "10100000",
    "11000000",
    "10000001",
    "01010000",
    "00110000",
    "00010001",
    "01001000",
    "00101000",
]

# BEGIN column solution https://stackoverflow.com/a/73320573
def get_max_len(series):
    return max(
        series.astype(str).map(len).max(), # len of largest item
        len(str(series.name)),             # len of header
    ) + 1

def export_excel(dframes: dict[pd.Dataframe], file_path_out: str):
    with pd.ExcelWriter(file_path_out, engine='xlsxwriter') as writer:
        for sheet_name, frame in dframes.items():
            df = pd.DataFrame(frame)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            for idx, col in enumerate(df):
                series = df[col]
                max_len = get_max_len(series)
                worksheet.set_column(idx, idx, max_len)
# END column solution

def main():
    try:
        argIpAmount: str = sys.argv[1]
    except:
        argIpAmount: str = input("¿Cuántos ejercicios desea? (mínimo 1, máximo 1.000.000) ")

    start_time = time.perf_counter()

    ipCount: int = int(argIpAmount)

    dExerciseFullData: dict[str, list[str]] = {
        "IP/Rangos IP": [],
        "CIDR":         [],
        "Máscara":      [],
        "IP Red":       [],
        "IP Broadcast": [],
        "IP Mínima":    [],
        "IP Máxima":    [],
        "Número hosts": [],
    }
    dExercisePartData: dict[str, list[str]] = copy.deepcopy(dExerciseFullData)

    for i in range(ipCount):
        addExercise(dExerciseFullData)

    ip.add_selective(dExerciseFullData, dExercisePartData, SELECTIVE_KEEP_PATTERNS)

    all_dataframes = {
        "Ejercicios IP EN BLANCO":  dExercisePartData,
        "Ejercicios IP CORREGIDOS": dExerciseFullData,
    }

    file_name = "EJERCICIOS_IP.xlsx"

    end_time = time.perf_counter()
    print(f"FINISHED IN {end_time - start_time}")

    export_excel(all_dataframes, file_name)

    end_write = time.perf_counter()
    print(f"WRITE IN {end_write - end_time}")
    print(f"TOTAL:   {end_write - start_time}")


def addExercise(target_dict):
    calcResults: tuple = ip.genExercise()

    for key, val in zip(target_dict.keys(), calcResults):
        target_dict[key].append(val)

if __name__ == "__main__":
    main()
