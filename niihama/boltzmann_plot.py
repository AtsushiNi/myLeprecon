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

# + [markdown] id="view-in-github"
# <a href="https://colab.research.google.com/github/AtsushiNi/myLeprecon/blob/master/niihama/boltzmann_plot.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# + [markdown] id="Xo_Whsq3-r09"
# ## ボルツマン分布の作成
# Fulcher-αのスペクトルを特定できたので、ボルツマン分布を作成した

# + colab={"base_uri": "https://localhost:8080/"} executionInfo={"elapsed": 11193, "status": "ok", "timestamp": 1605005909126, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="0x0bMDFMpjAE" outputId="ee554c24-20bd-47df-9ab7-0facd295ec7f"
# !pip install netcdf4 
# !pip install git+https://github.com/fujiisoup/pyspectra.git

import os
from os.path import join
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pyspectra

data_path = join('/', 'Volumes', 'BUFFALO', 'SpectrometerData', '20201006-2')
print(os.path.exists(data_path))

# + executionInfo={"elapsed": 11180, "status": "ok", "timestamp": 1605005909128, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="zOoKqgHL3h2I"
file_names = [f'H_{430000 + 5000*i}.nc' for i in range(11)]
data = []
for file_name in file_names:
  data_array = xr.open_dataarray(join(data_path, file_name))
  data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
  data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

# + colab={"base_uri": "https://localhost:8080/", "height": 520} executionInfo={"elapsed": 12201, "status": "ok", "timestamp": 1605005910158, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="kCVrycczrvgg" outputId="09563f04-10c2-488d-f7c8-9363613b9439"
plt.figure(figsize=(15, 5))
long_data = []
for i, p in enumerate(data['motor_coordinate']):
  d = data.sel(motor_coordinate=p).copy()
  d['long_x'] = d['x'][::-1] - 1000 * i
  d['x'] = data['x']
  long_data.append(d.sum('y'))
  plt.plot(d['long_x'], d.sum('y'))
long_data = xr.concat(long_data, dim='motor_coordinate')


# + [markdown] id="0zmQKVkb-8KI"
# ### long_data
#
# | long_data | 各セルの縦の合計|
# | -- | -- |
# | x | 画像のx座標(ピクセル) |
# | long_x | 一枚のグラフにしたときのx座標(ピクセル) |

# + [markdown] id="0UipfDUCAcaT"
# ## 各スペクトルのガウスフィッティング

# + executionInfo={"elapsed": 12189, "status": "ok", "timestamp": 1605005910159, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="mQmW9BsBcPoQ"
def fit(da):
  popt, perr = pyspectra.fit.singlepeak_fit(da['x'].values, da.values)
  return xr.Dataset({
      'A': popt[0], 'x0': popt[1], 'w': popt[2], 'y0': popt[3],
      'data': da,
      'fit': ('x', pyspectra.profiles.Gauss(da['x'].values, *popt))},
      coords={'x': da['x']})


# + [markdown] id="0amw2ELRbJdW"
# ### Q1

# + colab={"base_uri": "https://localhost:8080/", "height": 291} executionInfo={"elapsed": 12182, "status": "ok", "timestamp": 1605005910160, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="higQ73CrAy_5" outputId="3a5896ac-73a4-46cc-a773-2237f47e459d"
plt.figure(figsize=(30, 5))
long_data.sel(motor_coordinate=475000).plot()
plt.xlim(1500, 0)

# + colab={"base_uri": "https://localhost:8080/", "height": 251} executionInfo={"elapsed": 2313, "status": "ok", "timestamp": 1605006189682, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="HJf_kdnBccno" outputId="026167c2-5048-4d4a-8026-3df985a0a3df"
spectrum_lims = [
  [1430, 1500],
  [1300, 1380],
  [1100, 1200],
  [900, 940],
  [605, 640],
  [230, 280]
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
  result = fit(long_data.sel(motor_coordinate=475000).sel(x=slice(spectrum_lims[i][0], spectrum_lims[i][1])))
  result['v'] = 0
  result['N'] = i+1
  result['wave_length'] = wave_lengths[i]
  plt.subplot(1, len(spectrum_lims), i+1)
  result['data'].plot(marker='.')
  result['fit'].plot()
  plt.title('N = {}'.format(i+1))
  plt.xlabel('pixels')
  plt.ylabel('intencity')
  Q1_result.append(result)
Q1_result = xr.concat(Q1_result, dim='N')

# + colab={"base_uri": "https://localhost:8080/", "height": 369} executionInfo={"elapsed": 1541, "status": "ok", "timestamp": 1605006030426, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="8Mx07A5Eej8v" outputId="ef986504-151c-4e9f-c9c7-2f29dd63bff4"
spectrum_lims = [
  [1430, 1500],
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
plt.figure(figsize=(5, 5))
plt.rcParams['font.size'] = 20
Q1_result = []

for i, lims in enumerate(spectrum_lims):
  result = fit(long_data.sel(motor_coordinate=475000).sel(x=slice(spectrum_lims[i][0], spectrum_lims[i][1])))
  result['v'] = 0
  result['N'] = i+1
  result['wave_length'] = wave_lengths[i]
  result['data'].plot(marker='.', ls='--', label='data')
  result['fit'].plot(label='gauss fitting')
  plt.xlabel('pixels')
  plt.ylabel('intencity (a.u.)')
plt.title('')
plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=1, fontsize=14)
plt.fill_between(result['x'], result['fit'], 1086150, facecolor='C1', hatch='x', alpha=0.1)
plt.ylim(1.05*1e6, 1.8*1e6)
plt.savefig(join('drive', 'My Drive', '研究室', 'images','gauss'), bbox_inches='tight')

# + colab={"base_uri": "https://localhost:8080/", "height": 392} executionInfo={"elapsed": 1502, "status": "ok", "timestamp": 1605006196089, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="1sgq1Y_8kLL1" outputId="1772a034-7b76-4bd4-bf60-a39ceb5c4b00"
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

# + [markdown] id="WmtvxcDycXfB"
# ### Q2

# + colab={"base_uri": "https://localhost:8080/", "height": 310} executionInfo={"elapsed": 1691, "status": "ok", "timestamp": 1605006115642, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="JsBFvClXp2NG" outputId="013e47af-f1f2-4353-ea74-a8d3ea284102"
plt.figure(figsize=(30, 5))
long_data.sel(motor_coordinate=465000).plot()

# + colab={"base_uri": "https://localhost:8080/", "height": 252} executionInfo={"elapsed": 2677, "status": "ok", "timestamp": 1605006116793, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="AYjYfh9Yp6uQ" outputId="4f75bf6a-cbfa-4e79-cfda-c311c0d60a9a"
spectrum_lims = [
  [1090, 1150],
  [950, 1020],
  [770, 820],
  [515, 570],
  [210, 250]
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
  result = fit(long_data.sel(motor_coordinate=465000).sel(x=slice(spectrum_lims[i][0], spectrum_lims[i][1])))
  result['v'] = 1
  result['N'] = i+1
  result['wave_length'] = wave_lengths[i]
  plt.subplot(1, len(spectrum_lims), i+1)
  result['data'].plot(marker='.')
  result['fit'].plot()
  plt.title('N = {}'.format(i+1))
  plt.xlabel('pixels')
  plt.ylabel('intencity')
  Q2_result.append(result)
Q2_result = xr.concat(Q2_result, dim='N')

# + colab={"base_uri": "https://localhost:8080/", "height": 392} executionInfo={"elapsed": 3240, "status": "ok", "timestamp": 1605006117761, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="17QFEEzIq795" outputId="8fb9886c-8906-40a9-a942-34a75d539c0a"
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

# + [markdown] id="azG3lgwYr9e_"
# ### Q3

# + colab={"base_uri": "https://localhost:8080/", "height": 310} executionInfo={"elapsed": 2734, "status": "ok", "timestamp": 1605006117762, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="jp_XZFlqsEZ5" outputId="7320c90c-7117-45e5-926b-132a857fe1c1"
plt.figure(figsize=(30, 5))
long_data.sel(motor_coordinate=450000).plot()

# + colab={"base_uri": "https://localhost:8080/", "height": 252} executionInfo={"elapsed": 3538, "status": "ok", "timestamp": 1605006118726, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="XwIfuYhWttdy" outputId="6e423d14-2e04-4981-83fa-2004a829ce7b"
spectrum_lims = [
  [1700, 1750],
  [1570, 1610],
  [1375, 1420],
  [1120, 1160],
  [800, 840],
  [450, 490]
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
  result = fit(long_data.sel(motor_coordinate=450000).sel(x=slice(spectrum_lims[i][0], spectrum_lims[i][1])))
  result['v'] = 2
  result['N'] = i+1
  result['wave_length'] = wave_lengths[i]
  plt.subplot(1, len(spectrum_lims), i+1)
  result['data'].plot(marker='.')
  result['fit'].plot()
  plt.title('N = {}'.format(i+1))
  plt.xlabel('pixels')
  plt.ylabel('intencity')
  Q3_result.append(result)
Q3_result = xr.concat(Q3_result, dim='N')

# + colab={"base_uri": "https://localhost:8080/", "height": 392} executionInfo={"elapsed": 3188, "status": "ok", "timestamp": 1605006118728, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="FURtKob2xc2y" outputId="86b23713-548d-438a-a7f6-48adfdd769a1"
plt.figure(figsize=[15, 5])
plt.subplot(1, 2, 1)
plt.plot(Q3_result['x0'], Q3_result['wave_length'], marker='o')
plt.title('x0 --- wave length')
plt.xlabel('x0 (pixel)')
plt.ylabel('wave length (nm)')
plt.subplot(1, 2, 2)
plt.plot(Q3_result['N'], Q3_result['A'], marker='o')
plt.title('area for each peak')
plt.xlabel('N')
plt.ylabel('area')


# + [markdown] id="KtOZ61eanwvZ"
# ## Estimate population from the intensity

# + [markdown] id="m2c6jRXoobUe"
# <font color='red'>これは怪しい</font>
#
# $$
# A_N \propto n_N g_N g_\mathrm{as} 
# $$
#
# $n_N$ : population with the rotational quantum number $N$
#
# $g_N$: statistical weight for the rotational quantum number $N$, $g_N = 2(N+1)$
#
# $g_\mathrm{as}$ : statistical weight for the nuclear symmetry, $g_\mathrm{as} = \mathrm{mod} (N) * 2 + 1$

# + executionInfo={"elapsed": 1281, "status": "ok", "timestamp": 1605006119191, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="dTRmlS5Oa7B2"
# d状態の回転エネルギー
def e_rot(v, N):
  return ((30.364-1.545*(v+1/2))*N*(N+1)-0.0191*N*(N+1)*N*(N+1))*1.23984/1e4

# 核スピンの縮退度(核スピンの統計重率)
def g_as(N):
  return (N % 2) * 2 + 1

# 回転の統計重率(もしかしたら二乗じゃ無いかも)
def g_N(N):
  return (2*N+1)*(2*N+1)


# + colab={"base_uri": "https://localhost:8080/", "height": 514} executionInfo={"elapsed": 2400, "status": "ok", "timestamp": 1605006330591, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="SkTA_SdUfmpH" outputId="a8fdb4ce-4853-4252-edec-f7f10b61a274"
plt.figure(figsize=[10, 8])
plt.rcParams['font.size'] = 20

Q1_population = Q1_result['A'] * Q1_result['wave_length'] / g_N(Q1_result['N']) / g_as(Q1_result['N'])
Q2_population = Q2_result['A'] * Q2_result['wave_length'] / g_N(Q2_result['N']) / g_as(Q2_result['N'])
Q3_population = Q3_result['A'] * Q3_result['wave_length'] / g_N(Q3_result['N']) / g_as(Q3_result['N'])

#plt.subplot(1, 2, 1)
#Q1_population.plot(marker='o', ls='--')
#Q2_population.plot(marker='o', ls='--')
#Q3_population.plot(marker='o', ls='--')
plt.yscale('log')
#plt.title('N --- population')
plt.xlabel('N')
plt.ylabel('population')

#plt.subplot(1, 2, 2)
plt.semilogy(e_rot(Q1_result['v'], Q1_result['N']), Q1_population, marker='o', ls='--')
plt.semilogy(e_rot(Q2_result['v'], Q2_result['N']), Q2_population, marker='o', ls='--')
plt.semilogy(e_rot(Q3_result['v'], Q3_result['N']), Q3_population, marker='o', ls='--')
plt.xlabel('Rotational Energy (eV)')
plt.ylabel(r"$\frac{I^{dv'N'}_{av''N''}\lambda^{dv'N'}_{av''N''}}{(2N'+1)^2g^{N'}_{as}}$ (a.u.)")

plt.savefig(join('drive', 'My Drive', '研究室', 'images','boltzman'), bbox_inches='tight')

# + colab={"base_uri": "https://localhost:8080/", "height": 337} executionInfo={"elapsed": 1378, "status": "ok", "timestamp": 1605006120252, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="4QbvGtuDzt-6" outputId="fafd1dd2-9a56-4cb6-92b0-5bbc492c9ace"
upper_energy = np.arange(200, 1200, 200)
theory_population = np.exp(-(upper_energy / (8.6171*(1e-5))/300)+7735)
plt.semilogy(upper_energy, theory_population, '-')
plt.xlabel('upper energy (eV)')
plt.ylabel('population')
plt.title("""(v'-v\")=(1-1) Q branch""")

# + executionInfo={"elapsed": 844, "status": "ok", "timestamp": 1605006120253, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="Zm7Jo6omjC9e"



# + executionInfo={"elapsed": 1050, "status": "ok", "timestamp": 1605006122392, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}, "user_tz": -540} id="N0_TTXFc0dF6"

