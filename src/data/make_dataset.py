from __future__ import annotations

from src.config import PROCESSED_DATA_FILE, RAW_DATA_FILE
from src.data.preprocess import build_initial_dataset, load_raw_data


def main() -> None:
    raw = load_raw_data(RAW_DATA_FILE)
    processed = build_initial_dataset(raw)

    PROCESSED_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(PROCESSED_DATA_FILE, index=False)

    print(f"Dataset processado guardado em: {PROCESSED_DATA_FILE}")
    print(f"Linhas: {processed.shape[0]}")
    print(f"Colunas: {processed.shape[1]}")


if __name__ == "__main__":
    main()

