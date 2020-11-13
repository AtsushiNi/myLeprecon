# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + id="wUjMcbaJAxgA" executionInfo={"status": "ok", "timestamp": 1605006599885, "user_tz": -540, "elapsed": 35360, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="ebd1c9d0-2db2-4986-93e5-16ad3e749863" colab={"base_uri": "https://localhost:8080/"}
# !pip install git+https://github.com/fujiisoup/pyspectra.git

import os
from os.path import join
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pyspectra
from google_drive_tools import GoogleDrive

GoogleDrive.init_drive()

# + id="OVD_ZxxSBO9m" executionInfo={"status": "ok", "timestamp": 1605006606984, "user_tz": -540, "elapsed": 42441, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="817e60ac-6a07-4083-f6dc-a470e018a99a" colab={"base_uri": "https://localhost:8080/", "height": 223}
file_names = [f'H_{430000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
  data_array = GoogleDrive.download_file('20201106', file_name)
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

# + id="KlNaFwSvBdhJ" executionInfo={"status": "ok", "timestamp": 1605006611380, "user_tz": -540, "elapsed": 46811, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="a7cd31a4-7fc4-4340-9414-30d633874a72" colab={"base_uri": "https://localhost:8080/", "height": 223}
file_names = [f'back_{430000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
  data_array = GoogleDrive.download_file('20201106', file_name)
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

# + id="IJAXHJIxCJf2" executionInfo={"status": "ok", "timestamp": 1605006611383, "user_tz": -540, "elapsed": 46609, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="54d43b29-cf7a-4944-bde0-ff588924d116" colab={"base_uri": "https://localhost:8080/", "height": 280}
pixels = np.array([-8425, -6600, -3670])
wave = np.array([601.8299, 612.1787, 622.4815])
plt.plot(pixels, wave, 'o')

fun = np.poly1d(np.polyfit(pixels, wave, 1))
x = np.linspace(-9000, 2000, 100)
plt.plot(x, fun(x))


# + id="nTZSwasZBgiY" executionInfo={"status": "ok", "timestamp": 1605006611384, "user_tz": -540, "elapsed": 46588, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="ce006943-fc92-4dd3-cdcb-e9b791a50b51" colab={"base_uri": "https://localhost:8080/", "height": 517}
spectrum_data = plasma_data - back_data * 1.0

plt.figure(figsize=[15, 8])
for f in spectrum_data:
  plt.plot(fun(f['long_x']), f, 'C0')
#plt.xlim(-4000, -3500)
plt.xlabel('wavelength (nm)', fontsize=16)
plt.ylabel('intencity (a.u.)', fontsize=16)

# + [markdown] id="L7VvuvSNExh8"
# # D2

# + id="u_CzHsxrEy_X" executionInfo={"status": "ok", "timestamp": 1605006615668, "user_tz": -540, "elapsed": 50852, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="59d4b99f-4a30-4f7a-fcf6-6f2fda72c801" colab={"base_uri": "https://localhost:8080/", "height": 223}
file_names = [f'D_{430000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
  data_array = GoogleDrive.download_file('20201106', file_name)
  data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
  data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

Dplasma_data = []
for i, p in enumerate(data['motor_coordinate']):
  d = data.sel(motor_coordinate=p).copy()
  d['long_x'] = d['x'][::-1] - 1000 * i
  d['x'] = data['x']
  Dplasma_data.append(d.sum('y'))
Dplasma_data = xr.concat(Dplasma_data, dim='motor_coordinate')

# + id="V2k3j0JhE6LQ" executionInfo={"status": "ok", "timestamp": 1605006619958, "user_tz": -540, "elapsed": 55123, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="9e47a863-55b7-4d29-940d-930f3a3e10be" colab={"base_uri": "https://localhost:8080/", "height": 223}
file_names = [f'Dback_{430000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
  data_array = GoogleDrive.download_file('20201106', file_name)
  data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
  data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

Dback_data = []
for i, p in enumerate(data['motor_coordinate']):
  d = data.sel(motor_coordinate=p).copy()
  d['long_x'] = d['x'][::-1] - 1000 * i
  d['x'] = data['x']
  Dback_data.append(d.sum('y'))
Dback_data = xr.concat(Dback_data, dim='motor_coordinate')

# + id="DwHs4QMxE-mx" executionInfo={"status": "ok", "timestamp": 1605006620440, "user_tz": -540, "elapsed": 55587, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="d7c23c45-a568-4e3e-b2b3-220522e01972" colab={"base_uri": "https://localhost:8080/", "height": 517}
Dspectrum_data = Dplasma_data - Dback_data * 1.0

plt.figure(figsize=[15, 8])
for f in Dspectrum_data:
  plt.plot(fun(f['long_x']), f, 'C0')
#plt.xlim(-4000, -3500)
plt.xlabel('wavelength (nm)', fontsize=16)
plt.ylabel('intencity (a.u.)', fontsize=16)

# + [markdown] id="0c1ERuvyFmQf"
# # Ar

# + id="KdQ75s6qFeY0" executionInfo={"status": "ok", "timestamp": 1605006624298, "user_tz": -540, "elapsed": 59426, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="5b448502-3def-44ec-f8a0-95cd64d7d0cc" colab={"base_uri": "https://localhost:8080/", "height": 223}
file_names = [f'Ar_{430000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
  data_array = GoogleDrive.download_file('20201106', file_name)
  data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
  data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

Aplasma_data = []
for i, p in enumerate(data['motor_coordinate']):
  d = data.sel(motor_coordinate=p).copy()
  d['long_x'] = d['x'][::-1] - 1000 * i
  d['x'] = data['x']
  Aplasma_data.append(d.sum('y'))
Aplasma_data = xr.concat(Aplasma_data, dim='motor_coordinate')

# + id="Jn1CHRxlF1pY" executionInfo={"status": "ok", "timestamp": 1605006624300, "user_tz": -540, "elapsed": 59411, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="d28fd99b-d82f-4338-fbed-59917e06fabc" colab={"base_uri": "https://localhost:8080/", "height": 223}
file_names = [f'Dback_{430000 + 5000*i}.nc' for i in range(10)]
data = []
for file_name in file_names:
  data_array = GoogleDrive.download_file('20201106', file_name)
  data_array['motor_coordinate'] = data_array.attrs['motor_coordinate']
  data.append(data_array)
data = xr.concat(data, dim='motor_coordinate')

Dback_data = []
for i, p in enumerate(data['motor_coordinate']):
  d = data.sel(motor_coordinate=p).copy()
  d['long_x'] = d['x'][::-1] - 1000 * i
  d['x'] = data['x']
  Dback_data.append(d.sum('y'))
Dback_data = xr.concat(Dback_data, dim='motor_coordinate')

# + id="XYgouLqiF3ce" executionInfo={"status": "ok", "timestamp": 1605006624909, "user_tz": -540, "elapsed": 60003, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="f253eb9c-f979-4905-9220-d448c6450352" colab={"base_uri": "https://localhost:8080/", "height": 528}
Aspectrum_data = Aplasma_data - Dback_data * 1.0

plt.figure(figsize=[15, 8])
for f in Aspectrum_data:
  plt.plot(fun(f['long_x']), f, 'C0')
#plt.xlim(-4000, -3500)
plt.xlabel('wavelength (nm)', fontsize=16)
plt.ylabel('intencity (a.u.)', fontsize=16)

# + id="QR05HmPgF8ZK" executionInfo={"status": "ok", "timestamp": 1605006648421, "user_tz": -540, "elapsed": 1939, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="8fe96659-082f-4ce7-dd37-320dcee1cb57" colab={"base_uri": "https://localhost:8080/", "height": 649}
plt.subplots_adjust(top=2)
plt.figure(figsize=[15, 10])
plt.subplot(3, 1, 1)
plt.rcParams['font.size'] = 14
plt.title('H2')
plt.ylabel('intencity (a.u.)')
for f in spectrum_data:
  plt.plot(fun(f['long_x']), f, 'C0')
plt.subplot(3, 1, 2)
plt.title('D2')
plt.ylabel('intencity (a.u.)')
for f in Dspectrum_data:
  plt.plot(fun(f['long_x']), f, 'C0')
plt.subplot(3, 1, 3)
plt.title('Ar')
plt.ylabel('intencity (a.u.)')
for f in Aspectrum_data:
  plt.plot(fun(f['long_x']), f, 'C0')

plt.xlabel('wavelength (nm)')
plt.savefig(join(os.path.expanduser('~'), 'works', 'images', 'plasmas'))

# + id="ArZ4HYYyGiEE" executionInfo={"status": "ok", "timestamp": 1605006626549, "user_tz": -540, "elapsed": 61628, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}}

