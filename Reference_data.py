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

# 1. Straight Waveguide 생성
c = gf.components.straight(length=24, width=0.5)
c = gf.add_padding_container(c, default=0, top=3, bottom=3, left=10, right=8)

sim_results = gm.get_simulation(
    component=c,
    resolution=40,
    is_3d=False
)
sim = sim_results['sim']

# 2. 좌표 정의 (Ring 코드와 동일해야 함)

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
flux_ref_mon = sim.add_flux(
    Source_f, Source_width, nfreq,
    mp.FluxRegion(center=mp.Vector3(flux_out_x, 0, 0), size=mp.Vector3(0, 1.5, 0))
)

print('Reference 시뮬레이션 시작...')

"""sim.plot2D()
plt.savefig("Reference_Layout_check.png")"""

# 3. 수렴 조건으로 실행
sim.run(
    until_after_sources=mp.stop_when_fields_decayed(
        dt=50,
        c=mp.Ez,
        pt=mp.Vector3(flux_out_x, 0, 0),
        decay_by=1e-5
    )
)

# 4. Flux 데이터 및 주파수 추출 후 파일로 저장
ref_flux = np.array(mp.get_fluxes(flux_ref_mon))
freqs = np.array(mp.get_flux_freqs(flux_ref_mon))

np.save("ref_flux.npy", ref_flux)
np.save("ref_freqs.npy", freqs)
print("Reference 데이터 저장 완료! (ref_flux.npy)")