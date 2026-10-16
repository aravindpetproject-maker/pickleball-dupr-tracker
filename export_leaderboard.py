import pandas as pd

from services.file_service import (
    load_json
)

players = load_json(
    "players.json"
)

df = pd.DataFrame(players)

df = df.sort_values(
    by="currentDupr",
    ascending=False
)

output_file = (
    "exports/leaderboard.xlsx"
)

df.to_excel(
    output_file,
    index=False
)

print(
    f"Exported: {output_file}"
)