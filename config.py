from pathlib import Path


# Корневая папка проекта
BASE_DIR = Path(__file__).resolve().parent


# Папки проекта
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"


# Итоговый отчёт
OUTPUT_FILENAME = "report.csv"
OUTPUT_FILE = REPORTS_DIR / OUTPUT_FILENAME


# Лог ошибок
LOG_FILENAME = "errors.log"
LOG_FILE = LOGS_DIR / LOG_FILENAME


# Настройки фильтрации
STATUS_COLUMN = "status"
STATUS_VALUE = "Delivered"


# Колонка с суммой заказа
AMOUNT_COLUMN = "total_amount"


# Настройки CSV
CSV_SEPARATOR = ","
CSV_ENCODING = "utf-8"


# Обязательные колонки
REQUIRED_COLUMNS = {
    "order_id",
    "person_id",
    "order_date",
    "status",
    "total_amount",
    "currency",
    "payment_method",
    "shipping_method",
    "notes",
}
