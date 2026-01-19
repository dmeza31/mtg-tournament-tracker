# Tournament Import Resources

Assets and references for importing full tournaments via the MTG Tournament Tracker API.

## Contents
- `tournament_import_template.json` – Blank starter file
- `tournament_import_example.json` – Complete sample tournament
- `IMPORT_FORMAT_REFERENCE.md` – Field-by-field reference and validation tips
- `DataImport/` – Raw and cleaned sample data (ForTheChildrenShowdown)

## How to Import
1. Open the System Manager app (`system-manager/app.py`).
2. Go to the **📤 Import** tab.
3. Upload a JSON file (use the template/example here as a base).
4. Review the preview and counts, then click **🚀 Import Tournament**.

## CLI Helper
Regenerate matches from raw exports with the helper script at repo root:
```bash
python regenerate_matches.py imports/DataImport/ForTheChildrenShowdown.json
python regenerate_matches.py imports/DataImport/ForTheChildrenShowdown.json imports/DataImport/custom_import.json
```
