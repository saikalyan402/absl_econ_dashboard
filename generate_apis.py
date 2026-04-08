import os

api_dir = r"c:\Users\saika\OneDrive\Desktop\april-13-app-2026\economic dashboard\apis"
os.makedirs(api_dir, exist_ok=True)

endpoints = {
    "nifty.py": "nifty",
    "mostactive.py": "mostactive",
    "sme.py": "sme",
    "securities.py": "securities",
    "snapshot.py": "snapshot",
    "high_low_52weeks.py": "high_low_52weeks",
    "volume_gainers.py": "volume_gainers"
}

template = """from fastapi import APIRouter
from scraper_jobs import serve_data

router = APIRouter()

@router.get("/{name}", tags=["{name}"])
async def get_{name}():
    return await serve_data("{name}")
"""

for filename, name in endpoints.items():
    filepath = os.path.join(api_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template.format(name=name))

# Also write __init__.py
with open(os.path.join(api_dir, "__init__.py"), "w", encoding="utf-8") as f:
    pass

print("API files generated.")
