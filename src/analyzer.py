from pathlib import Path

import pandas as pd


class OrderAnalyzer:
    def __init__(
        self,
        data_dir,
        reports_dir,
        logs_dir,
        logger=None,
        status_value="Delivered",
    ):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.logs_dir = Path(logs_dir)
        self.logger = logger
        self.status_value = status_value

        self.required_columns = {
            "status",
            "total_amount",
        }

    def _log_error(self, message):
        if self.logger is not None:
            self.logger.error(message)

    def read_file(self, file_path):
        file_path = Path(file_path)
        return pd.read_csv(file_path)

    def validate_columns(self, data):
        missing_columns = self.required_columns - set(data.columns)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"отсутствуют обязательные колонки: {missing}"
            )

    def filter_delivered(self, data):
        return data[
            data["status"] == self.status_value
        ].copy()

    def calculate_metrics(self, data):
        delivered_data = self.filter_delivered(data)

        amounts = pd.to_numeric(
            delivered_data["total_amount"],
            errors="coerce",
        ).dropna()

        return {
            "total_sum": amounts.sum(),
            "average_check": amounts.mean(),
            "order_count": len(amounts),
        }

    def analyze_file(self, file_path):
        file_path = Path(file_path)

        try:
            data = self.read_file(file_path)
            self.validate_columns(data)

            metrics = self.calculate_metrics(data)

            return {
                "file_name": file_path.name,
                "total_sum": metrics["total_sum"],
                "average_check": metrics["average_check"],
                "order_count": metrics["order_count"],
            }

        except Exception as error:
            message = (
                f"Ошибка обработки файла "
                f"{file_path.name}: {error}"
            )
            self._log_error(message)
            raise

    def analyze_all_files(self):
        results = []
        errors = []

        self.data_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.reports_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        for file_path in sorted(
            self.data_dir.glob("*.csv")
        ):
            try:
                result = self.analyze_file(file_path)
                results.append(result)

            except Exception as error:
                errors.append(
                    {
                        "file_name": file_path.name,
                        "error": str(error),
                    }
                )

        return results, errors