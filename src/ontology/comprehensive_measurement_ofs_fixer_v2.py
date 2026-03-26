#!/usr/bin/env python3
"""
Comprehensive measurement_of assignment for BERVO ontology.
Assigns measurement_of based on label content analysis.
"""

import csv
import re

def get_bervo_labels():
    """Get all existing BERVO concept labels from the CSV."""
    labels = {}
    with open('bervo-src.csv', 'r') as f:
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
    skip_terms = [
        'equilibrium constant', 'rate constant', 'climate zone', 'biome',
        'sequence', 'genome', 'binary', 'initial number', 'distance between',
        'media addition', 'numerator', 'denominator', 'thermal adaptation',
        'plant maturity', 'plant water stress', 'self shading', 'maturity',
        'phenological progress', 'constraint', 'harvest index', 'leaf area index',
        'secondary axes', 'time step', 'day of', 'altitude', 'grain number',
        'coefficient', 'index', 'counter', 'flag', 'partitioning of'
    ]
    
    for term in skip_terms:
        if term in label_lower:
            return 'NA'
    
    # If attribute is NA, usually no measurement_of unless substance is obvious
    if attribute == 'NA':
        # Check for some clear substances even without attribute
        obvious_substances = [
            'water vapor', 'salt', 'phosphorus', 'nitrogen', 'element',
            'co2', 'carbon dioxide', 'methane', 'ammonia', 'ammonium',
            'nitrate', 'phosphate'
        ]
        has_obvious = any(term in label_lower for term in obvious_substances)
        if not has_obvious:
            return 'NA'
    
    # Ratios measure the ratio itself, not individual elements
    if 'ratio' in label_lower or ':' in label_lower:
        ratio_patterns = {
            r'nitrogen\s+to\s+carbon|n\s*:\s*c|c\s*:\s*n|carbon\s+to\s+nitrogen': 'Nitrogen to carbon ratio',
            r'phosphorus\s+to\s+carbon|p\s*:\s*c|c\s*:\s*p|carbon\s+to\s+phosphorus': 'Phosphorous to carbon ratio',
            r'nitrogen\s+to\s+phosphorus|n\s*:\s*p|p\s*:\s*n|phosphorus\s+to\s+nitrogen': 'Nitrogen to phosphorus ratio',
        }
        for pattern, ratio_name in ratio_patterns.items():
            if re.search(pattern, label_lower):
                return ratio_name
        # Other ratios don't have measurement_of
        if 'ratio' in label_lower:
            return 'NA'
    
    # Compound patterns (chemical formulas, gases, etc.) - check first as most specific
    compounds = {
        r'\bco2\b|carbon\s+dioxide': 'Carbon dioxide',
        r'\bch4\b|\bmethane\b': 'Methane',
        r'\bn2o\b|nitrous\s+oxide': 'Nitrous oxide',
        r'\bno2\b|nitrogen\s+dioxide': 'Nitrogen dioxide',
        r'\bno3\b|nitrate': 'Nitrate',
        r'\bnh4\b|ammonium': 'Ammonium',
        r'\bnh3\b|\bammonia\b': 'Ammonia',
        r'\burea\b': 'Urea',
        r'\bpo4\b|phosphate': 'Phosphate',
        r'water\s+vapor': 'Water vapor',
        r'\bh2o\b': 'Water',
    }
    
    for pattern, compound in compounds.items():
        if re.search(pattern, label_lower):
            return compound
    
    # Organic compounds - check before general elements to avoid over-matching
    organic_patterns = {
        r'dissolved\s+organic\s+carbon|\bdoc\b': 'Dissolved organic carbon',
        r'dissolved\s+organic\s+nitrogen|\bdon\b': 'Dissolved organic nitrogen',
        r'dissolved\s+organic\s+phosphorus|\bdop\b': 'Dissolved organic phosphorus',
        r'dissolved\s+inorganic\s+carbon|\bdic\b': 'Dissolved inorganic carbon',
        r'dissolved\s+inorganic\s+nitrogen|\bdin\b': 'Dissolved inorganic nitrogen',
        r'dissolved\s+inorganic\s+phosphorus|\bdip\b': 'Dissolved inorganic phosphorus',
        r'soil\s+organic\s+matter|\bsom\b': 'Soil organic matter',
        r'organic\s+matter': 'Organic matter',
        r'organic\s+carbon': 'Organic carbon',
        r'\bcarboxyl\b': 'Carboxyl',
    }
    
    for pattern, org in organic_patterns.items():
        if re.search(pattern, label_lower):
            return org
    
    # Element patterns - after checking for compounds and organics
    element_patterns = {
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
    
    for pattern, element in element_patterns.items():
        if re.search(pattern, label_lower):
            return element
    
    # Biological materials - check after elements to avoid over-matching
    bio_patterns = {
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
    
    for pattern, material in bio_patterns.items():
        if re.search(pattern, label_lower):
            return material
    
    # Physical substances
    substance_patterns = {
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
    
    for pattern, substance in substance_patterns.items():
        if re.search(pattern, label_lower):
            return substance
    
    # If attribute suggests a specific measurement_of
    if attribute in ['Respiration', 'Fixation', 'Photosynthesis']:
        # These typically measure carbon or CO2
        return 'Carbon'
    
    # Temperature measures heat/energy
    if attribute == 'Temperature':
        return 'Heat'
    
    # Flux, concentration, mass, etc. without specific substance mentioned
    if attribute in ['Flux', 'Concentration', 'Mass', 'Amount', 'Content', 'Volume']:
        # Try to find what's being measured from "of X" patterns
        of_match = re.search(r'\bof\s+([a-z][a-z\s]+?)(?:\s+in|\s+at|\s+from|\s+to|\s+during|$)', label_lower)
        if of_match:
            substance = of_match.group(1).strip()
            # Return as title case
            return substance.title()
    
    # Default to NA if nothing matches
    return 'NA'

def process_csv():
    """Process the CSV file and assign measurement_of values."""
    bervo_labels = get_bervo_labels()
    
    rows = []
    with open('bervo-src.csv', 'r') as f:
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
    with open('bervo-src-with-measurement-ofs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"Completed! Changes: {changes}, Unchanged: {unchanged}")
    print(f"\nTop 40 measurement_of assignments:")
    for measurement, count in sorted(measurement_counts.items(), key=lambda x: x[1], reverse=True)[:40]:
        print(f"  {count:4d}  {measurement}")
    
    print(f"\nTotal unique measurements assigned: {len(measurement_counts)}")

if __name__ == '__main__':
    process_csv()
