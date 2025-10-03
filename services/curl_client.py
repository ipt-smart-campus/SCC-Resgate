import json
import os
import platform
import shlex
import subprocess

def _curl_cmd():
    # Em Windows costuma existir curl.exe; noutros, 'curl'
    return "curl.exe" if platform.system().lower().startswith("win") else "curl"

def get_json(url: str, headers: dict | None = None, timeout: int = 10):
    """
    Faz GET com curl e devolve JSON (ou None em erro).
    """
    cmd = [_curl_cmd(), "-s", url]
    if headers:
        for k, v in headers.items():
            cmd += ["-H", f"{k}: {v}"]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout)
        txt = out.decode("utf-8", errors="replace").strip()
        return json.loads(txt)
    except subprocess.CalledProcessError as e:
        print("curl error:", e.output.decode(errors="replace"))
    except json.JSONDecodeError:
        print("Resposta não-JSON de", url)
    except Exception as e:
        print("Erro curl:", e)
    return None
