# LOL_Data-Analysis
---
## 서론

최근 E-SPORT의 인기과 규모가 커지면서 아시안게임의 정식 종목으로 채택되기도 하는 등 기계 학습을 사용하여 데이터를 효율적으로 분석, 승부 예측이나 선수 분석 등에 사용하고 있다. 현재는 전과는 다른 하나의 스포츠 분야로 인식되고 있다. 하지만 게임에 대한 전반적이 이해가 없으면 이해하기가 불가능한 어려운 종목이라고 생각한다. 해당 게임을 해본 이는 알겠지만 어떠한 행동이 승패의 어떤 영향을 미칠지 의견이 분분한 때도 있다. 이러하여 상위권 데이터를 가져와 어떠한 데이터가 승률에 가장 영향을 끼치는지 분석하기로 한다.

---

## 본론

1) 데이터 수집

-  RIOT GAMES에서 제공하는 API를 이용하여 2023시즌 동안의 최상의 티어 챌린저,그랜드마스터,마스터 티어에 플레이어의 순위를 결정하는 랭크 게임 데이터를 확보한다.
-  모델 선정 
--
## 변수설명

- teamId - 경기내의 파랑팀 (100) / 경기내의 빨강팀 (200)
- win - 승 / 패 , target_variable로 사용할 변수입니다. (W/F)
- firstBlood - 가장 먼저 상대팀의 챔피언을 킬했는지 여부. (T/F)
- firstTower - 가장 먼저 상대팀의 포탑을 깻는지 여부. (T/F)
- firstinhibitor - 가장 먼저 상대팀의 억제기를 깻는지 여부. (T/F)
- firstBaron - 가장 먼저 바론을 먹었는지 여부. (T/F)
- firstDragon - 가장 먼저 드래곤을 먹었는지 여부. (T/F)
- firstRiftHerald - 가장 먼저 전령을 먹었는지 여부. (T/F)
- towerKills - 깬 타워의 수(연속형변수)
- inhibitorKills - 깬 억제기의 수(연속형변수)
- baronKills - 처치한 바론의 수(연속형변수)
- dragonKills - 처치한 드래곤의 수(연속형변수)
- vilemawKills - 상관하지 않아도 되는 변수입니다.(5:5 게임에는 없는 오브젝트)
- riftHeraldKills - 처치한 전령의 수 (게임 내에서 전령은 20분전까지 한번밖에 나오지 않으므로 사실상 0과1로 나뉩니다.)
- dominionVictoryScore - 상관하지 않아도 되는 변수입니다.
- gameDuration - 경기 시간, 초 (연속형변수)

--
