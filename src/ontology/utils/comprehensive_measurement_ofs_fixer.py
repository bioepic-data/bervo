#!/usr/bin/env python3
"""
Comprehensive measurement_of assignment for BERVO ontology.
Assigns measurement_of based on label content analysis.
"""

import csv
import re
from pathlib import Path

ONTOLOGY_DIR = Path(__file__).resolve().parents[1]


def ontology_path(filename):
    return ONTOLOGY_DIR / filename

def get_bervo_labels():
    """Get all existing BERVO concept labels from the CSV."""
    labels = {}
    with open(ontology_path('bervo-src.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 2:  # skip headers
                continue
            if len(row) > 1:
                label = row[1].strip()
                if label:
                    labels[label.lower()] = label
    return labels

def normalize_measurement(measurement, bervo_labels):
    """Normalize measurement_of to match BERVO concept if available."""
    if not measurement:
        return measurement
    
    # Try exact match first
    if measurement.lower() in bervo_labels:
        return bervo_labels[measurement.lower()]
    
    return measurement

def extract_measurement_of(label, attribute):
    """Extract measurement_of from label and attribute."""
    label_lower = label.lower()
    
    # Skip certain types that generally don't have measurement_of
    if any(term in label_lower for term in [
        'equilibrium constant',
        'rate constant',
        'climate zone',
        'biome',
        'sequence',
        'genome',
        'binary',
        'initial number',
        'distance between',
        'media addition',
        'partitioning',
        'numerator',
        'denominator',
        'thermal adaptation',
        'plant maturity',
        'plant water stress',
        'self shading',
        'maturity',
        'phenological progress',
        'constraint',
        'harvest',
        'leaf area index',
        'secondary axes',
        'time step',
        'day',
        'altitude',
        'grain number',
        'coefficient'
    ]):
        return 'NA'
    
    # If attribute is NA, likely no measurement_of
    if attribute == 'NA':
        # But check for some exceptions where substance is still clear
        if any(term in label_lower for term in [
            'water vapor', 'salt', 'phosphorus', 'element', 'carbon', 'nitrogen'
        ]):
            pass  # Continue to normal processing
        else:
            return 'NA'
    
    # Compound patterns (chemical formulas, gases, etc.)
    compounds = {
        r'\bco2\b': 'Carbon dioxide',
        r'\bcarbon dioxide\b': 'Carbon dioxide',
        r'\bch4\b': 'Methane',
        r'\bmethane\b': 'Methane',
        r'\bn2o\b': 'Nitrous oxide',
        r'\bnitrous oxide\b': 'Nitrous oxide',
        r'\bno2\b': 'Nitrogen dioxide',
        r'\bnitrogen dioxide\b': 'Nitrogen dioxide',
        r'\bno3\b': 'Nitrate',
        r'\bnitrate': 'Nitrate',
        r'\bnh4\b': 'Ammonium',
        r'\bammonium': 'Ammonium',
        r'\bnh3\b': 'Ammonia',
        r'\bammonia\b': 'Ammonia',
        r'\burea\b': 'Urea',
        r'\bpo4\b': 'Phosphate',
        r'\bphosphate': 'Phosphate',
        r'\bwater vapor\b': 'Water vapor',
        r'\bh2o\b': 'Water',
    }
    
    for pattern, compound in compounds.items():
        if re.search(pattern, label_lower):
            return compound
    
    # Organic compounds - check before general elements
    organic = {
        r'\bdissolved organic carbon\b|\bdoc\b': 'Dissolved organic carbon',
        r'\bdissolved organic nitrogen\b|\bdon\b': 'Dissolved organic nitrogen',
        r'\bdissolved organic phosphorus\b|\bdop\b': 'Dissolved organic phosphorus',
        r'\bdissolved inorganic carbon\b|\bdic\b': 'Dissolved inorganic carbon',
        r'\bdissolved inorganic nitrogen\b|\bdin\b': 'Dissolved inorganic nitrogen',
        r'\bdissolved inorganic phosphorus\b|\bdip\b': 'Dissolved inorganic phosphorus',
        r'\bsoil organic matter\b|\bsom\b': 'Soil organic matter',
        r'\borganic matter\b': 'Organic matter',
        r'\borganic carbon\b': 'Organic carbon',
        r'\bcarboxyl\b': 'Carboxyl',
    }
    
    for pattern, org in organic.items():
        if re.search(pattern, label_lower):
            return org
    
    # Element patterns - after checking for compounds and organics
    elements = {
        r'\bcarbon\b': 'Carbon',
        r'\bnitrogen\b': 'Nitrogen',
        r'\bphosphorus\b': 'Phosphorus',
        r'\boxygen\b': 'Oxygen',
        r'\bsulfur\b': 'Sulfur',
        r'\bhydrogen\b': 'Hydrogen',
        r'\biron\b': 'Iron',
        r'\baluminum\b': 'Aluminum',
        r'\bcalcium\b': 'Calcium',
        r'\bmagnesium\b': 'Magnesium',
        r'\bpotassium\b': 'Potassium',
        r'\bsodium\b': 'Sodium',
        r'\bsilicon\b': 'Silicon',
        r'\bmanganese\b': 'Manganese',
    }
    
    for pattern, element in elements.items():
        if re.search(pattern, label_lower):
            return element
    
    # Biological materials - check after elements to avoid over-matching
    bio_materials = {
        r'\bleaf\b|\bleaves\b': 'Leaf',
        r'\broot\b|\broots\b': 'Root',
        r'\bbranch\b|\bbranches\b': 'Branch',
        r'\bstem\b|\bstems\b': 'Stem',
        r'\bwood\b': 'Wood',
        r'\bbiomass\b': 'Biomass',
        r'\blitter\b': 'Litter',
        r'\bpetiole\b': 'Petiole',
        r'\bnode\b|\bnodes\b': 'Node',
        r'\bgrain\b': 'Grain',
        r'\bseed\b': 'Seed',
        r'\bsheath\b': 'Sheath',
        r'\bstoma\b|\bstomata\b': 'Stoma',
        r'\bplant\b': 'Plant',
        r'\bmicrobes\b|\bmicrobial\b': 'Microbes',
        r'\bbacteria\b': 'Bacteria',
        r'\bsoil\b': 'Soil',
    }
    
    for pattern, material in bio_materials.items():
        if re.search(pattern, label_lower):
            return material
    
    # Physical substances
    substances = {
        r'\bwater\b': 'Water',
        r'\bair\b': 'Air',
        r'\benergy\b': 'Energy',
        r'\bheat\b': 'Heat',
        r'\bice\b': 'Ice',
        r'\bsnow\b': 'Snowpack',
        r'\bsalt\b': 'Salt',
        r'\bion\b|\bions\b': 'Ion',
        r'\bgas\b|\bgases\b': 'Gas',
        r'\bvapor\b': 'Vapor',
        r'\bsediment\b': 'Sediment',
    }
    
    for pattern, substance in substances.items():
        if re.search(pattern, label_lower):
            return substance
        if 'nitrogen to carbon' in label_lower or 'n:c' in label_lower or 'c:n' in label_lower:
            return 'Nitrogen to carbon ratio'
        elif 'phosphorus to carbon' in label_lower or 'p:c' in label_lower or 'c:p' in label_lower:
            return 'Phosphorous to carbon ratio'
        elif 'nitrogen to phosphorus' in label_lower or 'n:p' in label_lower or 'p:n' in label_lower:
            return 'Nitrogen to phosphorus ratio'
        else:
            return 'NA'
    
    # If attribute suggests a specific measurement_of
    if attribute in ['Respiration', 'Fixation', 'Photosynthesis']:
        # These typically measure carbon or CO2
        if 'carbon dioxide' in label_lower or 'co2' in label_lower:
            return 'Carbon dioxide'
        elif 'methane' in label_lower or 'ch4' in label_lower:
            return 'Methane'
        else:
            return 'Carbon'
    
    # Temperature measures heat/energy
    if attribute == 'Temperature':
        return 'Heat'
    
    # Flux, concentration, mass of something specific
    if attribute in ['Flux', 'Concentration', 'Mass', 'Amount', 'Content']:
        # Try to find what's being measured
        # Look for "of X" patterns
        of_match = re.search(r'\bof\s+([a-z][a-z\s]+?)(?:\s+in|\s+at|\s+from|\s+to|$)', label_lower)
        if of_match:
            substance = of_match.group(1).strip()
            # Check if this matches known substances
            substance_title = substance.title()
            return substance_title
    
    # Default to NA if nothing matches
    return 'NA'

def process_csv():
    """Process the CSV file and assign measurement_of values."""
    bervo_labels = get_bervo_labels()
    
    rows = []
    with open(ontology_path('bervo-src.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    
    changes = 0
    unchanged = 0
    measurement_counts = {}
    
    for i, row in enumerate(rows):
        if i < 2:  # skip headers
            continue
            
        # Ensure row has enough columns
        while len(row) < 29:
            row.append('')
        
        label = row[1].strip() if len(row) > 1 else ""
        attribute = row[14].strip() if len(row) > 14 else ""
        current_measurement = row[16].strip() if len(row) > 16 else ""
        
        # Only process if measurement_of is empty
        if not current_measurement:
            # Extract measurement_of
            new_measurement = extract_measurement_of(label, attribute)
            new_measurement = normalize_measurement(new_measurement, bervo_labels)
            
            row[16] = new_measurement
            changes += 1
            
            # Track assignments
            for m in new_measurement.split('|'):
                m = m.strip()
                if m and m != 'NA':
                    measurement_counts[m] = measurement_counts.get(m, 0) + 1
        else:
            unchanged += 1
    
    # Write output
    with open(ontology_path('bervo-src-with-measurement-ofs.csv'), 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"Completed! Changes: {changes}, Unchanged: {unchanged}")
    print(f"\nTop 30 measurement_of assignments:")
    for measurement, count in sorted(measurement_counts.items(), key=lambda x: x[1], reverse=True)[:30]:
        print(f"  {count:4d}  {measurement}")
    
    print(f"\nTotal unique measurements assigned: {len(measurement_counts)}")

if __name__ == '__main__':
    process_csv()
