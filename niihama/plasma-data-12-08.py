# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
# !pip install git+https://github.com/fujiisoup/pyspectra.git

import os
from os.path import join
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pyspectra
from scipy import interpolate

data_path = join('/', 'Volumes', 'BUFFALO', 'SpectrometerData', '20201208_niihama')
print(os.path.exists(data_path))
# -

data_path = join('..', '20201208_niihama')
print(os.path.exists(data_path))

# +
file_names = [f'H_{420000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
    data_array = xr.open_dataarray(join(data_path, file_name))
    data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
    data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

plasma_data = []
for i, p in enumerate(data['motor_coordinate']):
  d = data.sel(motor_coordinate=p).copy()
  d['long_x'] = d['x'][::-1] - 1000 * i
  d['x'] = data['x']
  plasma_data.append(d.sum('y'))
plasma_data = xr.concat(plasma_data, dim='motor_coordinate')

# +
file_names = [f'back_{420000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
    data_array = xr.open_dataarray(join(data_path, file_name))
    data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
    data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

back_data = []
for i, p in enumerate(data['motor_coordinate']):
    d = data.sel(motor_coordinate=p).copy()
    d['long_x'] = d['x'][::-1] - 1000 * i
    d['x'] = data['x']
    back_data.append(d.sum('y'))
back_data = xr.concat(back_data, dim='motor_coordinate')

# +
file_names = [f'sekibun_{420000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
    data_array = xr.open_dataarray(join(data_path, file_name))
    data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
    data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

sekibun_data = []
for i, p in enumerate(data['motor_coordinate']):
    d = data.sel(motor_coordinate=p).copy()
    d['long_x'] = d['x'][::-1] - 1000 * i
    d['x'] = data['x']
    sekibun_data.append(d.sum('y'))
sekibun_data = xr.concat(sekibun_data, dim='motor_coordinate')

# +
spectrum_data = plasma_data - back_data * 1.0

plt.figure(figsize=[15, 10])
plt.subplot(3, 1, 1)
plt.ylim(1.03*1e6, 1.9*1e6)
plt.title('plasma')
for f in plasma_data:
  plt.plot(f['long_x'], f)

plt.subplot(3, 1, 2)
plt.title('back ground')
plt.ylim(1.03*1e6, 1.9*1e6)
for f in back_data:
  plt.plot(f['long_x'], f)

plt.subplot(3, 1, 3)
plt.title('H2 spectrum')
for f in spectrum_data:
  plt.plot(f['long_x'], f)


# -

# # 波長校正

def fit(da):
  popt, perr = pyspectra.fit.singlepeak_fit(da['x'].values, da.values)
  return xr.Dataset({
      'A': popt[0], 'x0': popt[1], 'w': popt[2], 'y0': popt[3],
      'data': da,
      'fit': ('x', pyspectra.profiles.Gauss(da['x'].values, *popt))},
      coords={'x': da['x']})


# ## Q1

plt.figure(figsize=(30, 5))
spectrum_data.sel(motor_coordinate=465000).plot()
plt.xlim(0, 1200)
plt.ylim(0, 30000)

# +
spectrum_lims = [
  [1110, 1170],
  [990, 1040],
  [810, 860],
  [567, 610],
  [210, 310],
#  [240, 280]
]
wave_lengths = [
  601.8299,
  602.3757,
  603.1909,
  604.2716,
  605.6091,
  607.1996,
  609.0374,
  610.9030
]
plt.figure(figsize=(35, 5))
Q1_result = []

for i, lims in enumerate(spectrum_lims):
    result = fit(spectrum_data.sel(motor_coordinate=465000).sel(x=slice(spectrum_lims[i][0], spectrum_lims[i][1])))
    result['v'] = 0
    result['N'] = i+1
    result['wave_length'] = wave_lengths[i]
    result['long_x'] = spectrum_data.sel(motor_coordinate=465000).isel(x=int(result['x0'].values.tolist()))['long_x']
    plt.subplot(1, len(spectrum_lims), i+1)
    result['data'].plot(marker='.')
    result['fit'].plot()
    plt.title('N = {}'.format(i+1))
    plt.xlabel('pixels')
    plt.ylabel('intencity')
    Q1_result.append(result)
Q1_result = xr.concat(Q1_result, dim='N')
# -

plt.figure(figsize=[15, 5])
plt.subplot(1, 2, 1)
plt.plot(Q1_result['x0'], Q1_result['wave_length'], marker='o')
plt.title('x0 --- wave length')
plt.xlabel('x0 (pixel)')
plt.ylabel('wave length (nm)')
plt.subplot(1, 2, 2)
plt.plot(Q1_result['N'], Q1_result['A'], marker='o')
plt.title('area for each peak')
plt.xlabel('N')
plt.ylabel('area')

# ## Q2

plt.figure(figsize=(30, 5))
spectrum_data.sel(motor_coordinate=455000).plot()
plt.xlim(0, 1000)
#plt.ylim(0, 50000)

# +
spectrum_lims = [
  [750, 800],
  [600, 680],
  [430, 480],
  [180, 227],
]
wave_lengths = [
  612.1787,
  612.7246,
  613.5395,
  614.6186,
  615.9565
]
plt.figure(figsize=(35, 5))
Q2_result = []

for i, lims in enumerate(spectrum_lims):
    result = fit(spectrum_data.sel(motor_coordinate=455000).sel(x=slice(spectrum_lims[i][0], spectrum_lims[i][1])))
    result['v'] = 0
    result['N'] = i+1
    result['wave_length'] = wave_lengths[i]
    result['long_x'] = spectrum_data.sel(motor_coordinate=455000).isel(x=int(result['x0'].values.tolist()))['long_x']
    plt.subplot(1, len(spectrum_lims), i+1)
    result['data'].plot(marker='.')
    result['fit'].plot()
    plt.title('N = {}'.format(i+1))
    plt.xlabel('pixels')
    plt.ylabel('intencity')
    Q2_result.append(result)
Q2_result = xr.concat(Q2_result, dim='N')
# -

plt.figure(figsize=[15, 5])
plt.subplot(1, 2, 1)
plt.plot(Q2_result['x0'], Q2_result['wave_length'], marker='o')
plt.title('x0 --- wave length')
plt.xlabel('x0 (pixel)')
plt.ylabel('wave length (nm)')
plt.subplot(1, 2, 2)
plt.plot(Q2_result['N'], Q2_result['A'], marker='o')
plt.title('area for each peak')
plt.xlabel('N')
plt.ylabel('area')

# ## Q3

plt.figure(figsize=(30, 5))
spectrum_data.sel(motor_coordinate=445000).plot()
plt.xlim(0, 1000)
#plt.ylim(0, 50000)

# +
spectrum_lims = [
  [340, 390],
  [215, 260],
  [18, 63],
]
wave_lengths = [
  622.4815,
  623.0258,
  623.8391,
  624.9150,
  626.2495,
  627.8369,
  629.6622,
  631.7233

]
plt.figure(figsize=(35, 5))
Q3_result = []

for i, lims in enumerate(spectrum_lims):
    result = fit(spectrum_data.sel(motor_coordinate=445000).sel(x=slice(spectrum_lims[i][0], spectrum_lims[i][1])))
    result['v'] = 0
    result['N'] = i+1
    result['wave_length'] = wave_lengths[i]
    result['long_x'] = spectrum_data.sel(motor_coordinate=445000).isel(x=int(result['x0'].values.tolist()))['long_x']
    plt.subplot(1, len(spectrum_lims), i+1)
    result['data'].plot(marker='.')
    result['fit'].plot()
    plt.title('N = {}'.format(i+1))
    plt.xlabel('pixels')
    plt.ylabel('intencity')
    Q3_result.append(result)
Q3_result = xr.concat(Q3_result, dim='N')
# -

# # ピクセルを波長に変換

# +
wavelength = np.concatenate([Q1_result['wave_length'].values, Q2_result['wave_length'].values, Q3_result['wave_length'].values])
longx = np.concatenate([Q1_result['long_x'].values, Q2_result['long_x'].values, Q3_result['long_x'].values])

longx_to_wavelength_fun = np.poly1d(np.polyfit(longx, wavelength, 1))
x = np.linspace(-8100, -3000, 100)

plt.plot(longx, wavelength, marker='x', linestyle='None')
plt.plot(x, longx_to_wavelength_fun(x))
plt.xlabel('long_x (pixel)')
plt.ylabel('wavelength (nm)')

# +
array = []
for a in spectrum_data:
    d = a.assign_coords(wavelength=('x', longx_to_wavelength_fun(a['long_x'])))
    array.append(d)
spectrum_data = xr.concat(array, dim='motor_coordinate')

array = []
for a in sekibun_data:
    d = a.assign_coords(wavelength=('x', longx_to_wavelength_fun(a['long_x'])))
    array.append(d)
sekibun_data = xr.concat(array, dim='motor_coordinate')

plt.figure(figsize=(10, 6))
plt.xlabel('wavelength (nm)')
plt.ylabel('count (a.u.)')
for s in spectrum_data:
    plt.plot(s['wavelength'], s)
# -

# # 感度校正
# 分光器のカウントは、露光時間と放射輝度に比例する

# +
plt.title("積分球の放射輝度データ")
x_value = np.array([300,310,320,330,340,350,400,450,500,555,600,655,700,800,900,1050,1150,1200,1300,1540,1600,1700,2000,2100,2300,2400])
y_value = np.array([1.85e-2,2.80e-2,4.17e-2,5.89e-2,8.08e-2,1.09e-1,3.67e-1,8.03e-1,1.37e-0,2.05e-0,2.56e-0,3.10e-0,3.42e-0,3.80e-0,3.68e-0,3.23e-0,2.65e-0,2.22e-0,1.98e-0,7.69e-1,7.08e-1,6.00e-1,1.42e-1,1.14e-1,6.95e-2,5.01e-2])
plt.plot(x_value, y_value, marker='x', linestyle='None')

sekibun_func = interpolate.interp1d(x_value, y_value, kind='linear')
x = np.linspace(300, 2300, 100)

plt.plot(x, sekibun_func(x))

plt.xlabel("wavelength (nm)")
plt.ylabel(r"放射輝度 ($W m^{-2} nm^{-1} sr^{-1}$)")
# -

sekibun_func(spectrum_data.sel(motor_coordinate=460000)['wavelength']) * spectrum_data.sel(motor_coordinate=460000) / sekibun_data.sel(motor_coordinate=460000)

# +
array = []
for a in spectrum_data['motor_coordinate']:
    d = spectrum_data.sel(motor_coordinate=a).assign_coords(true_data=('x', sekibun_func(spectrum_data.sel(motor_coordinate=a)['wavelength']) * spectrum_data.sel(motor_coordinate=a) / sekibun_data.sel(motor_coordinate=a)))
    array.append(d)
spectrum_data = xr.concat(array, dim='motor_coordinate')

plt.figure(figsize=(10, 6))
plt.xlabel('wavelength (nm)')
plt.ylabel('count (a.u.)')
for s in spectrum_data:
    plt.plot(s['wavelength'], s['true_data'])
# -

# # ボルツマンフィッティング

plt.figure(figsize=(30, 5))
spectrum_data.sel(motor_coordinate=465000).plot()
plt.xlim(1500, 0)


