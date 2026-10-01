# URL Shortener

Turn a long URL into a short link.

## Install

In PowerShell, from the project folder, run:

```powershell
py -m pip install -r requirements.txt
```

## Run

```powershell
py app.py
```

Open http://127.0.0.1:5000 in your browser.

Enter a long URL and select **Shorten URL**. Click the short link to open the original page.

## Test

```powershell
py -m unittest -v
```

**Note:** Short links are cleared when the app stops or restarts.
