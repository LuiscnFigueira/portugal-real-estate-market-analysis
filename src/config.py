from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

RAW_DATA_FILE = RAW_DATA_DIR / "portugal_listinigs.csv"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "portugal_listings_initial_clean.csv"
PREPARED_DATA_FILE = PROCESSED_DATA_DIR / "portugal_listings_prepared.csv"
FEATURE_DATA_FILE = PROCESSED_DATA_DIR / "portugal_listings_features.csv"
FEATURE_DATA_COMPRESSED_FILE = PROCESSED_DATA_DIR / "portugal_listings_features.csv.gz"

REFERENCE_YEAR = 2026
