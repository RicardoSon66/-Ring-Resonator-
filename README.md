# **Optical-Ring-Resonators-Simulation**
**Meep** 와 **Gdsfactory** 파이썬 모듈을 이용하여 링 공진기 구현 및 시뮬레이션 

# **Key Features**
**Silicon Photonics Layout Design**:Gdsfactory를 활용하여 0.5μm 폭의 Single Ring Resonators 설계 및 표준 PDK 기반 레이아웃 생성

**FDTD Simulation Setup**:Meep 엔진을 연동하여 FDTD 시뮬레이션을 진행 또한 표준 PDK를 이용하여 시뮬레이션 신뢰도 향상

**Pulse and CW(Continuous Wave) Analysis**: Wave 가 Pulse일때 Ring Resonators의 응답과 CW일때 응답을 관찰하여 비교

# **Analysis & Engineering Opinion**
이번 프로젝트는 단순 구현만 하는것이 아닌 다른 두가지의 입력에 대해서 실험 결과를 비교하는 프로젝트 입니다.
채택한 두가지 입력은 Pulse와 CW(Continuous Wave)이며 두 실험 모두 1000단위 시간을 기준으로 측정하였습니다.
*단위시간 = 빛이 1μm를 이동하는 시간

### **1.Pulse Wave**
먼저 Pulse일때 상태를 보겠습니다.
### **1.Pulse Wave Response**
![Pulse Wave Response](./Ring_Resonator_unitil1000_Pulse.gif)

직선 도파로에 Pulse Wave의 입력이 가해졌을때 링 도파로와 만나는 지점에 커플링 현상이 잘 일어나는것을 관측할 수 있었습니다.
또한 Pulse Wave가 지나가고 링 내부의 빛이 한바퀴를 돌아 커플링이 되는 지점을 보았을때
전자기학에서 경계조건의 이론에 따라 링 도파로 내부의 Field의 세기가 약하더라도 직선 도파로에 간섭을 하는것을 확인 할 수 있었습니다.
이로 인해 링 내부에 가두어진 에너지가 감쇄를 하며 직선 도파로로 서서히 방출되는 Ring-down 현상을 보았습니다.
하지만 단위시간 1000일때는 Decay로 인해 링 내부의 에너지가 완전 소멸이 되는걸 관측이 안되는것을 확인을 하였을때
이는 Resonators의 성능을 시각적으로 검증이 가능하다는것을 해당 시뮬레이션으로 통해 확인 하였습니다.

### **2.CW**
다음은 CW일때를 보겠습니다.
### **2.CW Response**
![CW Response](./Ring_Resonator_until1000_CW.gif)
관측을 하였을때 Pulse와 다른점이 있다면 직선 도파로에 Wave를 계속 쏘고 있음에도 불구하고
링 내부의 빛이 거의 소멸되는 것처럼 보일 때가 있고 빛이 아주 강해지고 굉장히 희미해지는 지점 이 3가지를 관측을 할 수 있었습니다.
이에 대해 매우 흥미롭다고 생각을 하여 분석을 해보았습니다
### **1.빛이 거의 소멸되는것 처럼 보일때**
이는 링을 한바퀴 돌고 돌아온 빛과 새로 들어오는 빛이 딱 만날때 입니다.
이때 두 빛은 서로 다른 위상을 가지고 있어 상쇄를 하게 되며 결과적으로 에너지가 쌓이는 것이 아닌 사라지는 것 처럼 보이게 됩니다.
이러한 현상을 빛의 **상쇄 간섭**(Destructive Interference) 이라고 합니다.
### **2.빛이 아주 강해지거나 선명해질 때**
1번과 다르게 반대로 빛이 아주 강해진다면 그것이 바로 **공진**(Resonance)가 일어나게 된 것입니다.
이는 한바퀴 돌고온 빛과 새로 들어오는 빛의 위상이 정확히 겹치게 될때 이러한 현상이 일어나고 이때 에너지는 증폭이 이루어 집니다.
이러한 현상을 빛의 **보강 간섭**(Constructive Interference) 라고 합니다.
### **3.빛이 희미하게 남아있을때**
이때는 에너지의 평형에 의해 나타나게 되는데 링으로 들어가는 에너지와 링 내부에서 손실이 이루어진 에너지의 양이 일치할때 이를 **임계 결합**(Critical Coupling)라고 합니다.
이 상태에서는 직선 도파로의 출력단으로 나가는 빛이 거의 0에 수렴을 하게 됩니다.

