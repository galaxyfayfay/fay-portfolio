# Fay Yu · Personal Portfolio

## 本地预览

```bash
pip install streamlit
streamlit run app.py
```

## 上传照片

把照片文件（.jpg / .png / .webp）放进 `photos/` 文件夹。
文件名会自动读取，按文件名字母顺序排列，最多显示 6 张。

建议命名方式：
```
photos/
  01-tokyo.jpg
  02-paris.jpg
  03-shanghai.jpg
  ...
```

## 部署到 Streamlit Cloud（免费）

1. 把整个项目文件夹推送到 GitHub（含 photos/ 里的图片）
2. 打开 https://share.streamlit.io
3. 点 "New app" → 选你的 repo → Main file: `app.py`
4. Deploy

部署完成后会得到一个 `.streamlit.app` 的链接，直接分享即可。
