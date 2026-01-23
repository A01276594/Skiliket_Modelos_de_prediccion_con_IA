import pandas as pd
from pathlib import Path

BASE_DEVICES = Path("data/devices")

for device_dir in BASE_DEVICES.iterdir():
    if not device_dir.is_dir() or not device_dir.name.startswith("device_"):
        continue

    i = device_dir.name.split("_")[1]
    pivot_path = device_dir / f"pivot_{i}.csv"

    if not pivot_path.exists():
        print(f"⚠️ No existe {pivot_path}")
        continue

    # Leer CSV
    df = pd.read_csv(pivot_path)

    # Renombrar Time -> time
    if "Time" in df.columns:
        df = df.rename(columns={"Time": "time"})
    else:
        print(f"⚠️ {pivot_path} no tiene columna 'Time'")
        continue

    # Convertir a datetime
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"])

    # Redondear a minuto
    df["time"] = df["time"].dt.floor("min")

    # Columnas numéricas (todas menos time)
    value_cols = df.columns.drop("time")

    # Agrupar por minuto (promedio)
    df_min = (
        df.groupby("time", as_index=False)[value_cols]
        .mean(numeric_only=True)
        .sort_values("time")
    )

    # Guardar sin pisar el original
    out_path = device_dir / f"pivot_{i}_min.csv"
    df_min.to_csv(out_path, index=False)

    print(f"✅ device_{i}: creado {out_path.name}")

