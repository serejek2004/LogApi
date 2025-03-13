import os
import tempfile
import zipfile
import tarfile
import rarfile
import re
from datetime import datetime
from app.log.dao import LogDAO


def extract_archive(filepath, extract_to):
    if zipfile.is_zipfile(filepath):
        with zipfile.ZipFile(filepath, "r") as archive:
            archive.extractall(extract_to)
    elif rarfile.is_rarfile(filepath):
        with rarfile.RarFile(filepath, "r") as archive:
            archive.extractall(extract_to)
    elif tarfile.is_tarfile(filepath):
        with tarfile.open(filepath, "r") as archive:
            archive.extractall(extract_to)
    else:
        raise ValueError("Unsupported archive format")


def read_logs_from_dir(directory):
    logs = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".txt") and not file_name.startswith("._"):
                with open(os.path.join(root, file_name), "r", encoding="utf-8") as f:
                    logs.extend(f.readlines())
    return logs


class LogService:
    LOG_PATTERN = re.compile(r'\[(.*?)\]\s(\w+):\s(.+)')

    def __init__(self, db):
        self.dao = LogDAO(db)

    def process_file(self, file):
        filename = file.filename.lower()

        if filename.endswith(".txt"):
            return self._process_text_file(file)
        elif filename.endswith((".zip", ".rar", ".tar")):
            return self._process_archive(file)
        return {"error": "Unsupported file format"}, 400

    def _process_text_file(self, file):
        try:
            logs = file.read().decode("utf-8").splitlines()
            parsed_logs = [self._parse_log_line(log) for log in logs if log.strip()]
            self._save_logs(parsed_logs)
            return {"message": "Logs saved successfully from text file."}, 201
        except Exception as e:
            return {"error": f"Failed to process text file: {e}"}, 500

    def _process_archive(self, file):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                filepath = os.path.join(temp_dir, file.filename)
                file.save(filepath)

                extract_archive(filepath, temp_dir)

                logs = read_logs_from_dir(temp_dir)
                parsed_logs = [self._parse_log_line(log) for log in logs if log.strip()]
                self._save_logs(parsed_logs)

                return {"message": "Logs from archive saved successfully."}, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Failed to process archive: {e}"}, 500

    def _parse_log_line(self, log_line: str):
        match = self.LOG_PATTERN.match(log_line)
        if match:
            timestamp_str, log_level, log_data = match.groups()
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp = datetime.utcnow()
            return {"created_at": timestamp, "log_level": log_level, "log_data": log_data}
        return None

    def _save_logs(self, logs: list):
        for log in logs:
            if log:
                self.dao.save_log(
                    created_at=log["created_at"],
                    log_level=log["log_level"],
                    log_data=log["log_data"]
                )

    def get_all(self):
        logs = self.dao.get_all_logs()
        return [log.to_dict() for log in logs]

    def get_logs_by_time(self, start_time: datetime, end_time: datetime):
        logs = self.dao.get_logs_by_time(start_time, end_time)
        return [log.to_dict() for log in logs]

    def get_logs_by_fragment(self, fragment: str):
        logs = self.dao.get_logs_by_fragment(fragment)
        return [log.to_dict() for log in logs]

    def get_logs_by_fragment_and_by_time(self, fragment: str, start_time: datetime, end_time: datetime):
        logs = self.dao.get_logs_by_fragment_and_by_time(fragment, start_time, end_time)
        return [log.to_dict() for log in logs]
