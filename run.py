import logging
from pathlib import Path

import pandas as pd

from src.analyzer import OrderAnalyzer


def setup_logger(logs_dir):
    logs_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_file = logs_dir / "errors.log"

    logger = logging.getLogger("order_analysis")
    logger.setLevel(logging.ERROR)

    if not logger.handlers:
        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def save_report(results, reports_dir):
    reports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_file = reports_dir / "report.csv"

    columns = [
        "file_name",
        "total_sum",
        "average_check",
        "order_count",
    ]

    report_data = pd.DataFrame(
        results,
        columns=columns,
    )

    report_data.to_csv(
        report_file,
        index=False,
        encoding="utf-8",
    )

    return report_file


def main():
    base_dir = Path(__file__).resolve().parent

    data_dir = base_dir / "data"
    reports_dir = base_dir / "reports"
    logs_dir = base_dir / "logs"

    logger = setup_logger(logs_dir)

    analyzer = OrderAnalyzer(
        data_dir=data_dir,
        reports_dir=reports_dir,
        logs_dir=logs_dir,
        logger=logger,
        status_value="Delivered",
    )

    results, errors = analyzer.analyze_all_files()

    report_file = save_report(
        results,
        reports_dir,
    )

    print(f"Обработано файлов: {len(results)}")
    print(f"Файлов с ошибками: {len(errors)}")
    print(f"Отчёт сохранён: {report_file}")

    if errors:
        print(f"Ошибки записаны в: {logs_dir / 'errors.log'}")


if __name__ == "__main__":
    main()
