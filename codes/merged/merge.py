import pandas as pd
from pathlib import Path
from functools import reduce

# =========================
# 1. Paths del proyecto
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "csvs"     # o "dbs" si así se llama
OUTPUT_DIR_BASE = PROJECT_ROOT / "data" / "devices"

# =========================
# 2. Configuración del device
# =========================

DEVICE_ID = 1

OUTPUT_DIR = OUTPUT_DIR_BASE / f"device_{DEVICE_ID}"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# 3. Archivos por variable
# =========================

files = {
    "AQI": f"device_{DEVICE_ID}_AQI.csv",
    "ECO2": f"device_{DEVICE_ID}_ECO2.csv",
    "Humidity": f"device_{DEVICE_ID}_Humidity.csv",
    "Noise": f"device_{DEVICE_ID}_Noise.csv",  
    "Soil_Moisture": f"device_{DEVICE_ID}_Soil_Moisture.csv",
    "TVOC": f"device_{DEVICE_ID}_TVOC.csv",
    "Temperature": f"device_{DEVICE_ID}_Temperature.csv",
    "UV_Intensity": f"device_{DEVICE_ID}_UV_Intensity.csv",
}

# =========================
# 4. Función de carga/limpieza
# =========================

def load_clean(path: Path, var_name: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # columnas necesarias
    df = df[["device_id", "time", "value"]].copy()

    # parseo de tiempo
    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    # renombrar variable
    df = df.rename(columns={"value": var_name})

    # redondear a minuto (clave para merge)
    df["time"] = df["time"].dt.floor("min")

    # limpieza mínima
    df = df.dropna(subset=["device_id", "time"])

    return df

# =========================
# 5. Cargar, agrupar y mergear
# =========================

dfs = []

for var, fname in files.items():
    path = DATA_DIR / fname

    df_var = load_clean(path, var)

    # asegurar que solo sea este device
    df_var = df_var[df_var["device_id"] == DEVICE_ID]

    # agregar por minuto (por si hay varias mediciones)
    df_var = (
        df_var
        .groupby(["device_id", "time"], as_index=False)[var]
        .mean()
    )

    dfs.append(df_var)

# merge outer para no perder info
df_merged = reduce(
    lambda left, right: pd.merge(
        left, right,
        on=["device_id", "time"],
        how="outer"
    ),
    dfs
)

df_merged = df_merged.sort_values("time").reset_index(drop=True)

# =========================
# 6. Guardar resultado
# =========================

output_path = OUTPUT_DIR / f"device_{DEVICE_ID}_merged.csv"
df_merged.to_csv(output_path, index=False)

print(f"Archivo guardado en: {output_path.resolve()}")
