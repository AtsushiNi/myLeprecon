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

# + id="1wZjskRKtTKL" executionInfo={"status": "ok", "timestamp": 1604849836945, "user_tz": -540, "elapsed": 729, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="c38f4b84-82a2-42bd-fe26-117d0c446953" colab={"base_uri": "https://localhost:8080/"}
# %pylab inline

# + id="3UhwsWsCtTKX" executionInfo={"status": "ok", "timestamp": 1604849837404, "user_tz": -540, "elapsed": 1181, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}}
import os
from os.path import join
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
from google.colab import drive

# + id="DV9tCd4WtTKe" executionInfo={"status": "ok", "timestamp": 1604849858311, "user_tz": -540, "elapsed": 22072, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="bc7bed6d-0170-484b-8d7a-730821117125" colab={"base_uri": "https://localhost:8080/"}
drive.mount('/content/drive')
bpth = join('drive', 'My Drive', '研究室', 'MyLeprecon')
specpath = join(bpth, 'SpectrometerData', '20200820')

# + [markdown] id="YkBmaY7ntTKm"
# # Prot waterfall
#
# I arranged all the data vertically.<br>
# The red number on the left of the graph show the rotation of the moter. The horizontal axis of the graph is the horizontal pixel value of the each image.<br>
# We can see from the graph that the images next to each other overlap about half.
# (Using data is took by Prof.Kuzmin)

# + id="qFWvVTMgtTKn" executionInfo={"status": "ok", "timestamp": 1604849873987, "user_tz": -540, "elapsed": 37745, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}}
fig = gcf()
fig.set_facecolor('w')
fig.set_size_inches([30, 45])

R = [f'{400000 + 5000 * i}.fit' for i in range(21)]
for i, fp in enumerate(R):
  image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)

c = 'k'
if '410000' in fp or '415000' in fp: c = 'C2'
if '600000' in fp or '595000' in fp: c = 'C3'
if '640000' in fp or '645000' in fp or '650000' in fp: c = 'C1'

plot(image_data.sum(axis=0) + i * 1e6, f'{c}')

[text(-130, 1.6e6 + 1e6 * i, t[:-4], color='r') for i, t in enumerate(R)]
xlim(-200, 2100)
xlabel('pixel')
ylabel('intensity')
grid()
plt.close()

# + [markdown] id="ujj-FbmitTKx"
# # Overlap neighbours
# ## H-alpha
# I saw graph and estimated that the graphs next to each other were offset by 1033.5 pixels.<br>
# I plotted a graph and the next graph(add 1033.5 pixels to x axis), and confirmed that the two graph overlap.

# + id="UZZsHI_OtTKy" executionInfo={"status": "ok", "timestamp": 1604849873992, "user_tz": -540, "elapsed": 37733, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="f3abdaef-6139-4ef3-b529-4303a1c7f52b" colab={"base_uri": "https://localhost:8080/", "height": 291}
x = np.arange(2048)
fp = '410000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x, image_data.sum(axis=0), 'k')

fp = '415000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x + 1033.5, image_data.sum(axis=0), 'C0')

grid()

xlim(1400, 1600)

# + [markdown] id="2Grf9LP-tTK3"
# ## H-beta
# The two graph are offset by 945 pixels.

# + id="GHCuZPT9tTK4" executionInfo={"status": "ok", "timestamp": 1604849875796, "user_tz": -540, "elapsed": 39523, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="561fb96d-90da-40a1-c462-3e05a79d8a82" colab={"base_uri": "https://localhost:8080/", "height": 291}
x = np.arange(2048)
fp = '595000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x, image_data.sum(axis=0), 'k')

fp = '600000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x + 945, image_data.sum(axis=0), 'C0')

grid()

xlim(1320, 1380)

# + [markdown] id="tqaE_GG1tTK7"
# ## H-gamma
# The two graph are offset by 915 pixels.

# + id="zMt6RaDJtTK8" executionInfo={"status": "ok", "timestamp": 1604849877062, "user_tz": -540, "elapsed": 40778, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="9255533a-ff78-486a-f14c-14775f0fa335" colab={"base_uri": "https://localhost:8080/", "height": 291}
x = np.arange(2048)
fp = '640000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x, image_data.sum(axis=0), 'k')

fp = '645000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x + 915, image_data.sum(axis=0), 'C0')

grid()

xlim(1900, 2000)

# + [markdown] id="u7-T4B1xtTK-"
# ## other

# + id="kPNHxitrtTK-" executionInfo={"status": "ok", "timestamp": 1604849879731, "user_tz": -540, "elapsed": 43437, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="a220d848-540d-4ffd-9b8c-33bb4068e83b" colab={"base_uri": "https://localhost:8080/", "height": 630}
fig = gcf()
fig.set_size_inches([80, 30])

x = np.arange(2048)
fp = '500000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x, image_data.sum(axis=0), 'k')

fp = '505000.fit'
image_data = fits.getdata(get_pkg_data_filename(join(specpath, fp)), ext=0)
plot(x + 980, image_data.sum(axis=0), 'C0')

grid()

# + [markdown] id="a2mVmhXGtTLB"
# # moter-to-sizeOfOverlap
# I made a graph of the moter range and the size of the overlap.

# + id="vUJ3XuH0tTLB" executionInfo={"status": "ok", "timestamp": 1604849889714, "user_tz": -540, "elapsed": 1081, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="3402c919-ea1d-41ea-a628-d3c6e6d7dcd3" colab={"base_uri": "https://localhost:8080/", "height": 295}
index = np.array([410000,500000, 595000, 640000])
overlap = np.array([1033.5, 980, 945, 915])
plot(index, overlap, 'o')

fun = np.poly1d(np.polyfit(index, overlap, 1))
x = np.linspace(400000, 650000, 100)
plot(x, fun(x))

grid()

xlabel('moter')
ylabel('pixels of overlap')

print(fun.coef)

# + [markdown] id="1dmJHXl9tTLD"
# # Make an overlap spectrum
# I estimated the size of overlap by the previous graph.<br>
# By the function, I overlaid all the data.

# + id="TsjH0G-utTLE" executionInfo={"status": "ok", "timestamp": 1604849911203, "user_tz": -540, "elapsed": 21536, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="7d354d0a-c9b5-4ae7-8e7f-d9169a1c35f2" colab={"base_uri": "https://localhost:8080/", "height": 1000}
R = [f'{410000 + 5000*i}.fit' for i in range(50)]

fig=gcf()
fig.set_facecolor('w')
fig.set_size_inches([20,200])

x_range = np.arange(2048)
overlap = 0
for i,fp in enumerate(R):
    c = 'k'
    if i%2: c = 'C1'
    image_data = fits.getdata(get_pkg_data_filename( join(specpath,fp)),ext=0)
    
    overlap = overlap + fun(410000 + 5000 * i)
    x = x_range + overlap
    y = image_data.sum(axis=0)
    plot(y, x, f'{c}')


grid()
xscale('log')
#xlim(1.7e6,6e6)
axhline(2490)
axhline(38780)
axhline(47750)

# + [markdown] id="Pequ4yWgtTLG"
# # Convert pixels to wave length

# + id="kvkcFxDjtTLG" executionInfo={"status": "ok", "timestamp": 1604849912386, "user_tz": -540, "elapsed": 1166, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="444cdc4d-ef5a-41d4-c0a9-4ad6ac97fcb4" colab={"base_uri": "https://localhost:8080/", "height": 370}
balmers = np.array([656.279, 486.135, 434.047])
rs = np.array([2490, 38780, 47750])
plot(rs/1e4, balmers, 'o')

func = np.poly1d(np.polyfit(rs, balmers, 2))
xp = np.linspace(0, 50000, 100)
plot(xp/1e4, func(xp))
grid()
ylim(400, 700)
xlim(0, 5)
xlabel('accumulated pixel number, $10^{4}$')
ylabel('wavelength, nm')
print(func(5000))
print(10000-(5000-2490))
print(func(10000-(5000-2490)))
print(20000-(5000-2490))
print(func(20000-(5000-2490)))

# + [markdown] id="OFKtb49HtTLI"
# # Apply calibration

# + id="dHen9AUUtTLI" executionInfo={"status": "ok", "timestamp": 1604849915775, "user_tz": -540, "elapsed": 4540, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="9048d1f8-13ca-4e0b-ec08-dca3deaab5f6" colab={"base_uri": "https://localhost:8080/", "height": 1000}
R = [f'{410000 + 5000*i}.fit' for i in range(50)]

fig=gcf()
fig.set_facecolor('w')
fig.set_size_inches([40,40])

x_range = np.arange(2048)
overlap = 0
for i,fp in enumerate(R):
    image_data = fits.getdata(get_pkg_data_filename( join(specpath,fp)),ext=0)
    
    overlap = overlap + fun(410000 + 5000 * i)
    x = func(x_range + overlap)
    y = image_data.sum(axis=0)
    plot(x, y, 'C1')


grid()
ax = gca()
ax.axvspan(600,630,color='C2',alpha = 0.5)
props = dict(boxstyle='round', facecolor='w', alpha=0.9)
ax.text(604,5.5e6,'Fulcher-$\\alpha$',ha='left',bbox=props)
ax.text(654,5.5e6,'$H_\\alpha$',ha='right',bbox=props)
ax.text(484,5.5e6,'$H_\\beta$',ha='right',bbox=props)
ax.text(431,5.5e6,'$H_\\gamma$',ha='right',bbox=props)

yscale('log')
ylim(1.7e6,6e6)
xlim(400,665)

xlabel('wavelength, nm')
ylabel('intensity, a.u.')
fig.text(0.05,.92,'stepping motor\ncoordinate')

# + [markdown] id="ESsSO5wvtTLK"
# # Show Fulcher-α

# + id="agRy4ckztTLL" executionInfo={"status": "ok", "timestamp": 1604579139302, "user_tz": -540, "elapsed": 11312, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="52372049-0ee1-492f-abde-299dfe8f415d" colab={"base_uri": "https://localhost:8080/", "height": 782}
R = [f'{410000 + 5000*i}.fit' for i in range(50)]

fig=gcf()
fig.set_facecolor('w')
fig.set_size_inches([30,20])

x_range = np.arange(2048)
overlap = 0
for i,fp in enumerate(R):
    image_data = fits.getdata(get_pkg_data_filename( join(specpath,fp)),ext=0)
    
    overlap = overlap + fun(410000 + 5000 * i)
    x = func(x_range + overlap)
    y = image_data.sum(axis=0)
    plot(x, y, 'C1')

grid(which = 'major', color = 'black', linestyle = '-')
grid(which = 'minor', color = 'black', linestyle = '-')
# yscale('log')
ylim(1.7e6,6e6)
xlim(600,630)

xlabel('wavelength, nm', fontsize = 20)
ylabel('intensity, a.u.', fontsize = 20)

# + id="Bl6ZfdjOtTLN" executionInfo={"status": "ok", "timestamp": 1604579139305, "user_tz": -540, "elapsed": 11305, "user": {"displayName": "\u65b0\u6ff1\u6566\u53f2", "photoUrl": "", "userId": "13784546731581030034"}} outputId="380c1e1c-77ad-4206-a269-46724eafec50" colab={"base_uri": "https://localhost:8080/", "height": 36}
from IPython.display import Image
Image("./ishihara-spectrum.png")

# + [markdown] id="cSlhI5XHtTLP"
# I compaired my graph with Mr. Ishihara's one.<br>
# I couldn't clearly determine the lines from these graphs.
