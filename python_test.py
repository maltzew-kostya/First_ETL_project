# Вспомним метод Counter
from collections import Counter

lst = [1, 2, 3, 1, 2, 3, 1, 1, 1, 2, 5, 6, 7]

results = Counter(lst)

print(results.most_common(1))
