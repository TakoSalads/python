import json
from collections import Counter

#update to raspberry's log folder
with open('logs/recentlylistened.json', 'r') as f:
    amount_listened = Counter(json.load(f))

top_tracks = amount_listened.most_common(10)

for track, count in top_tracks:
    print(f"{track} - {count} plays")