import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def 読み込む(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def 日付で絞る(schedules, date):
    return sorted(
        [item for item in schedules if item["start"][:10] == date],
        key=lambda item: item["start"]
    )


def 文字列にする(item):
    start = datetime.fromisoformat(item["start"])
    end = datetime.fromisoformat(item["end"])

    location = item.get("location") or "（場所なし）"

    return (
        f"{start:%H:%M}-{end:%H:%M} "
        f"{item['title']} @{location}"
    )


def main():
    path = Path(__file__).with_name("schedule.json")

    if not path.exists():
        print("schedule.json がありません。同じフォルダに schedule.json を置いてください。")
        return

    if len(sys.argv) >= 2:
        date = sys.argv[1]
    else:
        date = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")

    schedules = 読み込む(path)
    today_schedules = 日付で絞る(schedules, date)

    print(f"{date} の予定 {len(today_schedules)} 件")

    for item in today_schedules:
        print(文字列にする(item))


if __name__ == "__main__":
    main()