#!/usr/bin/env python3
"""
Comprehensive script to add missing units to BERVO ontology CSV file.
Handles ~1,130 entries missing units in Column 13 (has_units).
"""

import csv
import re
import sys
from pathlib import Path

ONTOLOGY_DIR = Path(__file__).resolve().parents[1]


def ontology_path(filename):
    return ONTOLOGY_DIR / filename

def extract_unit_from_definition(definition):
    """Extract unit patterns from definition text."""
    if not definition:
        return None
    
    # Patterns for equilibrium constants and other units
    unit_patterns = [
        r'mol\^\d+\s*m\^-\d+',      # mol^2 m^-6
        r'mol\s*m\^-\d+',            # mol m^-3
        r'm\^\d+\s*mol\^-\d+',       # m^3 mol^-1
        r'eqv\s*\(gC\)\^-1',         # eqv (gC)^-1
        r'umol\s+e-\s+umol-1\s+PAR', # umol e- umol-1 PAR
        r'umol\s+CO2',               # umol CO2
        r'Mg\s*m-1\s*s',             # Mg m-1 s
        r'g\s*solute\s*/g\s*gas',    # g solute /g gas
    ]
    
    for pattern in unit_patterns:
        match = re.search(pattern, definition)
        if match:
            return match.group(0).strip()
    return None

def infer_units_from_label(label, category, definition=""):
    """Infer units based on label keywords and category."""
    label_lower = label.lower()
    
    # Dimensionless indicators
    dimensionless_keywords = [
        "fraction", "ratio", "partition", "shape parameter",
        "relative", "parameter for calculating", "allocation parameter",
        "percent", "proportion"
    ]
    if any(kw in label_lower for kw in dimensionless_keywords):
        return "NONE"
    
    # Categorical/flag indicators  
    if "flag" in label_lower or "type" in label_lower or category == "Flag data type":
        return "NA"
    
    # Count/index variables
    if "number" in label_lower or "count" in label_lower or "index" in label_lower:
        return "NONE"
    
    # Temperature
    if "temperature" in label_lower:
        return "C"
    
    # Pressure/water potential
    if "pressure" in label_lower or "potential" in label_lower and "water" in label_lower:
        return "MPa"
    
    # Length/distance/radius
    if any(kw in label_lower for kw in ["length", "distance", "radius", "diameter", "depth", "height"]):
        return "m"
    
    # Area
    if "area" in label_lower:
        return "m2"
    
    # Diffusivity
    if "diffusivity" in label_lower:
        return "m2 h-1"
    
    # Solubility coefficient
    if "solubility coefficient" in label_lower:
        return "g solute /g gas"
    
    # Viscosity
    if "viscosity" in label_lower:
        return "Mg m-1 s"
    
    # Rate constant
    if "rate constant" in label_lower:
        return "h-1"
    
    # Concentration
    if "concentration" in label_lower:
        # Check if it's a gas or dissolved substance
        if any(gas in label_lower for gas in ["oxygen", "co2", "methane", "nitrogen", "ammonia"]):
            return "g m-3"
        return "mol m-3"
    
    # Content/Mass variables (often total across domain)
    if "content" in label_lower or ("total" in label_lower and "mass" in definition.lower()):
        return "g d-2"
    
    # Flux variables
    if "flux" in label_lower:
        # Energy flux
        if "heat" in label_lower or "energy" in label_lower:
            return "MJ d-2"
        # Mass flux
        return "g d-2 h-1"
    
    # Volume
    if "volume" in label_lower or ("water" in label_lower and "total" in label_lower):
        return "m3 d-2"
    
    # Uptake/emission/demand (rates)
    if any(kw in label_lower for kw in ["uptake", "emission", "demand", "respiration"]):
        return "g d-2 h-1"
    
    # Specific keywords by category
    if category == "Microbial parameters":
        if "km" in label_lower or "michaelis" in label_lower:
            return "g m-3"
        if "vmax" in label_lower or "maximum" in label_lower and "rate" in label_lower:
            return "g d-2 h-1"
    
    return None

def main():
    # Read the CSV file
    with open(ontology_path('bervo-src.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    header = rows[0]
    metadata = rows[1]
    data_rows = rows[2:]
    
    changes = []
    no_change_reasons = []
    
    for i, row in enumerate(data_rows):
        if len(row) < 29:  # Ensure row has enough columns
            # Pad with empty strings
            row.extend([''] * (29 - len(row)))
        
        bervo_id = row[0]
        label = row[1]
        category = row[2]
        ecosim_var = row[4]
        definition = row[6] if len(row) > 6 else ""
        current_units = row[12]
        
        # Skip if units already exist
        if current_units and current_units.strip():
            continue
        
        new_units = None
        reason = ""
        
        # Rule 1: Root Variable class
        if bervo_id == "BERVO:0000000":
            new_units = "NA"
            reason = "Root Variable class"
        
        # Rule 2: Parent category classes (no EcoSIM variable name)
        elif not ecosim_var or not ecosim_var.strip():
            if category in ["Chemical tracer parameters", "Concept"]:
                new_units = "NA"
                reason = f"Parent class in category: {category}"
            elif "diffusivity" in label.lower() and category == "Chemical tracer parameters":
                new_units = "NA"
                reason = "Parent diffusivity class"
        
        # Rule 3: Try extracting from definition (equilibrium constants, etc.)
        if not new_units:
            extracted = extract_unit_from_definition(definition)
            if extracted:
                new_units = extracted
                reason = "Extracted from definition"
        
        # Rule 4: Infer from label and category
        if not new_units:
            inferred = infer_units_from_label(label, category, definition)
            if inferred:
                new_units = inferred
                reason = f"Inferred from label/category"
        
        # Apply change
        if new_units:
            row[12] = new_units
            changes.append({
                'line': i + 3,  # +3 for header rows
                'id': bervo_id,
                'label': label[:60],
                'category': category[:30],
                'old': current_units or '(empty)',
                'new': new_units,
                'reason': reason
            })
        else:
            no_change_reasons.append({
                'line': i + 3,
                'id': bervo_id,
                'label': label[:60],
                'category': category[:30],
            })
    
    # Write updated CSV
    with open(ontology_path('bervo-src-with-units.csv'), 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(metadata)
        writer.writerows(data_rows)
    
    # Report
    print(f"{'='*80}")
    print(f"BERVO Units Assignment Report")
    print(f"{'='*80}")
    print(f"\nTotal changes made: {len(changes)}")
    print(f"Entries still without units: {len(no_change_reasons)}")
    print(f"\nOutput file: bervo-src-with-units.csv")
    
    # Show sample of changes
    print(f"\n{'='*80}")
    print(f"Sample of changes (first 50):")
    print(f"{'='*80}")
    for change in changes[:50]:
        print(f"Line {change['line']}: {change['id']} - {change['label']}")
        print(f"  Category: {change['category']}")
        print(f"  Units: '{change['old']}' → '{change['new']}' ({change['reason']})")
        print()
    
    # Show entries that still need manual review
    if no_change_reasons:
        print(f"\n{'='*80}")
        print(f"Entries still needing manual review ({len(no_change_reasons)}):")
        print(f"{'='*80}")
        for item in no_change_reasons[:30]:
            print(f"Line {item['line']}: {item['id']} - {item['label']}")
            print(f"  Category: {item['category']}")
        if len(no_change_reasons) > 30:
            print(f"\n... and {len(no_change_reasons) - 30} more")
    
    # Write detailed log
    with open(ontology_path('units_changes_log.txt'), 'w', encoding='utf-8') as f:
        f.write("BERVO Units Assignment Detailed Log\n")
        f.write("="*80 + "\n\n")
        f.write(f"Changes made: {len(changes)}\n\n")
        for change in changes:
            f.write(f"Line {change['line']}: {change['id']}\n")
            f.write(f"  Label: {change['label']}\n")
            f.write(f"  Category: {change['category']}\n")
            f.write(f"  Units: '{change['old']}' → '{change['new']}'\n")
            f.write(f"  Reason: {change['reason']}\n\n")
        
        if no_change_reasons:
            f.write("\n" + "="*80 + "\n")
            f.write(f"Entries needing manual review: {len(no_change_reasons)}\n\n")
            for item in no_change_reasons:
                f.write(f"Line {item['line']}: {item['id']}\n")
                f.write(f"  Label: {item['label']}\n")
                f.write(f"  Category: {item['category']}\n\n")
    
    print(f"\nDetailed log written to: units_changes_log.txt")
    print(f"\nPlease review the changes before replacing the original file.")

if __name__ == "__main__":
    main()
