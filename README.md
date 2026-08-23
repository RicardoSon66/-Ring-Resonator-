# **완전한 원형 Ring Resonator의 분석 및 한계**
#**1.개요**
이번에 알아 볼 것은 Ring Resonator를 분석합니다. 분석 환경은 Python를 사용하였고 Layout module는 gdsfactory를 사용하였고 FDTD module는 Meep를 사용하였습니다.
Ring Resonator의 스펙은 Bus와 Ring의 gap은 0.2μm 이며 Ring의 Radius는 5.0μm 입니다. length_X, Y는 0이기에 완전한 원형 Ring입니다. λ = 1.55μm 이며 주파수로는 1/1.55입니다.
waveguide의 물질은 Si 실리콘이며 Cladding 영역은 SiO2 즉 silicon-dioxide 이며 이는 표준 PDK를 사용합니다.

#**2.시뮬레이션 세팅 및 정규화**
시뮬레이션을 하기 위해 Source는 Gaussian Source 이며 λ = 1.55μm, Fwidth = 0.1이고 EigenModeSource를 사용하였습니다. Resolution는 20으로 초기에 설정하였고 오차를 줄이기 위해 40으로 늘려 더욱 정밀화를 하였습니다.
정규화를 진행하기 위해 링 구조가 없는 단일 Straight waveguide를 먼저 실험 하여 Reference Flux 데이터를 수집하고 저장 후 
$$S_{21}(\text{dB}) = 10 \times \log_{10}\left(\frac{P_{\text{ring}}}{P_{\text{ref}}}\right)$$
라는 공식을 통해 **0dB** 기준선 보정을 완료 하였습니다.





