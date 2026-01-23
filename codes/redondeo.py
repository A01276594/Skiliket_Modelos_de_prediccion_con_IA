import pandas as pd
from pathlib import Path

VAR_DIR = Path("data/var")

# busca todos los wide.csv
wide_files = list(VAR_DIR.rglob("*_wide.csv"))

for f in wide_files:
    df = pd.read_csv(f)

    # time a datetime
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"])

    # redondear hacia abajo a minuto
    df["time"] = df["time"].dt.floor("min")

    # columnas dev_*
    dev_cols = [c for c in df.columns if c.startswith("dev_")]

    # agrupar por minuto (promedia si hay repetidos)
    df_min = df.groupby("time", as_index=False)[dev_cols].mean()

    # ordenar
    df_min = df_min.sort_values("time")

    # guardar como *_wide_min.csv (no pisa el original)
    out_path = f.with_name(f.stem + "_min.csv")
    df_min.to_csv(out_path, index=False)

    print(f"✅ {f.name} -> {out_path.name}")
