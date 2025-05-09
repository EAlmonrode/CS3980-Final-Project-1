from datetime import datetime
import logging

today_str = datetime.today().strftime('%Y-%m-%d')

logging.basicConfig(
    filename=f"logs/{today_str}.log",
    format="%(asctime)s: %(name)s: %(levelname).4s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
