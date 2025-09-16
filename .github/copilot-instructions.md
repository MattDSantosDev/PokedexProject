# Copilot Instructions for Pokemon Pokedex Main

## Project Overview
- This project is a simple command-line tool for querying Pokémon data using the `pokebase` library.
- The main entry point is `Pokemon_pokedex_Main`, which contains a script for interactive user queries about Pokémon characteristics.

## Architecture & Data Flow
- User input is collected via the console and used to query the `pokebase` API for Pokémon species, types, evolution chains, and Pokédex entries.
- The code is structured as a single script with a `main()` function calling `pokemon_basics()`.
- All data retrieval is handled through the `pokebase` library, so no local data models or custom API logic are present.

## Developer Workflows
- **Run the script:** Execute `Pokemon_pokedex_Main` with Python 3.13+ (ensure `pokebase` is installed).
- **Dependencies:** Install with `pip install pokebase`.
- **Debugging:** Use print statements for debugging; there are no custom logging or error handling conventions.
- **Testing:** No automated tests are present; manual testing is done by running the script and providing input.

## Project-Specific Conventions
- All user interaction is via `input()` and `print()`.
- Pokémon names are converted to lowercase before querying.
- Only a subset of characteristics are supported (type, evolution, dex entry); height/weight are commented out and not implemented.
- The script expects valid Pokémon names; no custom error handling for invalid input.

## Integration Points
- Relies entirely on the `pokebase` library for data access.
- No other external APIs, databases, or services are used.

## Example Usage
```bash
python Pokemon_pokedex_Main
```

## Key Files
- `Pokemon_pokedex_Main`: Main script containing all logic.

---

**For AI agents:**
- Focus on extending the script by adding new characteristics or improving user interaction.
- Follow the existing pattern of using `pokebase` for all data queries.
- If adding new features, keep the code simple and interactive.
- Document any new commands or conventions in this file.
