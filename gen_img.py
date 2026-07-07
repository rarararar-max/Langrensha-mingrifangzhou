from pathlib import Path
import base64
out = []
out.append("const IMG={")
for i in range(1, 10):
    p = Path(f"D:\\anzhuo\\ailangrensha\\{i}.png")
    b64 = base64.b64encode(p.read_bytes()).decode()
    out.append(f'  {i}: "data:image/png;base64,{b64}",')
out.append("};")
Path("D:\\anzhuo\\ailangrensha\\img_js_output.txt").write_text("\n".join(out), encoding="utf-8")
print("done", len("\n".join(out)), "chars")
