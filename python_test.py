# Вспомним метод Counter
from collections import Counter, defaultdict

lst = [1, 2, 3, 1, 2, 3, 1, 1, 1, 2, 5, 6, 7]

results = Counter(lst)

print(results.most_common(1))

# Дополнительно вспомним метод defaultdict

arr = [
    {"name": "Petr", "subject": "Python", "score": 97},
    {"name": "Max", "subject": "C++", "score": 70},
    {"name": "Petr", "subject": "C++", "score": 45},
    {"name": "Max", "subject": "Python", "score": 60},
    {"name": "Petr", "subject": "SQL", "score": 65},
    {"name": "Max", "subject": "SQL", "score": 100},
]

res_dct = defaultdict(lambda: {"sum": 0, "count": 0})

for row in arr:
    subject = row["subject"]
    score = row["score"]
    res_dct[subject]["sum"] += score
    res_dct[subject]["count"] += 1

for sub, data in res_dct.items():
    print(f"{sub}: {data['sum'] / data['count']}")
