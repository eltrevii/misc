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


# https://stackoverflow.com/a/73320573
def export_excel(df: pd.Dataframe, sheet_name: str, file_path_out: str):
    workbook = Workbook(file_path_out)
    worksheet = workbook.add_worksheet(sheet_name)

    worksheet.write_row(0, 0, [col for col in df.columns])

    for index, row in df.iterrows():
        worksheet.write_row(index + 1, 0, [col for col in row])
    for idx, col in enumerate(df):
        series = df[col]
        max_len = (
            max(
                (
                    series.astype(str).map(len).max(),  # len of largest item
                    len(str(series.name)),  # len of header
                )
            )
            + 1
        )
        worksheet.set_column(idx, idx, max_len)

    workbook.close()


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
        "Ejercicios IP EN BLANCO": dExercisePartData,
        "Ejercicios IP CORREGIDOS": dExerciseFullData,
    }

    file_name = "EJERCICIOS_IP.xlsx"

    end_time = time.perf_counter()
    print(f"FINISHED IN {end_time - start_time}")

    # https://stackoverflow.com/a/40535454
    # with pd.ExcelWriter(file_name, engine='xlsxwriter') as pdWriter:
    #    for cur_sheet_name, cur_df in all_dataframes.items():
    #        df_current = pd.DataFrame(cur_df)
    #        df_current.to_excel(pdWriter, sheet_name=cur_sheet_name, index=False)
    #        gotWorksheet = pdWriter.sheets[cur_sheet_name]
    #        for idx, col in enumerate(df_current):
    #            series = df_current[col]
    #            max_len = max((
    #            series.astype(str).map(len).max(), # len of largest item
    #            len(str(series.name)),             # len of header
    #            )) + 1
    #            gotWorksheet.set_column(idx, idx, max_len)

    for cur_sheet_name, cur_df in all_dataframes.items():
        df_current = pd.DataFrame(cur_df)
        export_excel(df_current, cur_sheet_name, file_name)

    end_write = time.perf_counter()
    print(f"WRITE IN {end_write - end_time}")
    print(f"TOTAL:   {end_write - start_time}")


def addExercise(target_dict):
    calcResults: tuple = ip.genExercise()

    for key, val in zip(target_dict.keys(), calcResults):
        target_dict[key].append(val)

if __name__ == "__main__":
    main()
