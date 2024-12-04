import requests
import flet as ft

# 地域リスト取得用のエンドポイントURL
AREA_LIST_URL = "http://www.jma.go.jp/bosai/common/const/area.json"

# 天気予報取得用のテンプレートURL
WEATHER_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"

# 天気画像のパス
WEATHER_IMAGE_PATH = "weather.png"  # このファイルは同じディレクトリに保存

# 地域リストを取得する関数
def fetch_area_list():
    try:
        # APIから地域リストを取得
        response = requests.get(AREA_LIST_URL)
        response.raise_for_status()  # エラーがあれば例外を発生
        return response.json()  # JSON形式で返す
    except requests.exceptions.RequestException as e:
        print(f"地域リストの取得に失敗: {e}")
        return None

# 地域の天気予報を取得する関数
def fetch_weather_forecast(area_code):
    try:
        # 天気予報のURLを構築
        url = WEATHER_URL_TEMPLATE.format(area_code)
        response = requests.get(url)
        response.raise_for_status()  # エラーがあれば例外を発生
        return response.json()  # JSON形式で返す
    except requests.exceptions.RequestException as e:
        print(f"天気予報の取得に失敗: {e}")
        return None

# 天気予報を表示する関数
def show_weather_forecast(page: ft.Page, area_code: str):
    # 天気予報を取得
    weather_data = fetch_weather_forecast(area_code)
    
    if not weather_data:
        page.add(ft.Text("天気予報を取得できませんでした。"))
        return

    # 天気予報の情報を抽出
    forecast_info = ""
    weather_icon = WEATHER_IMAGE_PATH  # 画像パス（初期設定）

    # 天気情報を抽出して表示
    for forecast in weather_data:
        area_name = forecast['area']['name']
        time_series = forecast['timeSeries'][0]
        weather_condition = time_series['areas'][0]['weather']
        forecast_info += f"{area_name}の天気予報:\n"
        forecast_info += f"  - 発表時刻: {time_series['timeDefines'][0]}\n"
        forecast_info += f"  - 天気: {weather_condition}\n"
        
        # 天気に応じた画像を変更（例: 雨、晴れ、曇り）
        if "晴れ" in weather_condition:
            weather_icon = "weather_clear.png"  # 曇りの画像
        elif "雨" in weather_condition:
            weather_icon = "weather_rain.png"  # 雨の画像
        elif "曇り" in weather_condition:
            weather_icon = "weather_cloudy.png"  # 曇りの画像

    # 天気予報情報をページに表示
    page.controls.clear()  # 既存のコンポーネントをクリア
    page.add(
        ft.Image(src=weather_icon, width=200),  # 天気画像を表示
        ft.Text(forecast_info, size=20)  # 天気予報のテキストを表示
    )

# メインアプリケーションの関数
def main(page: ft.Page):
    page.title = "気象庁 天気予報アプリ"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 地域リストを取得
    area_list = fetch_area_list()
    if not area_list:
        page.add(ft.Text("地域リストを取得できませんでした。"))
        return

    # 地域リストをビューに表示
    area_buttons = []
    for area_code, area_info in area_list['centers'].items():
        area_buttons.append(
            ft.ElevatedButton(
                text=area_info['name'],
                on_click=lambda e, code=area_code: show_weather_forecast(page, code)
            )
        )

    # 地域ボタンをページに追加
    page.add(ft.Column(area_buttons, spacing=10))

# Fletアプリケーションを起動
ft.app(target=main)
