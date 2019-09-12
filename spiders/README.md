# Data Spiders
## Collect different classes of garbage images for feeding model
- Create virtual environment. (I used conda, feel free to use others.)
- Install packages from requirements.txt for spiders.
- Run below to start.

```bash
cd <where_u_like>/garbage_classification/spiders
python images_downloader.py
```
- If you don't need the proxy for accessing required network, comment below block from the code.
```python
proxy = "socks5h://127.0.0.1:1080"

os.environ['http_proxy'] = proxy 
os.environ['https_proxy'] = proxy
```

---

### ToDo
- Refractor the code and parameterize input.