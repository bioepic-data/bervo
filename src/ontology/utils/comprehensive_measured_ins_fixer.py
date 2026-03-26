#!/usr/bin/env python3
"""
Comprehensive Measured_ins Fixer for BERVO Ontology
Assigns appropriate BERVO:8 concept terms to Column 16 (measured_ins)
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

ONTOLOGY_DIR = Path(__file__).resolve().parents[1]


def ontology_path(filename):
    return ONTOLOGY_DIR / filename

# Valid measured_in terms - these match BERVO:8 concept labels
VALID_MEASURED_INS = {
    'Soil', 'Root', 'Water', 'Canopy', 'Plant', 'Leaf', 'Air', 'Snow',
    'Snowpack', 'Microbes', 'Micropore', 'Root layer', 'Macropore',
    'Surface litter', 'Surface', 'Atmosphere', 'Subsurface', 'Litter',
    'Branch', 'Nodule', 'Ground surface', 'Stoma', 'Sheath', 'Grain',
    'Soil surface', 'Stalk', 'Runoff', 'Reserve', 'Husk', 'Ear',
    'Surface runoff', 'Solution', 'Fertilizer', 'Bundle sheath', 'Mesophyll',
    'Seed', 'Zone', 'Dead standing tree', 'Node', 'Aluminum hydroxide',
    'Layer', 'Landscape', 'Grid cell', 'Field', 'Growth', 'Internode',
    'Temperature', 'Soil water', 'Harvest', 'Soil non-band', 'Topsoil',
    'Soil band', 'Erosion band', 'Sediment', 'Ice', 'Day', 'Stem',
    'Water table', 'Surface water',
    # Newly created (Jan 8 2026)
    'Shoot', 'Litter layer'
}

def clean_measured_in(value):
    """Clean up problematic measured_in values"""
    if not value or value == 'NA':
        return value
    
    # Fix known data quality issues
    fixes = {
        'Canopy Shoot': 'Canopy|Shoot',
        'Litter (plant)': 'Litter',
        'Soil Micropore': 'Micropore',
        'Soil band, micropore': 'Micropore',
        'Soil Non-band, micropore': 'Micropore',
        'Surface layer': 'Surface',
    }
    
    parts = value.split('|')
    cleaned_parts = []
    for part in parts:
        part = part.strip()
        if part in fixes:
            # If fix has pipe, split and add all parts
            if '|' in fixes[part]:
                cleaned_parts.extend(fixes[part].split('|'))
            else:
                cleaned_parts.append(fixes[part])
        else:
            cleaned_parts.append(part)
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for p in cleaned_parts:
        if p and p not in seen:
            seen.add(p)
            result.append(p)
    
    return '|'.join(result) if result else 'NA'

def extract_measured_in_from_label(label, category, attribute):
    """Extract measured_in from the label using pattern matching"""
    if not label:
        return None
    
    label_lower = label.lower()
    
    # Direct patterns (most specific first)
    
    # "in [medium]" patterns
    if ' in soil' in label_lower or label_lower.endswith(' soil') or label_lower.startswith('soil '):
        if 'micropore' in label_lower:
            return 'Micropore'
        elif 'macropore' in label_lower:
            return 'Macropore'
        elif 'root layer' in label_lower or 'rhizosphere' in label_lower:
            return 'Root layer'
        return 'Soil'
    
    if ' in water' in label_lower or label_lower.endswith(' water'):
        return 'Water'
    
    if ' in air' in label_lower or label_lower.endswith(' air'):
        return 'Air'
    
    if ' in atmosphere' in label_lower:
        return 'Atmosphere'
    
    if ' in plant' in label_lower or label_lower.endswith(' plant'):
        return 'Plant'
    
    if ' in leaf' in label_lower or ' in leaves' in label_lower or 'foliar' in label_lower:
        return 'Leaf'
    
    if ' in root' in label_lower or label_lower.endswith(' root'):
        return 'Root'
    
    if ' in canopy' in label_lower or label_lower.startswith('canopy '):
        return 'Canopy'
    
    if ' in litter' in label_lower or label_lower.startswith('litter '):
        if 'layer' in label_lower:
            return 'Litter layer'
        return 'Litter'
    
    if ' in snow' in label_lower or label_lower.startswith('snow '):
        if 'pack' in label_lower:
            return 'Snowpack'
        return 'Snow'
    
    # Context-based patterns
    if 'microbial' in label_lower or 'microb' in label_lower:
        if 'soil' in label_lower:
            return 'Soil|Microbes'
        return 'Microbes'
    
    if 'heterotrophic' in label_lower:
        return 'Soil|Microbes'
    
    if 'autotrophic' in label_lower or 'photosynthes' in label_lower:
        return 'Plant'
    
    # Attribute-based inference
    if attribute:
        attr_lower = attribute.lower()
        
        if attr_lower == 'diffusivity':
            if 'soil' in label_lower:
                return 'Soil'
            elif 'water' in label_lower or 'aqueous' in label_lower:
                return 'Water'
            elif 'air' in label_lower or 'gas' in label_lower:
                return 'Air'
        
        if attr_lower == 'respiration':
            if 'plant' in label_lower or 'autotrophic' in label_lower:
                return 'Plant'
            elif 'soil' in label_lower or 'heterotrophic' in label_lower:
                return 'Soil|Microbes'
        
        if attr_lower in ['fixation', 'primary productivity']:
            return 'Plant'
        
        if attr_lower == 'mineralization':
            return 'Soil|Microbes'
    
    # Category-based patterns
    if category:
        cat_lower = category.lower()
        
        if 'soil' in cat_lower:
            return 'Soil'
        if 'canopy' in cat_lower:
            return 'Canopy'
        if 'root' in cat_lower:
            return 'Root'
        if 'litter' in cat_lower:
            return 'Litter'
    
    return None

def should_have_measured_in(row):
    """Determine if an entry should have a measured_in"""
    bervo_id = row[0]
    label = row[1]
    category = row[2]
    
    # Root class doesn't need measured_in
    if bervo_id == 'BERVO:0000000':
        return False
    
    # BERVO:8 concepts and properties don't need measured_in
    if bervo_id.startswith('BERVO:8') or bervo_id.startswith('BERVO:has_') or bervo_id.startswith('BERVO:measured_') or bervo_id.startswith('BERVO:measurement_') or bervo_id.startswith('BERVO:Context') or bervo_id.startswith('BERVO:Qualifier') or bervo_id.startswith('BERVO:Attribute') or bervo_id.startswith('BERVO:involves_'):
        return False
    
    # Generic parent classes might not need measured_in
    if category and label == category:
        return False
    
    # Constants and equilibrium constants don't need measured_in
    if category and 'constant' in category.lower():
        return False
    
    return True

def assign_measured_ins(input_file, output_file):
    """Main function to assign measured_ins"""
    
    changes = []
    stats = defaultdict(int)
    
    with open(input_file, 'r', encoding='utf-8') as f_in:
        reader = csv.reader(f_in)
        rows = list(reader)
    
    # Process each row (skip headers)
    for i, row in enumerate(rows):
        if i < 2:  # Skip header rows
            continue
        
        bervo_id = row[0]
        label = row[1]
        category = row[2]
        attribute = row[14] if len(row) > 14 else ''
        current_measured = row[15] if len(row) > 15 else ''
        
        # Clean existing measured_in
        if current_measured and current_measured not in ['', 'NA']:
            cleaned = clean_measured_in(current_measured)
            if cleaned != current_measured:
                stats['cleaned'] += 1
                current_measured = cleaned
                row[15] = cleaned
        
        # Check if already has a valid measured_in
        if current_measured and current_measured not in ['', 'NA']:
            # Check if all parts are valid
            parts = current_measured.split('|')
            all_valid = all(part.strip() in VALID_MEASURED_INS for part in parts)
            
            if all_valid:
                # Keep existing valid measured_ins
                stats['already_valid'] += 1
                continue
            else:
                # Invalid data - needs fixing
                stats['had_invalid_data'] += 1
        
        # Try to assign measured_in
        new_measured = extract_measured_in_from_label(label, category, attribute)
        
        if not new_measured and should_have_measured_in(row):
            # Default to NA if no measured_in applies
            new_measured = 'NA'
        elif not new_measured:
            new_measured = 'NA'
        
        # Update row
        if current_measured != new_measured:
            old_val = current_measured if current_measured else '(empty)'
            row[15] = new_measured
            changes.append({
                'id': bervo_id,
                'label': label,
                'old': old_val,
                'new': new_measured
            })
            stats['changed'] += 1
            
            # Track measured_in types
            if new_measured != 'NA':
                for measured in new_measured.split('|'):
                    stats[f'measured_in_{measured.strip()}'] += 1
        else:
            stats['unchanged'] += 1
    
    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(rows)
    
    return changes, stats

def main():
    input_file = ontology_path('bervo-src.csv')
    output_file = ontology_path('bervo-src-with-measured-ins.csv')
    log_file = ontology_path('measured_ins_changes_log.txt')
    
    print("Starting measured_ins assignment...")
    changes, stats = assign_measured_ins(input_file, output_file)
    
    # Write changes log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("BERVO Measured_ins Assignment Log\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total changes: {len(changes)}\n\n")
        
        for change in changes[:100]:  # Show first 100 changes
            f.write(f"ID: {change['id']}\n")
            f.write(f"Label: {change['label']}\n")
            f.write(f"Old: {change['old']}\n")
            f.write(f"New: {change['new']}\n")
            f.write("-" * 80 + "\n")
        
        if len(changes) > 100:
            f.write(f"\n... and {len(changes) - 100} more changes\n")
        
        f.write("\n\nStatistics:\n")
        f.write("=" * 80 + "\n")
        for key, value in sorted(stats.items()):
            f.write(f"{key}: {value}\n")
    
    print(f"\nCompleted! Changes: {stats['changed']}, Unchanged: {stats['unchanged']}")
    if stats.get('cleaned', 0) > 0:
        print(f"Cleaned: {stats['cleaned']}")
    print(f"Output written to: {output_file}")
    print(f"Log written to: {log_file}")
    
    # Show statistics
    print("\nMeasured_in Distribution (top 20):")
    measured_items = [(k.replace('measured_in_', ''), v) for k, v in stats.items() if k.startswith('measured_in_')]
    for measured, count in sorted(measured_items, key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {measured}: {count}")

if __name__ == '__main__':
    main()
