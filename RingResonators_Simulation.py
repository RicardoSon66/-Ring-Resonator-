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

get_generic_pdk().activate() #PDK 활성화

c = gf.components.ring_single(gap = 0.2, radius = 5.0, length_x = 4.0, length_y = 0.0 ) #gap 0.2μm, 반지름 5μm, 커플링 구간의 길이 4μm 링 공진기

c = gf.add_padding_container(c, default = 3) # PML과 소스 배치를 위해 레이아웃 주변영역을 상하 3μm 증가

print("setting")
#Pulse Wave 를 사용하고 싶으면 이대로 사용
sim_results = gm.get_simulation(
    component=c,
    resolution=20,
    is_3d=False,
)
#1μm 당 격자를 20개로 조정 및 3d 비활성화 코드

center_f = 1 / 1.55 # 1.55μm 파장에 해당하는 주파수 (f = c/λ)
center_value = mp.Vector3(-12, 0, 0) # 광원이 위치할 버스 도파로 입구 좌표
#두개 다 source 가 CW로 설정하는 코드일때 필요한 값

sim = sim_results['sim']
#CW 사용 시 아래 주석을 해제
'''
sim.sources = [
    mp.EigenModeSource(
        src = mp.ContinuousSource(frequency=center_f),
        center = center_value,
        size = mp.Vector3(0, 2, 0), # 빛의 크기를 도파로 단면 만큼 키움
        direction=mp.X, # x축 방향으로 빛을 발사
        eig_band=1 # 기본 모드만 사용
    )
]
'''

fig = plt.figure(figsize=(10,8))
animate = mp.Animate2D(sim, fields=mp.Ez, f=fig, realtime=False, normalize=True)

print("Loading")
sim.run(mp.at_every(7, animate), until = 100) # at_every(7) 7단위 시간마다 캡쳐 숫자가 작을 수록 파일 용량 증가

filename = "파일 이름 설정"
animate.to_gif(10, filename)
print("End")
