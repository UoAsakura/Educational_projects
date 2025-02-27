

import numpy as np
data = [1, 2, 3, 4, 5, 6, 1000]  # Пример данных с выбросом
median = np.median(data)
percentile_45 = np.percentile(data, 45)
print(f"Медиана: {median}, 45-й перцентиль: {percentile_45}")