import json
import os
from collections import defaultdict
import argparse

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def find_verified_entries(videototext_data):
    verified_entries = []
    seen = defaultdict(list)
    
    for entry in videototext_data:
        key = (entry['kopfnummer'], entry['pferdename'], entry['reitername'])
        seen[key].append(entry['timestamp'])

    for key, timestamps in seen.items():
        if len(timestamps) >= 2 and timestamps[1] - timestamps[0] <= 3:
            verified_entries.append({
                "kopfnummer": key[0],
                "pferdename": key[1],
                "reitername": key[2],
                "timestamp": timestamps[0]
            })

    return verified_entries

def match_startlist(verified_entries, startlist_data):
    matched_entries = []
    used_start_numbers = set()
    entries = startlist_data['startlist']['entries']
    
    for verified in verified_entries:
        for startlist_entry in entries:
            if (verified['kopfnummer'] == startlist_entry['headnr'] and
                verified['pferdename'] == startlist_entry['sport_name'] and
                verified['reitername'] == startlist_entry['ridername']):
                if startlist_entry['startnr'] not in used_start_numbers:
                    matched_entry = {
                        "sport_name": startlist_entry['sport_name'],
                        "breed_name": startlist_entry['breed_name'],
                        "horse_iso": startlist_entry['horse_iso'],
                        "year_of_birth": startlist_entry['year_of_birth'],
                        "color_en": startlist_entry['color_en'],
                        "gender_en": startlist_entry['gender_en'],
                        "breeder": startlist_entry['breeder'],
                        "fei": startlist_entry['fei'],
                        "name_father": startlist_entry['name_father'],
                        "iso_father": startlist_entry['iso_father'],
                        "name_mother": startlist_entry['name_mother'],
                        "iso_mother": startlist_entry['iso_mother'],
                        "ridername": startlist_entry['ridername'],
                        "team": startlist_entry['team'],
                        "start_time": startlist_entry['start_time'],
                        "startnr": startlist_entry['startnr'],
                        "headnr": startlist_entry['headnr'],
                        "live_chapter": [
                            {"second": verified['timestamp']},
                            {"second": verified['timestamp']}
                        ]
                    }
                    matched_entries.append(matched_entry)
                    used_start_numbers.add(startlist_entry['startnr'])
                break
    return matched_entries

def save_cockpit_export(matched_entries, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(matched_entries, file, ensure_ascii=False, indent=4)

def main(videototext_path, startlist_path, output_path):
    try:
        videototext_data = load_json(videototext_path)
        startlist_data = load_json(startlist_path)

        verified_entries = find_verified_entries(videototext_data)
        matched_entries = match_startlist(verified_entries, startlist_data)
        save_cockpit_export(matched_entries, output_path)

        print(f"Cockpit export saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Cockpit Export")
    parser.add_argument(
        "--videototext", 
        type=str, 
        required=True, 
        help="Path to the videototext.json file"
    )
    parser.add_argument(
        "--startlist", 
        type=str, 
        required=True, 
        help="Path to the startlist.json file"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        required=True, 
        help="Path to save the cockpitexport.json file"
    )
    args = parser.parse_args()

    main(args.videototext, args.startlist, args.output)