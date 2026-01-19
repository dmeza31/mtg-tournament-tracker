# Tournament Import Assets (UI/DataImport)

This folder contains raw tournament data and validated import-ready JSON files used by the Streamlit "Import Tournament" feature.

## Files
- ForTheChildrenShowdown.json: Raw tournament export from the external platform (source data).
- ForTheChildrenShowdown_import.json: Cleaned, schema-compliant import file generated from the raw export.
- Related references: see TOURNAMENT_IMPORT_GUIDE.md and UI/IMPORT_FORMAT_REFERENCE.md in the repository root for full field descriptions and validation rules.

## Regenerating an import file
Use the parameterized helper script at the repo root:

```bash
python regenerate_matches.py UI/DataImport/ForTheChildrenShowdown.json
# or specify a custom output file
python regenerate_matches.py UI/DataImport/ForTheChildrenShowdown.json UI/DataImport/custom_import.json
```

Notes:
- The script defaults the output name to <input_name>_import.json when not provided.
- If an output file already exists, the script preserves its players and decks arrays and only regenerates matches/games.
- Each match will include 2-3 games to satisfy the importer validation.

## Importing via UI
1. Open the Streamlit app (default http://localhost:8501).
2. Go to the "Import Tournament" tab and upload the latest *_import.json file.
3. Review the preview and confirm import. See TOURNAMENT_IMPORT_GUIDE.md for detailed screenshots, troubleshooting, and API usage.

## Tips
- Keep the raw export alongside the generated *_import.json for traceability.
- Validate JSON syntax before uploading (jsonlint.com works well).
- If you add new tournaments, name files consistently (e.g., MyEvent2026.json and MyEvent2026_import.json).
