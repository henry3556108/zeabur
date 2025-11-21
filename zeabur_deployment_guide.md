# 如何將 Python API 部署到 Zeabur

這份指南將協助您將簡單的 Python Flask API 部署到 Zeabur 平台。

## 前置準備

確保您的專案目錄包含以下檔案：
- `main.py`: 您的應用程式程式碼
- `requirements.txt`: 列出專案依賴套件 (必須包含 `Flask` 和 `gunicorn`)

## 步驟 1：推送程式碼到 GitHub

Zeabur 透過 GitHub 進行部署，因此您需要將程式碼推送到 GitHub 儲存庫。

### 1.1 在 GitHub 上建立新的 Repository

1. 前往 [GitHub](https://github.com)
2. 點擊右上角的 **+** 按鈕，選擇 **New repository**
3. 輸入 Repository 名稱 (例如 `zeabur-demo`)
4. 選擇 **Public** 或 **Private**
5. 點擊 **Create repository**

### 1.2 將本地專案推送到 GitHub

在您的專案目錄中執行以下指令：

```bash
# 初始化 Git repository
git init

# 加入所有檔案
git add .

# 建立第一個 commit
git commit -m "Initial commit"

# 設定主分支名稱
git branch -M main

# 加入遠端 repository (請替換成您的 GitHub Repository URL)
git remote add origin https://github.com/您的使用者名稱/zeabur-demo.git

# 推送到 GitHub
git push -u origin main
```

## 步驟 2：在 Zeabur 上部署

### 2.1 登入 Zeabur

1. 前往 [Zeabur Dashboard](https://dash.zeabur.com)
2. 點擊 **Sign in with GitHub** 使用 GitHub 帳號登入
3. 授權 Zeabur 存取您的 GitHub 帳號

### 2.2 建立新專案

1. 在 Zeabur Dashboard 點擊 **Create Project**
2. 選擇部署區域 (建議選擇 **Asia** 以獲得較低延遲)
3. 輸入專案名稱 (可選)
4. 點擊 **Create**

### 2.3 部署服務

1. 進入剛建立的專案
2. 點擊 **Deploy New Service**
3. 選擇 **GitHub**
4. 在搜尋框中輸入您的 Repository 名稱 (例如 `zeabur-demo`)
5. 找到並點擊您的 Repository
6. 點擊 **Import**

Zeabur 會自動：
- 偵測這是一個 Python 專案
- 讀取 `requirements.txt` 並安裝依賴
- 建置並部署您的應用程式

### 2.4 等待部署完成

部署過程通常需要 1-3 分鐘。您可以在服務頁面查看建置日誌 (Build Logs)。

## 步驟 3：設定網域

部署完成後，您需要設定網域才能公開存取您的 API。

1. 在服務頁面點擊 **Networking** 分頁
2. 點擊 **Generate Domain** 按鈕
3. Zeabur 會自動產生一個網域 (例如 `zeabur-demo-xxxxx.zeabur.app`)
4. 點擊該網域即可開啟您的 API

您應該會看到：
```
Hello from Zeabur! (Python)
```

## 步驟 4：自訂網域 (可選)

如果您有自己的網域，可以設定自訂網域：

1. 在 **Networking** 分頁點擊 **Custom Domain**
2. 輸入您的網域名稱 (例如 `api.yourdomain.com`)
3. 依照指示在您的 DNS 服務商設定 CNAME 記錄
4. 等待 DNS 生效 (通常需要數分鐘到數小時)

## 常見問題

### Q: 為什麼我的應用程式無法啟動？

**A:** 請確認以下事項：
- `main.py` 中的應用程式使用 `PORT` 環境變數
- `requirements.txt` 包含所有必要的依賴套件
- 檢查 Zeabur 的建置日誌 (Build Logs) 查看錯誤訊息

### Q: 如何指定 Python 版本？

**A:** 在專案根目錄建立 `runtime.txt` 檔案，內容為：
```
python-3.11
```

### Q: 如何設定環境變數？

**A:** 
1. 在服務頁面點擊 **Variables** 分頁
2. 點擊 **Add Variable**
3. 輸入變數名稱和值
4. 點擊 **Save**

### Q: 部署後如何更新程式碼？

**A:** 只需將新的程式碼推送到 GitHub：
```bash
git add .
git commit -m "Update code"
git push
```

Zeabur 會自動偵測到變更並重新部署。

### Q: 如何查看應用程式日誌？

**A:** 在服務頁面點擊 **Logs** 分頁即可查看即時日誌。

## 進階設定

### 使用 Gunicorn 作為 Production Server

在 `requirements.txt` 中已包含 `gunicorn`。Zeabur 會自動使用 Gunicorn 來執行您的應用程式。

如果需要自訂 Gunicorn 設定，可以建立 `zbpack.json`：

```json
{
  "start_command": "gunicorn main:app --workers 4 --bind 0.0.0.0:$PORT"
}
```

### 連接資料庫

Zeabur 支援多種資料庫服務 (PostgreSQL, MySQL, MongoDB, Redis 等)：

1. 在專案中點擊 **Deploy New Service**
2. 選擇 **Prebuilt Services**
3. 選擇您需要的資料庫
4. Zeabur 會自動注入連線資訊到環境變數中

## 總結

恭喜！您已經成功將 Python Flask API 部署到 Zeabur。

主要步驟回顧：
1. ✅ 將程式碼推送到 GitHub
2. ✅ 在 Zeabur 建立專案並連接 GitHub Repository
3. ✅ 等待自動部署完成
4. ✅ 設定網域並測試 API

如有任何問題，請參考 [Zeabur 官方文件](https://zeabur.com/docs) 或聯繫支援團隊。
