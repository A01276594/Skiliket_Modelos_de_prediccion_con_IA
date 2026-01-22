from pathlib import Path

BASE_DIR = Path("data/devices")

for device_dir in BASE_DIR.iterdir():
    if not device_dir.is_dir() or not device_dir.name.startswith("device_"):
        continue

    print(f"🧹 Limpiando {device_dir.name}")

    for file in device_dir.iterdir():
        if file.is_file():
            if (
                file.name.startswith("pivot_")
                or file.name.endswith("_FULL_HISTORY.csv")
            ):
                file.unlink()
                print(f"   ❌ eliminado {file.name}")
