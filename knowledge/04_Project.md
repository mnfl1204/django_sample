
## 新規Djangoプロジェクトを作成する場合
```
python -m pip install Django
python -m django --version

django-admin startproject {プロジェクト名}
python manage.py startapp {アプリ名}
```

## Pythonのライブラリ取込
```
pip install -r requirements.txt
pip install -r test_requirements.txt
```

## Docker基本コマンド
```
# 起動　
  docker compose up {-d}
# 終了
  docker compose down

# DB確認
  docker compose exec {image名} bash
  mysql -u sysadmin -p
# 補足（hostから接続）
  mysql -u sysadmin -h 127.0.0.1 -P 3306 -p
```

## DBマイグレーション
```
python manage.py makemigrations {アプリ名（省略可）}
python manage.py migrate {アプリ名（省略可）}

# 指定バージョンに戻す（以下は0001に戻す場合、全部戻す場合はzero）
python manage.py migrate {アプリ名（省略可）} 0001

# admin画面を使う場合のスーパーユーザー作成
python manage.py createsuperuser
```

## サーバー起動
```
python manage.py runserver
```
