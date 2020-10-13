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

# # テーマ
# 're-calibration-with-neon-niihama'では取得した波長の範囲が小さすぎて、ネオン線の特定ができなかったのでやり直した

# +
# %pylab inline

import os
from os.path import join
import xarray as xr
# -

bpth = join(os.path.expanduser('~'), 'works', 'myLeprecon')
specpath = join(bpth, 'SpectrometerData', '20201006-2')

# # Plot waterfall

# ### Neon

# +
fig = gcf()
fig.set_facecolor('w')
fig.set_size_inches([25, 25])

R = [f'H_{410000 + 5000 * i}.nc' for i in range(50)]
for i, fp in enumerate(R):
    image_data = xr.open_dataset(join(specpath, fp))

    plot(image_data.to_array()[0].sum(axis=0) + i * 1e6, f'C1')
         
[text(-100, 1.055e6 + 1e6 * i, t[2:-3], color='r') for i, t in enumerate(R)]
xlabel('pixel')
ylabel('intensity')
rcParams['font.size'] = 12
grid()
# -

# ### Hydrogen

# +
fig = gcf()
fig.set_facecolor('w')
fig.set_size_inches([25, 25])

R = [f'Ne_{410000 + 5000 * i}.nc' for i in range(50)]
for i, fp in enumerate(R):
    image_data = xr.open_dataset(join(specpath, fp))

    plot(image_data.to_array()[0].sum(axis=0) + i * 1e6, f'C1')
         
[text(-100, 1.055e6 + 1e6 * i, t[2:-3], color='r') for i, t in enumerate(R)]
xlabel('pixel')
ylabel('intensity')
rcParams['font.size'] = 12
grid()
# -


