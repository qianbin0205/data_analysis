import pandas as pd
import numpy as np

dict_obj = {'key1': ['a', 'b', 'a', 'b',
                     'a', 'b', 'a', 'a'],
            'key2': ['one', 'one', 'two', 'three',
                     'two', 'two', 'one', 'three'],
            'data1': np.random.randint(1, 10, 8),
            'date2': np.random.randint(1, 10, 8)
            }

df_obj = pd.DataFrame(dict_obj)
print(df_obj)
# transform里面写聚合函数、add_prefix为列标添加前缀
k1_sun_tf = df_obj.groupby('key1').transform(np.min).add_prefix('min_')
print(k1_sun_tf)