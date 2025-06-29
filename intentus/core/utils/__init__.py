import logging
import colorlog


def setup_logging():
    """Set up colored logging for the entire application."""
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "green",
                "INFO": "blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )

    # Get the root logger and set its level
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)


def make_json_serializable(obj):
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, dict):
        return {
            make_json_serializable(key): make_json_serializable(value)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [make_json_serializable(element) for element in obj]
    elif hasattr(obj, "__dict__"):
        return make_json_serializable(obj.__dict__)
    else:
        return str(obj)


def make_json_serializable_truncated(obj, max_length: int = 100000):
    if isinstance(obj, (int, float, bool, type(None))):
        if isinstance(obj, (int, float)) and len(str(obj)) > max_length:
            return str(obj)[: max_length - 3] + "..."
        return obj
    elif isinstance(obj, str):
        return obj if len(obj) <= max_length else obj[: max_length - 3] + "..."
    elif isinstance(obj, dict):
        return {
            make_json_serializable_truncated(
                key, max_length
            ): make_json_serializable_truncated(value, max_length)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [
            make_json_serializable_truncated(element, max_length) for element in obj
        ]
    elif hasattr(obj, "__dict__"):
        return make_json_serializable_truncated(obj.__dict__, max_length)
    else:
        result = str(obj)
        return result if len(result) <= max_length else result[: max_length - 3] + "..."
