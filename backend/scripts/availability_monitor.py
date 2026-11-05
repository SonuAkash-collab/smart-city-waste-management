"""TC-AVL-01: check /health once a minute and report uptime (SCW-NF-003).

    python scripts/availability_monitor.py --url http://localhost:8000 --hours 24

Writes every check to availability-log.csv and prints the uptime percentage at the end
(or when stopped with Ctrl+C). 99% of 1,440 checks means at least 1,426 successes.
"""

import argparse
import csv
import time
from datetime import datetime, timezone

import httpx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--hours", type=float, default=24)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--log", default="availability-log.csv")
    args = parser.parse_args()

    planned = int(args.hours * 3600 / args.interval)
    ok = done = 0
    with open(args.log, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["time_utc", "result", "detail"])
        try:
            for _ in range(planned):
                started = time.monotonic()
                try:
                    response = httpx.get(f"{args.url}/health", timeout=10)
                    good = response.status_code == 200 and response.json().get("status") == "ok"
                    detail = str(response.status_code)
                except (httpx.HTTPError, ValueError) as exc:
                    good, detail = False, type(exc).__name__
                ok += good
                done += 1
                writer.writerow([datetime.now(timezone.utc).isoformat(), "OK" if good else "FAIL", detail])
                handle.flush()
                time.sleep(max(0.0, args.interval - (time.monotonic() - started)))
        except KeyboardInterrupt:
            pass
    uptime = 100 * ok / planned if planned else 0
    print(f"Checks planned {planned}, run {done}, successful {ok}. Uptime {uptime:.2f}% (target 99%).")


if __name__ == "__main__":
    main()
