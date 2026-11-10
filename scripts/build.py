from pathlib import Path
import base64
import mimetypes
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


def inline_asset(match):
    path = SOURCE / match[1]
    if not path.is_file():
        raise FileNotFoundError(path)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'src="data:{mime};base64,{data}"'


fragment = re.sub(
    r'src="(assets/[^"]+)"',
    inline_asset,
    (SOURCE / "keyboard.html").read_text(encoding="utf-8"),
)
template = (SOURCE / "page-shell.html").read_text(encoding="utf-8")
assert template.count("{{KEYBOARD_FRAGMENT}}") == 1
(ROOT / "index.html").write_text(
    template.replace("{{KEYBOARD_FRAGMENT}}", fragment.rstrip()),
    encoding="utf-8",
)
print("Built index.html with embedded assets")
