"""로깅 설정 모듈"""
import logging
import logging.handlers
import json
from pathlib import Path
from typing import Dict, Any
from config import Config


class JSONFormatter(logging.Formatter):
    """JSON 포맷 로거"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # extra 필드 추가
        excluded_keys = {
            "name", "msg", "args", "created", "filename",
            "funcName", "levelname", "levelno", "lineno",
            "module", "msecs", "pathname", "process",
            "processName", "relativeCreated", "thread",
            "threadName", "exc_info", "exc_text", "stack_info"
        }

        for key, value in record.__dict__.items():
            if key not in excluded_keys:
                log_data[key] = value

        # 예외 정보 추가
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """콘솔 출력용 포맷터 (사람이 읽기 쉬운 형식)"""

    def format(self, record: logging.LogRecord) -> str:
        # 기본 메시지 포맷
        base_msg = super().format(record)

        # extra 필드 수집
        excluded_keys = {
            "name", "msg", "args", "created", "filename",
            "funcName", "levelname", "levelno", "lineno",
            "module", "msecs", "pathname", "process",
            "processName", "relativeCreated", "thread",
            "threadName", "exc_info", "exc_text", "stack_info",
            "message", "asctime"
        }

        extra_fields = []
        for key, value in record.__dict__.items():
            if key not in excluded_keys:
                extra_fields.append(f"{key}={value}")

        # extra 필드가 있으면 추가
        if extra_fields:
            base_msg += " | " + ", ".join(extra_fields)

        return base_msg


def setup_logging(config: Config) -> None:
    """로깅 시스템을 초기화합니다.

    Args:
        config: Config 인스턴스
    """
    # 루트 로거 설정
    logger = logging.getLogger("transbot")
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    logger.handlers.clear()  # 기존 핸들러 제거

    # 콘솔용 포맷터 (항상 사람이 읽기 쉬운 포맷)
    console_formatter = ConsoleFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 파일용 포맷터 (JSON 또는 일반 포맷)
    if config.LOG_FORMAT == "json":
        file_formatter = JSONFormatter()
    else:
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # 콘솔 핸들러
    if config.LOG_CONSOLE_OUTPUT:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # 파일 핸들러 (로테이션)
    if config.LOG_FILE_PATH:
        log_dir = Path(config.LOG_FILE_PATH).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE_PATH,
            maxBytes=config.LOG_FILE_MAX_BYTES,
            backupCount=config.LOG_FILE_BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.info("로깅 시스템 초기화 완료", extra={
        "log_level": config.LOG_LEVEL,
        "log_format": config.LOG_FORMAT,
        "console_output": config.LOG_CONSOLE_OUTPUT,
        "file_output": bool(config.LOG_FILE_PATH)
    })


def get_logger(name: str) -> logging.Logger:
    """로거 인스턴스를 반환합니다.

    Args:
        name: 로거 이름 (예: "transbot.api")

    Returns:
        Logger 인스턴스
    """
    return logging.getLogger(name)


def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """민감정보를 마스킹합니다.

    Args:
        data: 로깅할 데이터 딕셔너리

    Returns:
        마스킹된 데이터 딕셔너리
    """
    masked = data.copy()

    # API 키 마스킹
    if "api_key" in masked and masked["api_key"]:
        key = masked["api_key"]
        if len(key) >= 10:
            masked["api_key"] = f"{key[:3]}***...***{key[-3:]}"
        else:
            masked["api_key"] = "***"

    # Endpoint 마스킹
    if "endpoint" in masked and masked["endpoint"] and "azure" in masked["endpoint"]:
        endpoint = masked["endpoint"]
        # https://my-resource.openai.azure.com/ → https://*****. openai.azure.com/
        parts = endpoint.split(".")
        if len(parts) >= 2:
            resource_part = parts[0].split("//")[-1]
            masked["endpoint"] = endpoint.replace(resource_part, "*****")

    return masked
