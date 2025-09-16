def print_learnable_moves():
    while True:
        poke = input("Which pokemon are you looking for?\n").lower()
        is_variant = input("Is this a variant (e.g., alolan, galarian, etc.)? (y/n): ").lower()
        if is_variant == 'y':
            variant_name = input("Please specify the variant (e.g., alola, galar, hisui): ").lower()
            poke_full = f"{poke}-{variant_name}"
        else:
            poke_full = poke

        while True:
            method = input("How should the moves be learned? (level-up, machine, egg, or 'back' to change species): ").lower()
            if method == 'back':
                break
            try:
                poke_obj = pb.pokemon(poke_full)
                moves = set()
                for move in poke_obj.moves:
                    for detail in move.version_group_details:
                        if detail.move_learn_method.name == method:
                            moves.add(move.move.name)
                if moves:
                    print(f"Moves {poke_full} can learn by {method}:")
                    for m in sorted(moves):
                        print(m)
                else:
                    print(f"No moves found for {poke_full} by {method}.")
            except Exception as e:
                print(f"Could not retrieve moves for '{poke_full}'. Error: {e}")
        again = input("Would you like to look up moves for another species? (y/n): ").lower()
        if again != 'y':
            break
def print_evolution_chain():
    poke = input("Which pokemon are you looking for?\n").lower()
    is_variant = input("Is this a variant (e.g., alolan, galarian, etc.)? (y/n): ").lower()
    if is_variant == 'y':
        variant_name = input("Please specify the variant (e.g., alola, galar, hisui): ").lower()
        poke_full = f"{poke}-{variant_name}"
    else:
        poke_full = poke

    try:
        species = pb.pokemon_species(poke_full)
        if not hasattr(species, 'evolution_chain'):
            print(f"{poke_full} does not have an evolution chain.")
            return
        evo_chain = pb.evolution_chain(species.evolution_chain.id)
        chain = evo_chain.chain
        print("Evolution chain:")
        while chain:
            print(chain.species.name, end='')
            # Check for evolution details
            if chain.evolves_to:
                evo_details = chain.evolves_to[0].evolution_details
                if evo_details:
                    detail = evo_details[0]
                    evo_desc = []
                    # Collect all relevant evolution factors for this step
                    if detail.min_level:
                        evo_desc.append(f"Level {detail.min_level}")
                    if detail.item:
                        evo_desc.append(f"using {detail.item.name}")
                    if detail.held_item:
                        evo_desc.append(f"while holding {detail.held_item.name}")
                    if detail.trade_species:
                        evo_desc.append(f"traded for {detail.trade_species.name}")
                    if detail.known_move:
                        evo_desc.append(f"knowing move {detail.known_move.name}")
                    if detail.known_move_type:
                        evo_desc.append(f"knowing move of type {detail.known_move_type.name}")
                    if detail.location:
                        evo_desc.append(f"at {detail.location.name}")
                    if detail.time_of_day:
                        evo_desc.append(f"during {detail.time_of_day}")
                    if detail.gender is not None:
                        evo_desc.append(f"gender {detail.gender}")
                    if detail.relative_physical_stats is not None:
                        evo_desc.append(f"relative physical stats {detail.relative_physical_stats}")
                    if detail.needs_overworld_rain:
                        evo_desc.append("while raining")
                    if detail.party_species:
                        evo_desc.append(f"with {detail.party_species.name} in party")
                    if detail.party_type:
                        evo_desc.append(f"with type {detail.party_type.name} in party")
                    if detail.turn_upside_down:
                        evo_desc.append("while device is upside down")
                    if detail.min_happiness:
                        evo_desc.append(f"with happiness {detail.min_happiness}+")
                    if detail.min_beauty:
                        evo_desc.append(f"with beauty {detail.min_beauty}+")
                    if detail.min_affection:
                        evo_desc.append(f"with affection {detail.min_affection}+")
                    if evo_desc:
                        print(f" (evolves by: {', '.join(evo_desc)})", end='')
            print()
            if chain.evolves_to:
                chain = chain.evolves_to[0]
            else:
                break
    except Exception as e:
        print(f"Could not retrieve evolution chain for '{poke_full}'. Error: {e}")
import pokebase as pb
import requests

def show_type_effectiveness(poke_full):
    """Display the type effectiveness for a given Pokémon."""
    try:
        poke_obj = pb.pokemon(poke_full)
        if not hasattr(poke_obj, 'types'):
            print(f"No type data found for '{poke_full}'.")
            return
        types = [t.type.name for t in poke_obj.types]
        print(f"{poke_full.title()} typing: {', '.join(types)}")
        double_from, half_from, no_from = set(), set(), set()
        for t in types:
            t_obj = pb.type_(t)
            dr = t_obj.damage_relations
            double_from.update([d.name for d in dr.double_damage_from])
            half_from.update([d.name for d in dr.half_damage_from])
            no_from.update([d.name for d in dr.no_damage_from])
        print("Type effectiveness:")
        print(f"Super effective against {poke_full.title()}: {', '.join(double_from) or 'None'}")
        print(f"Not very effective against {poke_full.title()}: {', '.join(half_from) or 'None'}")
        print(f"No effect against {poke_full.title()}: {', '.join(no_from) or 'None'}")
    except Exception as e:
        print(f"Could not retrieve type effectiveness for '{poke_full}'. Error: {e}")
        
def find_pokemon_location(poke, game):
    """Find and print the location(s) of a Pokémon in a specific game version."""
    pokemon = pb.pokemon(poke)
    url = pokemon.location_area_encounters
    if not isinstance(url, str):
        print("Error: Could not retrieve a valid location URL for this Pokémon. (Debug: location_area_encounters is not a string)")
        print(f"Value: {url}")
        return
    response = requests.get(url)
    if response.status_code != 200:
        print("Could not retrieve location data.")
        return
    data = response.json()
    locations = []
    for entry in data:
        for version_detail in entry['version_details']:
            if version_detail['version']['name'] == game:
                locations.append(entry['location_area']['name'])
    if locations:
        print(f"{poke} can be found in: {', '.join(locations)} in {game}.")
    else:
        print(f"{poke} is not found in {game}.")  

def pokemon_basics():
    poke = input("Which pokemon are you looking for?\n").lower()
    is_variant = input("Is this a variant (e.g., alolan, galarian, etc.)? (y/n): ").lower()
    if is_variant == 'y':
        variant_name = input("Please specify the variant (e.g., alola, galar, hisui): ").lower()
        poke_full = f"{poke}-{variant_name}"
    else:
        poke_full = poke

    try:
        species = pb.pokemon_species(poke_full)
        poke_obj = pb.pokemon(poke_full)
    except Exception as e:
        print(f"Could not find data for '{poke_full}'. Error: {e}")
        return

    # Print type
    if hasattr(poke_obj, 'types'):
        types = [t.type.name for t in poke_obj.types]
        print(f"Type: {', '.join(types)}")
    else:
        print("Type: Not available")

    # Print height
    if hasattr(poke_obj, 'height'):
        print(f"Height: {poke_obj.height/10} meters")
    else:
        print("Height: Not available")

    # Print weight
    if hasattr(poke_obj, 'weight'):
        print(f"Weight: {poke_obj.weight/10} Kg")
    else:
        print("Weight: Not available")

    # Print dex entry (always in English)
    try:
        entry = next((entry.flavor_text for entry in species.flavor_text_entries if entry.language.name == "en"), None)
        if entry:
            print(f"Dex entry: {entry}")
        else:
            print("Dex entry: Not available")
    except AttributeError:
        print("Dex entry: Not available")

    # Print evolution last
    if not hasattr(species, 'evolution_chain'):
        print(f"{poke_full} does not evolve.")
        return
    try:
        evo_chain = pb.evolution_chain(species.evolution_chain.id)
        chain = evo_chain.chain
        while chain.species.name != poke_full and chain.evolves_to:
            chain = chain.evolves_to[0]
        if chain.evolves_to:
            next_evos = [evo.species.name for evo in chain.evolves_to]
            print(f"Next evolution(s): {', '.join(next_evos)}")
        else:
            print("This Pokémon does not evolve further.")
    except Exception:
        print(f"{poke_full} does not evolve.")

