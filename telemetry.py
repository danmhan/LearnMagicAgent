import logging
import json
import re
from typing import Any, Dict

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Initialize OpenTelemetry
provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("learn_magic_agent.tracer")

class PIIRedactingJSONFormatter(logging.Formatter):
    """
    A custom JSON formatter that structures log data and redacts basic PII
    (like emails and phone numbers) from the log messages.
    """
    
    # Simple regex for emails
    EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
    
    def format(self, record: logging.LogRecord) -> str:
        # Create structured log dict
        log_record: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        
        # Redact PII from the message
        if log_record["message"]:
            log_record["message"] = self.EMAIL_REGEX.sub("[REDACTED EMAIL]", log_record["message"])
            
        # Add any extra contextual data
        if hasattr(record, "extra_data"):
            log_record["extra_data"] = record.extra_data # type: ignore
            
        return json.dumps(log_record)

def setup_telemetry() -> logging.Logger:
    """Sets up structured JSON logging."""
    logger = logging.getLogger("LearnMagicAgent")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = PIIRedactingJSONFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# Create a singleton logger
logger = setup_telemetry()
