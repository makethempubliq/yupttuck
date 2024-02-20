import pandas as pd
import folium
import pyproj
import numpy as np

def project_array(coord, p1_type, p2_type):
    """
    좌표계 변환 함수
    - coord: x, y 좌표 정보가 담긴 NumPy Array
    - p1_type: 입력 좌표계 정보 ex) epsg:5179
    - p2_type: 출력 좌표계 정보 ex) epsg:4326
    """
    p1 = pyproj.Proj(init=p1_type)
    p2 = pyproj.Proj(init=p2_type)
    fx, fy = pyproj.transform(p1, p2, coord[:, 0], coord[:, 1])
    return np.dstack([fx, fy])[0]

data = pd.read_csv('./data/fulldata_07_24_04_P_일반음식점.csv', encoding = 'cp949')
loc_data = data[['사업장명', '좌표정보(x)', '좌표정보(y)']]
loc_data.dropna(inplace = True)
loc_data = loc_data[loc_data['사업장명'].str.contains('엽기떡볶이')]
loc_data['좌표정보(x)'] = pd.to_numeric(loc_data['좌표정보(x)'], errors="coerce")
loc_data['좌표정보(y)'] = pd.to_numeric(loc_data['좌표정보(y)'], errors="coerce")
df = loc_data[['좌표정보(x)', '좌표정보(y)']]
coord = np.array(df)
p1_type = "epsg:2097"
p2_type = "epsg:4326"
# project_array() 함수 실행
result = project_array(coord, p1_type, p2_type)
loc_data['경도'] = result[:, 0]
loc_data['위도'] = result[:, 1]
loc_data = loc_data.reset_index().drop('index', axis = 1)
m = folium.Map(location = ['37.5536067','126.9674308'], zoom_start = 15)

for i in range(len(loc_data)):
    x = loc_data.loc[i, '위도']
    y = loc_data.loc[i, '경도']
    name = loc_data.loc[i, '사업장명']
    icon=folium.Icon(icon='info-sign')
    folium.Marker(location=[x, y],
                  tooltip=f"{name}",
                  icon=icon,
                  popup=f"<strong>{name}</strong><br><button onclick='fetchData(\"{name}\")'>Show Data</button>"
                  ).add_to(m)
m.save('map_with_markers.html')