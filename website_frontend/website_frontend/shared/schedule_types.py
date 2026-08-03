from typing import Literal, TypeAlias

WeekdayKey: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6"]
LiveSchedule: TypeAlias = dict[WeekdayKey, str]
