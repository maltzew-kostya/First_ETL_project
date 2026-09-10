# Вспомним метод Counter
from collections import Counter

lst = list("мама мыла раму")
res_dct = Counter(lst)
print(res_dct.most_common(3))
