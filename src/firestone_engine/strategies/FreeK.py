import logging
from bisect import bisect_right
from datetime import datetime, timedelta
from decimal import Decimal
from firestone_engine.Utils import Utils
from .Base import Base


class FreeK(Base):
    """
    Match rules:
      1) k_shape: open/low/high/close each within configured [min, max] ranges
      2) speed:
           - in `time_price` seconds: ((price - pre_price) / pre_price) * 100 >= percent
           - in `time_volume` seconds: (volume - pre_volume) >= volume_threshold
      3) voulme_now: current total volume >= configured threshold
    """

    _logger = logging.getLogger(__name__)

    def matchCondition(self):
        if not self.match_k_shape():
            return False
        if not self.match_speed():
            return False
        if not self.match_volume_now():
            return False
        FreeK._logger.info("TradeId=%s Code=%s FreeK matched k_shape+speed+voulme_now", self.trade.get("_id"), self.dataLastRow.get("code"))
        return True

    def match_k_shape(self):
        params = self.trade["params"]
        if "k_shape" not in params:
            return False

        k_shape = params["k_shape"]
        # Current k-line data: "open", "low", "high", "price" (price == close)
        open_p = Decimal(str(self.dataLastRow["open"]))
        low_p = Decimal(str(self.dataLastRow["low"]))
        high_p = Decimal(str(self.dataLastRow["high"]))
        close_p = Decimal(str(self.dataLastRow["price"]))

        def in_range(key, value):
            if key not in k_shape:
                return False
            if "min" not in k_shape[key] or "max" not in k_shape[key]:
                return False
            min_v = Decimal(str(k_shape[key]["min"]))
            max_v = Decimal(str(k_shape[key]["max"]))
            return value >= min_v and value <= max_v

        return (
            in_range("open", open_p)
            and in_range("low", low_p)
            and in_range("high", high_p)
            and in_range("close", close_p)
        )

    def _parse_row_datetime(self, row):
        row_date = row.get("date")
        row_time = row.get("time")

        if not isinstance(row_date, str):
            row_date = row_date.strftime("%Y-%m-%d")

        # time is usually like "09:25:03", but defensively strip fractional/Z.
        if isinstance(row_time, str):
            row_time = row_time.split(".")[0]
            row_time = row_time.replace("Z", "")

        return datetime.strptime("{} {}".format(row_date, row_time), "%Y-%m-%d %H:%M:%S")

    def _ensure_datetime_cache(self):
        # Base.run is called repeatedly and `self.data` may grow over time.
        # Cache parsed datetimes for binary search.
        if not hasattr(self, "_dt_cache") or len(self._dt_cache) != len(self.data):
            self._dt_cache = [self._parse_row_datetime(r) for r in self.data]

    def _get_pre_row_seconds_ago(self, seconds):
        seconds = float(seconds)
        self._ensure_datetime_cache()
        now_dt = self._dt_cache[-1]
        target_dt = now_dt - timedelta(seconds=seconds)

        # Find the latest row with dt <= target_dt.
        idx = bisect_right(self._dt_cache, target_dt) - 1
        if idx < 0:
            return None
        return self.data[idx]

    def match_speed(self):
        params = self.trade["params"]
        if "speed" not in params:
            return False
        speed = params["speed"]

        # Price speed
        if "time_price" not in speed or "percent" not in speed:
            return False

        time_price = float(speed["time_price"])
        percent_threshold = Decimal(str(speed["percent"]))
        pre_price_row = self._get_pre_row_seconds_ago(time_price)
        if pre_price_row is None:
            return False

        pre_price = Decimal(str(pre_price_row["price"]))
        if pre_price == 0:
            return False

        price = Decimal(str(self.dataLastRow["price"]))
        percent = Utils.round_dec((price - pre_price) / pre_price * Decimal("100"))
        if percent < percent_threshold:
            return False

        # Volume speed (increase over window)
        if "time_volume" not in speed or "volume" not in speed:
            return False

        time_volume = float(speed["time_volume"])
        volume_threshold = Decimal(str(speed["volume"]))
        pre_volume_row = self._get_pre_row_seconds_ago(time_volume)
        if pre_volume_row is None:
            return False

        pre_volume = Decimal(str(pre_volume_row["volume"]))
        current_volume = Decimal(str(self.dataLastRow["volume"]))
        volume_increase = current_volume - pre_volume
        return volume_increase >= volume_threshold

    def match_volume_now(self):
        params = self.trade["params"]
        # Keep your original misspelling, but also accept a corrected key.
        volume_key = "voulme_now" if "voulme_now" in params else "volume_now"
        if volume_key not in params:
            return False

        volume_now_threshold = Decimal(str(params[volume_key]))
        current_volume = Decimal(str(self.dataLastRow["volume"]))
        return current_volume >= volume_now_threshold