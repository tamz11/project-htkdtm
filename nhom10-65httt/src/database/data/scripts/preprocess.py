"""
Tiền xử lý dữ liệu Hotel Booking Demand (Kaggle - jessemostipak/hotel-booking-demand)
Nhóm: nhom10-65httt | Người phụ trách: Trịnh Thị Vân

Đầu vào : ../raw/hotel_bookings.csv
Đầu ra  : ../processed/hotel_bookings_clean.csv
          ../processed/bao_cao_tien_xu_ly.txt

Cách chạy (đứng ở thư mục gốc repo):
    python nhom10-65httt/src/database/data/scripts/preprocess.py
"""

import sys
from pathlib import Path

import numpy as np

# Tránh lỗi in tiếng Việt trên terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd

# ---------------------------------------------------------------------------
# Cấu hình đường dẫn (tính theo vị trí của file script, chạy ở đâu cũng được)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # .../data
RAW_FILE = BASE_DIR / "raw" / "hotel_bookings.csv"
OUT_DIR = BASE_DIR / "processed"
OUT_FILE = OUT_DIR / "hotel_bookings_clean.csv"
REPORT_FILE = OUT_DIR / "bao_cao_tien_xu_ly.txt"

# Ngưỡng giá phòng bất thường (bộ dữ liệu có 1 dòng adr = 5400)
ADR_MAX = 1000

# Bộ dữ liệu không có mã booking nên các dòng trùng có thể là các booking
# thật giống hệt nhau (đặt theo đoàn). Mặc định GIỮ LẠI, chỉ thống kê.
DROP_DUPLICATES = False

MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11,
    "December": 12,
}

SEASON_MAP = {
    12: "Mùa đông", 1: "Mùa đông", 2: "Mùa đông",
    3: "Mùa xuân", 4: "Mùa xuân", 5: "Mùa xuân",
    6: "Mùa hè", 7: "Mùa hè", 8: "Mùa hè",
    9: "Mùa thu", 10: "Mùa thu", 11: "Mùa thu",
}

log_lines = []


def log(msg: str) -> None:
    print(msg)
    log_lines.append(msg)


# ---------------------------------------------------------------------------
# 1. Đọc dữ liệu
# ---------------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file {RAW_FILE}\n"
            "Hãy đặt hotel_bookings.csv vào thư mục data/raw/"
        )
    df = pd.read_csv(RAW_FILE)
    log(f"[1] Đọc dữ liệu: {len(df):,} dòng x {df.shape[1]} cột")
    return df


# ---------------------------------------------------------------------------
# 2. Khảo sát chất lượng dữ liệu
# ---------------------------------------------------------------------------
def profile(df: pd.DataFrame) -> None:
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    log("[2] Giá trị thiếu theo cột:")
    for col, n in missing.items():
        log(f"    - {col}: {n:,} ({n / len(df):.1%})")
    log(f"    Số dòng trùng lặp hoàn toàn: {df.duplicated().sum():,}")


# ---------------------------------------------------------------------------
# 3. Làm sạch
# ---------------------------------------------------------------------------
def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    n0 = len(df)
    log("[3] Làm sạch dữ liệu:")

    # 3.1 Giá trị thiếu
    df["children"] = df["children"].fillna(0).astype(int)
    df["country"] = df["country"].fillna("Unknown")
    df["has_agent"] = df["agent"].notna().astype(int)
    df["has_company"] = df["company"].notna().astype(int)
    df["agent"] = df["agent"].fillna(0).astype(int)      # 0 = không qua đại lý
    df["company"] = df["company"].fillna(0).astype(int)  # 0 = khách lẻ
    log("    - children thiếu -> 0; country thiếu -> 'Unknown'; "
        "agent/company thiếu -> 0 (thêm cột cờ has_agent, has_company)")

    # 3.2 Chuẩn hóa giá trị phân loại
    # Theo bài báo gốc, 'Undefined' và 'SC' đều là không kèm bữa ăn
    n_meal = (df["meal"] == "Undefined").sum()
    df["meal"] = df["meal"].replace("Undefined", "SC")
    log(f"    - meal 'Undefined' -> 'SC': {n_meal:,} dòng")
    for col in ["hotel", "meal", "market_segment", "distribution_channel",
                "customer_type", "deposit_type", "reserved_room_type",
                "assigned_room_type", "reservation_status"]:
        df[col] = df[col].astype(str).str.strip()

    # 3.3 Loại booking không có khách nào
    no_guest = (df["adults"] + df["children"] + df["babies"]) == 0
    df = df[~no_guest]
    log(f"    - Loại booking 0 người lớn, 0 trẻ em, 0 em bé: {no_guest.sum():,} dòng")

    # 3.4 Giá phòng bất thường
    bad_adr = (df["adr"] < 0) | (df["adr"] > ADR_MAX)
    df = df[~bad_adr]
    log(f"    - Loại adr < 0 hoặc > {ADR_MAX}: {bad_adr.sum():,} dòng")

    # 3.5 Trùng lặp
    if DROP_DUPLICATES:
        n_dup = df.duplicated().sum()
        df = df.drop_duplicates()
        log(f"    - Loại dòng trùng lặp: {n_dup:,} dòng")
    else:
        log("    - Giữ dòng trùng lặp (có thể là booking theo đoàn); "
            "đổi DROP_DUPLICATES = True nếu nhóm muốn loại")

    log(f"    => Còn {len(df):,} / {n0:,} dòng ({len(df) / n0:.1%})")
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# 4. Tạo cột phục vụ phân tích & KPI
# ---------------------------------------------------------------------------
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Thời gian
    df["arrival_month_num"] = df["arrival_date_month"].map(MONTH_MAP)
    df["arrival_date"] = pd.to_datetime(dict(
        year=df["arrival_date_year"],
        month=df["arrival_month_num"],
        day=df["arrival_date_day_of_month"],
    ))
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])
    df["booking_date"] = df["arrival_date"] - pd.to_timedelta(df["lead_time"], unit="D")
    df["arrival_quarter"] = df["arrival_date"].dt.quarter
    df["arrival_year_month"] = df["arrival_date"].dt.to_period("M").astype(str)
    df["arrival_weekday"] = df["arrival_date"].dt.day_name()
    df["season"] = df["arrival_month_num"].map(SEASON_MAP)

    # Lưu trú & khách
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df["total_guests"] = df["adults"] + df["children"] + df["babies"]
    df["is_day_use"] = (df["total_nights"] == 0).astype(int)
    df["is_family"] = ((df["children"] + df["babies"]) > 0).astype(int)

    # Doanh thu (chỉ tính booking không hủy)
    df["revenue"] = (df["adr"] * df["total_nights"]).round(2)
    df["realized_revenue"] = np.where(df["is_canceled"] == 0, df["revenue"], 0.0)
    df["lost_revenue"] = np.where(df["is_canceled"] == 1, df["revenue"], 0.0)

    # Vận hành
    df["room_changed"] = (df["reserved_room_type"] != df["assigned_room_type"]).astype(int)
    df["lead_time_group"] = pd.cut(
        df["lead_time"],
        bins=[-1, 7, 30, 90, 180, 10_000],
        labels=["0-7 ngày", "8-30 ngày", "31-90 ngày", "91-180 ngày", ">180 ngày"],
    ).astype(str)

    # Mã booking để nạp vào database
    df.insert(0, "booking_id", range(1, len(df) + 1))

    log(f"[4] Thêm cột phân tích -> tổng {df.shape[1]} cột")
    return df


# ---------------------------------------------------------------------------
# 5. Kiểm tra nhanh & xuất file
# ---------------------------------------------------------------------------
def summarize(df: pd.DataFrame) -> None:
    log("[5] Tóm tắt nhanh sau xử lý:")
    log(f"    - Khoảng thời gian đến: {df['arrival_date'].min().date()} "
        f"-> {df['arrival_date'].max().date()}")
    log(f"    - Tỷ lệ hủy: {df['is_canceled'].mean():.1%}")
    kept = df[df["is_canceled"] == 0]
    log(f"    - ADR trung bình (booking không hủy): {kept['adr'].mean():.2f}")
    log(f"    - Tổng doanh thu thực tế: {df['realized_revenue'].sum():,.0f}")
    by_hotel = df.groupby("hotel").agg(
        so_booking=("booking_id", "count"),
        ty_le_huy=("is_canceled", "mean"),
        adr_tb=("adr", "mean"),
        doanh_thu=("realized_revenue", "sum"),
    )
    log("    - Theo loại khách sạn:")
    for hotel, r in by_hotel.iterrows():
        log(f"        {hotel}: {r.so_booking:,.0f} booking | hủy {r.ty_le_huy:.1%} | "
            f"ADR {r.adr_tb:.2f} | doanh thu {r.doanh_thu:,.0f}")
    assert df.isna().sum().sum() == 0, "Vẫn còn giá trị thiếu!"
    log("    - Kiểm tra: không còn giá trị thiếu ✔")


def save(df: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
    log(f"[6] Đã lưu: {OUT_FILE}")
    REPORT_FILE.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"    Báo cáo: {REPORT_FILE}")


def main() -> None:
    df = load_data()
    profile(df)
    df = clean(df)
    df = add_features(df)
    summarize(df)
    save(df)


if __name__ == "__main__":
    main()