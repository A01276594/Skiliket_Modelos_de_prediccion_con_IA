import pandas as pd
from pathlib import Path

BASE_DEVICES = Path("data/devices")
OUT_BASE = Path("data/var")
OUT_BASE.mkdir(parents=True, exist_ok=True)

# detecta devices disponibles (device_1 ... device_7)
device_dirs = sorted([d for d in BASE_DEVICES.iterdir() if d.is_dir() and d.name.startswith("device_")],
                     key=lambda p: int(p.name.split("_")[1]))

# agarra la lista de variables desde device_1/variables (puedes cambiarlo si quieres)
vars_dir0 = device_dirs[0] / "variables"
var_files = sorted(vars_dir0.glob("*.csv"))

for vf in var_files:
    # nombre variable: "AQI_1.csv" -> "AQI"
    var_name = vf.stem.rsplit("_", 1)[0]

    frames = []

    for d in device_dirs:
        device_id = int(d.name.split("_")[1])
        f = d / "variables" / f"{var_name}_{device_id}.csv"
        if not f.exists():
            print(f"⚠️ Falta {f}")
            continue

        df = pd.read_csv(f)

        # detecta columna de tiempo
        time_col = None
        for c in ["time", "Time", "created_at", "timestamp"]:
            if c in df.columns:
                time_col = c
                break
        if time_col is None:
            raise ValueError(f"No encuentro columna time en {f}. Columnas: {df.columns.tolist()}")

        # detecta columna de valor (la otra)
        value_col = [c for c in df.columns if c != time_col][0]

        df = df.rename(columns={time_col: "time", value_col: f"dev_{device_id}"})
        df["time"] = pd.to_datetime(df["time"], errors="coerce")

        # si hay repetidos por time, promedia (evita errores de merge)
        df = df.dropna(subset=["time"]).groupby("time", as_index=False).mean(numeric_only=True)

        frames.append(df)

    if not frames:
        continue

    # merge por time (outer para conservar tiempos aunque falten devices)
    wide = frames[0]
    for nxt in frames[1:]:
        wide = wide.merge(nxt, on="time", how="outer")

    wide = wide.sort_values("time")

    # guardar
    out_dir = OUT_BASE / var_name
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"{var_name}_wide.csv"
    wide.to_csv(out_file, index=False)

    print(f"✅ {var_name}: guardado {out_file}")
