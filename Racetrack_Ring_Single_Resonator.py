import numpy as np
import sys

if not hasattr(np, "float_"):
    np.float_ = np.float64
if not hasattr(np, "int_"):
    np.int_ = np.int64
if not hasattr(np, "asfarray"):
    np.asfarray = lambda x, **kwargs: np.array(x, dtype=np.float64, **kwargs)

import meep as mp
import gdsfactory as gf
import gplugins.gmeep as gm
import matplotlib.pyplot as plt
from gdsfactory.generic_tech import get_generic_pdk

get_generic_pdk().activate()

# 1. Ring Resonator 구조 생성
Racetrack = gf.components.ring_single(
    gap=0.2,
    radius=5.0,
    length_x=3.0,
    length_y=0.0
)
Racetrack = gf.add_padding_container(
    Racetrack,
    default=0,
    top=3,
    bottom=3,
    left=10,
    right=8   # reference와 동일하게 복원
)

sim_result = gm.get_simulation(
    component=Racetrack,
    resolution=40,
    is_3d=False
)
sim = sim_result['sim']

# 2. Reference와 완벽히 동일한 좌표/파원 설정
src_x, flux_out_x = -10, 8
Source_f = 1 / 1.55
Source_width = 0.02

sim.sources = [
    mp.EigenModeSource(
        src=mp.GaussianSource(frequency=Source_f, fwidth=Source_width),
        center=mp.Vector3(src_x, 0, 0),
        size=mp.Vector3(0, 1.5, 0),
        direction=mp.X,
        eig_band=1
    )
]

nfreq = 500
flux_Racetrack_mon = sim.add_flux(
    Source_f, Source_width, nfreq,
    mp.FluxRegion(center=mp.Vector3(flux_out_x, 0, 0), size=mp.Vector3(0, 1.5, 0))
)

# 3. flux 계산과 Harminv를 하나의 run으로 통합
#    (필드가 충분히 감쇠할 때까지 기다려야 flux도, Harminv도 정확해짐)
h = mp.Harminv(mp.Ez, mp.Vector3(0, 10.7, 0), Source_f, Source_width)

print('Racetrack 시뮬레이션 시작')

"""sim.plot2D()
plt.savefig("racetrack_sim_check2.png")"""

sim.run(
    mp.after_sources(h),
    until_after_sources=mp.stop_when_fields_decayed(
        dt=50,
        c=mp.Ez,
        pt=mp.Vector3(flux_out_x, 0, 0),
        decay_by=1e-5
    )
)

print("\n--- Harminv 결과 (링 내부 공진 모드) ---")
for m in h.modes:
    print(f"freq={m.freq}, Q={m.Q}, wavelength={1/m.freq*1000:.2f}nm")

# 4. Ring Flux 및 Reference 데이터 수집
Racetrack_flux = np.array(mp.get_fluxes(flux_Racetrack_mon))
ref_flux = np.load("ref_flux.npy")
freqs = np.load("ref_freqs.npy")

# 5. 정규화된 S21 (dB) 계산
s21 = 10 * np.log10(Racetrack_flux / ref_flux)
wavelengths = (1 / freqs) * 1000  # 파장 (nm)

# 6. 최종 그래프 출력
plt.figure(figsize=(9, 5))
plt.plot(wavelengths, s21, color='b', linewidth=1.0)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Normalized S21 (dB)")
plt.title("Normalized Single Ring Resonator Spectrum")
plt.xlim(1520, 1580)
plt.ylim(-30, 2)
plt.grid(True)
plt.show()

ratio = Racetrack_flux / ref_flux
print("\nratio 범위:", ratio.min(), "~", ratio.max())
print("dB 범위:", 10*np.log10(ratio.min()), "~", 10*np.log10(ratio.max()))

if mp.am_master():
    np.save("racetrack_flux.npy", Racetrack_flux)
    np.save("racetrack_freqs.npy", freqs)
    print("데이터 저장 완료")