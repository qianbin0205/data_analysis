# 关键字
# 蓄电池
# 特征工程
# 随机森林
#
# 项目背景
# 毫无疑问，蓄电池是一辆汽车不可缺少的一部分，它是一种将化学能转变成电能的装置，属于直流电源，其作用有：
#
# 启动发动机时，给起动机提供强大的起动电流（10
# A左右）
# 当发电机过载时，可以协助发电机向用电设备供电
# 当发动机处于怠速时，向用电设备供电
# 蓄电池还是一个大容量电容器，可以保护汽车的用电器
# 当发电机端电压高于铅蓄电池的电动势时，将一部分电能转变为化学能储存起来，也就是进行充电
# 该项目主要针对汽油车内的铅蓄电池故障，基于TBOX采集的原始数据建立机器学习模型以期挖掘故障特征或模式提前做出预警。
# 实际场景中也很有意义，如果车子因蓄电池故障在半路抛锚估计只能叫拖车了，提前预警的话不仅一定程度上提升驾驶者的安全性，也利于车主安排维修计划，这对距离维修点较远的用户来说意义更大。
# 数据及问题描述
# 笔者当时就职于某汽车集团，所能拿到的数据是云平台积累的TBox秒级数据（TB级），总变量超过100多个，包括启停时间、发动机转速、车内外温度、车速、里程等，与蓄电池直接相关的变量只有蓄电池电压；另外还有对应车辆的蓄电池历史维修记录。业务给出的理想要求是能在蓄电池发生故障前一个月内给出预警，后来改为剩余可行驶里程为100公里时给出预警，这样更为合理。
#
# 解决方案
# 该项目初看起来并非典型的预测或分类问题。为了转化为我们熟悉的机器学习可解对象，首先需对数据进行标注，然后进行聚合操作，再进行特征工程，最后再选择合适的算法进行模型训练。
#
# 数据标注
# 上述原始数据是不带标签的，需要根据维修记录人为打标。具体问题需具体分析，这里经过和业务、设计、维保相关人员的交流，发现蓄电池故障绝大部分的情况具有渐进性，是非突发式的（除非是不可控的物理损坏）。这就为模式识别方式解决该问题提供了可能。也可据此推论，与正常数据相比在时间上接近蓄电池发生故障的数据是带有某种故障模式或表征的。
# 因此，将维修时间点往前15天且发动机转速非零的数据标记为1（故障负样本），将未发生蓄电池故障的同区域同时间区间的数据标记为0（正常样本）。
#
# 聚合与特征工程
# 该部分主要对秒级数据进行按天聚合（也可按更小的时间粒度），同时构造特征字段，包括各字段的统计量（均值、方差、峰度、偏度等）、驾驶行为归因表征、现象表征。其中驾驶行为归因表征是指可能导致蓄电池发生故障的驾驶行为变量，比如转速低于2000转的时长占比（转速2000转以下蓄电池不充电）；现象表征是指即将发生蓄电池故障的车辆某些变量的异常情况，比如蓄电池电压低于标准电压时长等。
# 最终构造了42个变量。每天一条数据（未行驶的时间除外）。
#
# 算法建模
# 基于上述的特征工程，这里选择了随机森林作为初段建模算法。
#
# 关键过程
# 数据抽取
# 正常情况下应该是直接从数据库读取数据，但是出于“某种原因”，当时只能拿到离线数据，从csv文件进行处理，平均每个csv大小约5g，为按时间区间存储的若干辆汽车的秒级TBox数据，因此需要对这些数据重新按照车辆vin号进行抽取再计算特征进行聚合。由于数据量较大，为便于后期调试特征聚合及算法，这里对抽取后的中间数据进行缓存并采用多进程处理，核心代码如下：
#
# 缓存装饰器
import hashlib
import pickle
import os
from tqdm import tqdm
import pandas as pd
from mix_class import Construction_data
import numpy as np
from multiprocessing import Pool

# 缓存装饰器
cache_root_dir = 'cache_vin_copy'
if not os.path.exists(cache_root_dir):
    os.makedirs(cache_root_dir)


def md5(s):
    m = hashlib.md5()
    m.update(s.encode("utf8"))
    return m.hexdigest()


def cache_key(f, *args, **kwargs):
    s = '%s-%s-%s' % (f.__name__, str(args), str(kwargs))
    return os.path.join(cache_root_dir, '%s.dump' % md5(s))


def cache(f):
    def wrap(*args, **kwargs):
        fn = cache_key(f, *args, **kwargs)
        if os.path.exists(fn):
            print('loading cache')
            with open(fn, 'rb') as fr:
                return pickle.load(fr)

        obj = f(*args, **kwargs)
        with open(fn, 'wb') as fw:
            pickle.dump(obj, fw, protocol=4)
        return obj

    return wrap


# 多进程 + 缓存中间结果


def vin_combin(k, pathss):
    s1 = time.time()
    with open(pathss, 'rb') as fr:
        temp_vin = pickle.load(fr)
    temp_vin = temp_vin.drop_duplicates()
    temp_vin.loc[:, 'starttime'] = pd.to_datetime(temp_vin.loc[:, 'starttime'])
    temp_vin.index = temp_vin.starttime
    temp_vin = temp_vin.sort_index()
    mix = Construction_data(temp_vin, time='D')
    mixx = mix.concat_data();
    mixx['vin'] = k
    mix['label'] = 0
    efors = time.time()
    print("for one vin cost time ：", int(efors - s1) / 3600)
    return [mixx]


@cache
def mix_pool(path, times):
    print(times);
    path = dict(path)
    nor_list = []
    pool = Pool(15);
    pool_list = []
    for k, v in tqdm(path.items()):
        results = pool.apply_async(vin_combin, (k, v))
        pool_list.append(results)
    print(len(pool_list))
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出
    for result in pool_list:
        try:
            nor_df = result.get()
            nor_list.append(nor_df[0])
        except:
            pass
    return nor_list


# 特征工程
# 根据上述特征构造思路，基于pandas强大的数据处理能力实现了一个数据聚合与特征生成的类，输入df输出聚合后的特征。核心代码如下：

class Construction_data():
    '''
    the class of converge of data, default time is day!
    two args need give : df and time
    for df need have common vin at serial time.
    time can give : 'M'/'D'/'H'
    return 42 columns data in every VIN

    '''

    def __init__(self, df, time='D'):
        self.n_power_time = 'n_power_time'
        self.run_time_2k = 'run_time_2k'
        self.num_non_p = 'num_non_p'
        self.battery_start = 'battery_start'
        self.battery_avg = 'battery_avg'
        self.battery_var = 'battery_var'
        self.battery_max = 'battery_max'
        self.battery_mix4 = 'battery_mix4'
        self.battery_mix1 = 'battery_mix1'
        self.battery_min = 'battery_min'
        self.kurt_v_battery = 'kurt_v_battery'
        self.skew_v_battery = 'skew_v_battery'
        self.avg_temperature_in = 'avg_temperature_in'
        self.avg_temperature_out = 'avg_temperature_out'
        self.starting_num_day = 'starting_num_day'
        self.minutes15_st = '15_minutes_st'
        self.remote_boot_times = 'remote_boot_times'
        self.x_acc = 'x_acc'
        self.y_acc = 'y_acc'
        self.z_acc = 'z_acc'
        #        self.accepos_var = 'accepos_var'
        self.brakepos_var = 'brakepos_var'
        self.dr_avg_v = 'dr_avg_v'
        self.dr_avg_mile = 'dr_avg_mile'
        #        self.day_fuel = 'day_fuel'
        self.dr_mile50 = 'dr_mile50'
        self.dr_v0_rate = 'dr_v0_rate'
        self.avg_run_mile = 'avg_run_mile'
        self.avg_run_times = 'avg_run_times'
        self.ac_on_count = 'ac_on_count'
        self.ac_auto_on_count = 'ac_auto_on_count'
        self.fanspeed_avg = 'fanspeed_avg'
        self.fanspeed_var = 'fanspeed_var'
        self.d_temp_avg = 'd_temp_avg'
        self.c_temp_avg = 'c_temp_avg'
        self.side_light_count = 'side_light_count'
        self.dip_light_count = 'dip_light_count'
        self.main_light_count = 'main_light_count'
        self.wiperswitch_avg = 'wiperswitch_avg'
        self.oli_box_avg = 'oli_box_avg'
        self.cool_avg = 'cool_avg'
        self.batt_1 = 'batt_1'
        self.batt_0 = 'batt_0'
        self.mils = 'mils'

        self.df = df
        self.time = time

        self.df.starttime = pd.to_datetime(self.df.starttime)
        self.df.index = self.df.starttime
        self.df = self.df.sort_index()

        self.day_index = self.df.to_period(self.time)
        self.day_group = self.day_index.groupby(self.day_index.index)

    def n_p_time(self, g_df):
        vehsyspwrmod_list = list(g_df.loc[:, 'vehsyspwrmod'])
        values_counts = Counter(vehsyspwrmod_list)
        return (values_counts[0] + values_counts[1]) / len(vehsyspwrmod_list)

    def run_t_2k(self, g_df):
        vehrpm_2k = len(list(g_df[g_df.vehrpm < 2000].loc[:, 'vehrpm']))
        return vehrpm_2k / len(list(g_df.loc[:, 'vehrpm']))

    def num_n_p(self, g_df):
        ttx = np.array(g_df.starttime)
        c = list(np.diff(ttx) / np.timedelta64(1, 's'))
        c.insert(0, 1);
        g_df.loc[:, 'temp'] = c
        start_t = g_df[g_df.temp > 10].starttime.tolist()
        i = 0
        if len(start_t) == 0:
            return 0
        for t in start_t:
            diff = float(g_df[g_df.starttime == t].iloc[-1].vehbatt) - float(g_df[g_df.starttime < t].iloc[-1].vehbatt)
            i += diff
            pass
        return i / len(start_t)

    def batt_start(self, g_df):
        ttx = np.array(g_df.starttime)
        c = list(np.diff(ttx) / np.timedelta64(1, 's'))
        c.insert(0, 1);
        g_df.loc[:, 'temp'] = c
        start_t = g_df[g_df.temp > 10].starttime.tolist()
        i = 0
        if len(start_t) == 0:
            return 0
        for t in start_t:
            diff = float(g_df[g_df.starttime == t].iloc[-1].vehbatt)
            i += diff
            pass
        return i / len(start_t)

    def batt_avg(self, g_df):
        return g_df.vehbatt.mean()

    def batt_var(self, g_df):
        return g_df.vehbatt.std()

    def batt_max(self, g_df):
        return g_df.vehbatt.max()

    def batt_mix4(self, g_df):
        return g_df.vehbatt.quantile(0.4)

    def batt_mix1(self, g_df):
        return g_df.vehbatt.quantile(0.1)

    def batt_min(self, g_df):
        return g_df.vehbatt.min()

    def kurt_v_batterys(self, g_df):
        return g_df.vehbatt.kurt()

    def skew_v_batterys(self, g_df):
        return g_df.vehbatt.skew()

    def avg_temp_in(self, g_df):
        return g_df.vehinsidetemp.mean()

    def avg_temp_out(self, g_df):
        return g_df.vehoutsidetemp.mean()

    def start_num_day(self, g_df):
        ttx = np.array(g_df.starttime)
        c = list(np.diff(ttx) / np.timedelta64(1, 's'))
        c.insert(0, 1);
        g_df.loc[:, 'temp'] = c
        return len(g_df[g_df.temp > 10].starttime.tolist())

    def min15_st(self, g_df):
        ttx = np.array(g_df.starttime)
        c = list(np.diff(ttx) / np.timedelta64(1, 's'))
        c.insert(0, 1);
        g_df.loc[:, 'temp'] = c
        start_t = g_df[g_df.temp > 10].starttime.tolist()
        i = 0
        ax = pd.DataFrame(start_t, columns=['t'])
        tc = [x.total_seconds() / 60 for x in ax.diff().dropna().t]
        for t in tc:
            if t < 10:
                i += 1
        return i

    def remote_times(self, g_df):
        return g_df.vehbatt.median()

    def x_ac(self, g_df):
        return g_df.tboxaccelx.std()

    def y_ac(self, g_df):
        return g_df.tboxaccely.std()

    def z_ac(self, g_df):
        return g_df.tboxaccelz.std()

    #    def acc_var(self,g_df):
    #        pass########################################
    #
    def brak_var(self, g_df):
        return g_df.vehbrakepos.std()

    def d_avg_v(self, g_df):
        g_1 = g_df[g_df.vehspeed > 0]
        return g_1.vehspeed.mean()

    def d_avg_mile(self, g_df):
        return g_df.vehodo.iloc[-1] - g_df.vehodo.iloc[0]

    #    def days_fuel(self,g_df):
    #        pass########################################

    def dr_miles50(self, g_df):
        g_1 = g_df[g_df.vehspeed > 0]
        return g_1[g_1.vehspeed < 50].shape[0] / 3600

    def dr_v0_rates(self, g_df):
        g_1 = g_df[g_df.vehspeed > 0]
        if g_1.shape[0] == 0:
            return 0
        return g_1[g_1.vehspeed < 50].shape[0] / g_1.shape[0]

    #    def avg_run_mile(self,g_df):
    #        pass########################################

    def avg_run_time(self, g_df):
        return g_df[g_df.vehsyspwrmod > 0].shape[0] / 3600

    def ac_on_counts(self, g_df):
        return g_df[g_df.vehac > 0].shape[0] / g_df.shape[0]

    def ac_auto_on_counts(self, g_df):
        return g_df[g_df.vehacauto > 0].shape[0] / g_df.shape[0]

    def fanspeed_avgs(self, g_df):
        return g_df.vehacfanspeed.mean()

    def fanspeed_vars(self, g_df):
        return g_df.vehacfanspeed.std()

    def d_temp_avgs(self, g_df):
        g_p = g_df[g_df.vehacdrvtargettemp > 0]
        return g_p.vehacdrvtargettemp.mean()

    def c_temp_avgs(self, g_df):
        g_p = g_df[g_df.vehacpasstargettemp > 0]
        return g_p.vehacpasstargettemp.mean()

    def side_light_counts(self, g_df):
        gs = g_df[g_df.vehsidelight > 0]
        return gs.shape[0] / g_df.shape[0]

    def dip_light_counts(self, g_df):
        return g_df[g_df.vehdiplight > 0].shape[0] / g_df.shape[0]

    def main_light_counts(self, g_df):
        return g_df[g_df.vehmainlight > 0].shape[0] / g_df.shape[0]

    def wiperswitch_avgs(self, g_df):
        gs = g_df[g_df.vehwiperswitchfront > 0]
        return gs.shape[0] / g_df.shape[0]

    def oli_box_avgs(self, g_df):
        return g_df.vehfuellev.mean()

    def cool_avgs(self, g_df):
        return g_df.vehcoolanttemp.mean()

    def milss(self, g_df):
        return g_df.vehodo[-1]

    def batt_1s(self, g_df):
        return g_df.vehbatt[-1]

    def batt_0s(self, g_df):
        return g_df.vehbatt[0]

    def concat_data(self):
        n_power_time = self.day_group.apply(self.n_p_time).to_frame(name=self.n_power_time)
        run_time_2k = self.day_group.apply(self.run_t_2k).to_frame(name=self.run_time_2k)
        num_non_p = self.day_group.apply(self.num_n_p).to_frame(name=self.num_non_p)
        battery_start = self.day_group.apply(self.batt_start).to_frame(name=self.battery_start)
        battery_avg = self.day_group.apply(self.batt_avg).to_frame(name=self.battery_avg)
        battery_var = self.day_group.apply(self.batt_var).to_frame(name=self.battery_var)
        battery_max = self.day_group.apply(self.batt_max).to_frame(name=self.battery_max)
        battery_mix4 = self.day_group.apply(self.batt_mix4).to_frame(name=self.battery_mix4)
        battery_mix1 = self.day_group.apply(self.batt_mix1).to_frame(name=self.battery_mix1)
        battery_min = self.day_group.apply(self.batt_min).to_frame(name=self.battery_min)
        kurt_v_battery = self.day_group.apply(self.kurt_v_batterys).to_frame(name=self.kurt_v_battery)
        skew_v_battery = self.day_group.apply(self.skew_v_batterys).to_frame(name=self.skew_v_battery)
        avg_temperature_in = self.day_group.apply(self.avg_temp_in).to_frame(name=self.avg_temperature_in)
        avg_temperature_out = self.day_group.apply(self.avg_temp_out).to_frame(name=self.avg_temperature_out)
        starting_num_day = self.day_group.apply(self.start_num_day).to_frame(name=self.starting_num_day)
        minutes15_st = self.day_group.apply(self.min15_st).to_frame(name=self.minutes15_st)
        remote_boot_times = self.day_group.apply(self.remote_times).to_frame(name=self.remote_boot_times)
        x_acc = self.day_group.apply(self.x_ac).to_frame(name=self.x_acc)
        y_acc = self.day_group.apply(self.y_ac).to_frame(name=self.y_acc)
        z_acc = self.day_group.apply(self.z_ac).to_frame(name=self.z_acc)
        #        accepos_var =  self.day_group.apply(self.acc_var).to_frame(name=self.accepos_var)
        brakepos_var = self.day_group.apply(self.brak_var).to_frame(name=self.brakepos_var)
        dr_avg_v = self.day_group.apply(self.d_avg_v).to_frame(name=self.dr_avg_v)
        dr_avg_mile = self.day_group.apply(self.d_avg_mile).to_frame(name=self.dr_avg_mile)
        #        day_fuel =  self.day_group.apply(self.days_fuel).to_frame(name=self.day_fuel)
        dr_mile50 = self.day_group.apply(self.dr_miles50).to_frame(name=self.dr_mile50)
        dr_v0_rate = self.day_group.apply(self.dr_v0_rates).to_frame(name=self.dr_v0_rate)
        #        avg_run_mile =  self.day_group.apply(self.avg_run_miles).to_frame(name=self.avg_run_mile)
        avg_run_times = self.day_group.apply(self.avg_run_time).to_frame(name=self.avg_run_times)
        ac_on_count = self.day_group.apply(self.ac_on_counts).to_frame(name=self.ac_on_count)
        ac_auto_on_count = self.day_group.apply(self.ac_auto_on_counts).to_frame(name=self.ac_auto_on_count)
        fanspeed_avg = self.day_group.apply(self.fanspeed_avgs).to_frame(name=self.fanspeed_avg)
        fanspeed_var = self.day_group.apply(self.fanspeed_vars).to_frame(name=self.fanspeed_var)
        d_temp_avg = self.day_group.apply(self.d_temp_avgs).to_frame(name=self.d_temp_avg)
        c_temp_avg = self.day_group.apply(self.c_temp_avgs).to_frame(name=self.c_temp_avg)
        side_light_count = self.day_group.apply(self.side_light_counts).to_frame(name=self.side_light_count)
        dip_light_count = self.day_group.apply(self.dip_light_counts).to_frame(name=self.dip_light_count)
        main_light_count = self.day_group.apply(self.main_light_counts).to_frame(name=self.main_light_count)
        wiperswitch_avg = self.day_group.apply(self.wiperswitch_avgs).to_frame(name=self.wiperswitch_avg)
        oli_box_avg = self.day_group.apply(self.oli_box_avgs).to_frame(name=self.oli_box_avg)
        cool_avg = self.day_group.apply(self.cool_avgs).to_frame(name=self.cool_avg)
        mils = self.day_group.apply(self.milss).to_frame(name=self.mils)
        batt_1 = self.day_group.apply(self.batt_1s).to_frame(name=self.batt_1)
        batt_0 = self.day_group.apply(self.batt_0s).to_frame(name=self.batt_0)

        vin_data = pd.concat([n_power_time, run_time_2k, num_non_p, battery_start, battery_avg,
                              battery_var, battery_max, battery_mix4, battery_mix1, battery_min,
                              kurt_v_battery, skew_v_battery, avg_temperature_in, avg_temperature_out,
                              starting_num_day, minutes15_st, remote_boot_times, x_acc, y_acc, z_acc,
                              brakepos_var, dr_avg_v, dr_avg_mile, dr_mile50, dr_v0_rate,
                              avg_run_times, ac_on_count, ac_auto_on_count, fanspeed_avg, fanspeed_var,
                              d_temp_avg, c_temp_avg, side_light_count, dip_light_count, main_light_count,
                              wiperswitch_avg,
                              oli_box_avg, cool_avg, mils, batt_1, batt_0], axis=1)
        vin_data = vin_data.fillna(method='pad');
        vin_data = vin_data.fillna(method='bfill');
        vin_data = vin_data.sort_index()
        return vin_data


# 算法建模
# 这里该出初段采用随机森林的建模代码，这个结果F1值达到了0
# .85，代码如下：

import copy
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDAs
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.feature_selection import SelectFromModel
from sklearn import preprocessing
import numpy as np
from sklearn.utils import shuffle
from sklearn.preprocessing import Imputer
from sklearn.externals import joblib
import random
from sklearn.metrics import roc_curve, auc

use_cols = ['15_minutes_st', 'ac_auto_on_count', 'ac_on_count', 'avg_run_times',
            'avg_temperature_in', 'avg_temperature_out', 'batt_0', 'batt_1',
            'battery_avg', 'battery_max', 'battery_min', 'battery_mix1',
            'battery_mix4', 'battery_start', 'battery_var', 'brakepos_var',
            'c_temp_avg', 'cool_avg', 'd_temp_avg', 'dip_light_count',
            'dr_avg_mile', 'dr_avg_v', 'dr_mile50', 'dr_v0_rate', 'fanspeed_avg',
            'fanspeed_var', 'kurt_v_battery', 'main_light_count', 'mils',
            'n_power_time', 'num_non_p', 'oli_box_avg',
            'remote_boot_times', 'run_time_2k', 'side_light_count',
            'skew_v_battery', 'starting_num_day', 'wiperswitch_avg', 'x_acc',
            'y_acc', 'z_acc', 'label']

use_colsl = ['15_minutes_st', 'ac_auto_on_count', 'ac_on_count', 'avg_run_times',
             'avg_temperature_in', 'avg_temperature_out', 'batt_0', 'batt_1',
             'battery_avg', 'battery_max', 'battery_min', 'battery_mix1',
             'battery_mix4', 'battery_start', 'battery_var', 'brakepos_var',
             'c_temp_avg', 'cool_avg', 'd_temp_avg', 'dip_light_count',
             'dr_avg_mile', 'dr_avg_v', 'dr_mile50', 'dr_v0_rate', 'fanspeed_avg',
             'fanspeed_var', 'kurt_v_battery', 'main_light_count', 'mils',
             'n_power_time', 'num_non_p', 'oli_box_avg',
             'remote_boot_times', 'run_time_2k', 'side_light_count',
             'skew_v_battery', 'starting_num_day', 'wiperswitch_avg', 'x_acc',
             'y_acc', 'z_acc']


def confusion_matrix_plot_matplotlib(y_truth, y_predict, cmap=plt.cm.Blues):
    cm = confusion_matrix(y_truth, y_predict)
    plt.matshow(cm, cmap=cmap)  # 混淆矩阵图
    plt.colorbar()  # 颜色标签
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()  # 显示作图结果


def classification_report(y_true, y_pred):
    from sklearn.metrics import classification_report
    print("classification_report(left: labels):")
    print(classification_report(y_true, y_pred))


def get_xy(df):
    x = df[use_colsl]
    y = df['label']
    return x, y


def merged(wdata):
    return pd.concat(wdata)


def clean_list(ll):
    ls = []
    for item in ll:
        if item.shape[0] > 0:
            ls.append(item)
            pass
    return ls


def count_01(df):
    pre_list = list(df.loc[:, 'pre_label'])
    values_counts = Counter(pre_list)
    if df.loc[:, 'label'].iloc[0] == 0:
        return values_counts[0] / len(pre_list), 0
    elif df.loc[:, 'label'].iloc[0] == 1:
        return values_counts[1] / len(pre_list), 1


def split_data(err1, nor1, norn, num=0.75):
    #    err1 = [x[use_cols] for x in err1];nor1 = [x[use_cols] for x in nor1];norn = [x[use_cols] for x in norn]
    random.shuffle(err1);
    random.shuffle(nor1);
    random.shuffle(norn)
    train_list = err1[:round(len(err1) * num)];
    test_list = err1[round(len(err1) * num):]
    train_list.extend(nor1[:round(len(nor1) * num)])
    test_list.extend(nor1[round(len(nor1) * num):])
    train_list.extend(norn[:round(len(norn) * num)])
    test_list.extend(norn[round(len(norn) * num):])
    return train_list, test_list


def data_scaler(X_train, X_test):
    '''
    根据scaler对训练集和测试集的特征变量实现标准化（0均值，方差为1）
    :return:
    '''
    scaler = sklearn.preprocessing.StandardScaler().fit(X_train)
    X_train_std = scaler.transform(X_train)
    X_test_std = scaler.transform(X_test)
    return X_train_std, X_test_std, scaler


def data_split(e_list, err_e_list, err_n_list, nor_list):
    all_list = [];
    emptylist = []
    for i in range(1717):
        if err_e_list[i].shape[0] == 0 or err_n_list[i].shape[0] == 0:
            emptylist.append(i)
        else:
            all_list.append([e_list[i], err_e_list[i], err_n_list[i]])
    print('ok,num == %d' % (len(all_list)))
    train_l, test_l = train_test_split(all_list, train_size=0.8, test_size=0.2)
    train_nor, test_nor = train_test_split(nor_list, train_size=0.8, test_size=0.2)
    train_list = [];
    test_ll = []
    for item in train_l:
        train_list.append(item[1])
        train_list.append(item[2])
    for item2 in test_l:
        test_ll.append(item2[1])
        test_ll.append(item2[2])
    test_ll.extend(test_nor)
    train_list.extend(train_nor)
    nor_no_label = copy.deepcopy(test_nor)
    nor_no = [x.drop(['label'], axis=1) for x in nor_no_label]
    test_list = [x[0] for x in test_l]
    test_list.extend(nor_no)
    return train_list, test_list, test_ll, emptylist


if __name__ == '__main__':
    #    trainx,testlist,testx,emptylist = data_split(e_list,err_e_list,err_n_list,temp_vin)
    #    df_train = merged(trainx)
    #    df_test = merged(testx)
    #    df_train = shuffle(df_train)
    #    df_test = shuffle(df_test)
    #
    #    xr,yr = get_xy(df_train)
    #    test_xr,test_yr = get_xy(df_test)

    #    xr = Imputer().fit_transform(xr)
    #    test_xr = Imputer().fit_transform(test_xr)
    #    pca = PCA(n_components=15,whiten=True)

    #    pca.fit(xr)

    #    xp = pca.transform(xr)

    #    test_xp = pca.transform(test_xr)
    #    joblib.dump(pca, 'pca.pkl')
    #    feature_train, feature_test, target_train, target_test = train_test_split(xr,yr,train_size=0.8,test_size=0.2)
    # 随机森林分类树

    #    rfc = RandomForestClassifier(n_jobs=-1,oob_score=True,criterion='gini',max_features=None,min_samples_split = 10,verbose = 1,max_depth =8,
    #                                 min_samples_leaf=1,n_estimators =200,
    #                                 class_weight='balanced')
    #    rfc = RandomForestClassifier(
    #            n_estimators=122, n_jobs=-1,oob_score=1, random_state=None,
    #            verbose=1)
    rfc = RandomForestClassifier(n_jobs=-1, oob_score=True, criterion='gini', max_features='auto',
                                 verbose=1, n_estimators=100, class_weight={0: 1, 1: 7})

    Y = rfc.predict(feature_test)
    # 评估模型准确率

    r_rate = rfc.score(feature_test, target_test)
    print('准确率：', r_rate)
    classification_report(target_test, Y)

    confusion_matrix_plot_matplotlib(Y, target_test, cmap=plt.cm.tab10_r)
    joblib.dump(rfc, 'rc01.pkl')
    #    rcf = joblib.load('rcf.pkl')
    print('...............>> now give real test ! <<.....................')
    y_test = rfc.predict(test_xr)

    classification_report(test_yr, y_test)
    confusion_matrix_plot_matplotlib(y_test, test_yr, cmap=plt.cm.tab10_r)
    print('...............>>  real test over ! <<.....................')
##    rfc = joblib.load('.//model//7_rcf73-92.pkl')
##    pca = joblib.load('.//model//7_pca73-92.pkl')
#
#
#
imports = dict(zip(use_colsl, list(rfc.feature_importances_)))
imports = sorted(imports.items(), key=lambda x: x[1], reverse=True)
# 小结
# 后期经过模型融合准确率和召回率都在93 % 以上。值得指出的是，预测结果是统计指定时间段内label为1的占比，超过指定值即认为会发生故障。如将预测目标改为剩余公里数，需对打标方式进行调整，即以维修时间前转速非零的里程值开始前推100公里标记为1，更好的方式是使label为递增值，最后对label做回归。
# 其实不仅是汽车蓄电池故障，很多类似的场景如能做到提前预知，将大大提升效率降低相关风险。如对工业生产设备的故障预测，可提前计划排产最终降低维护、运营成本。
#
# 作者：萧风博宇
# 链接：https: // www.jianshu.com / p / e39bbd29f403
# 来源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。