#!/usr/bin/env python3
"""
Comprehensive Attributes Fixer for BERVO Ontology
Assigns appropriate BERVO:8 attribute concept terms to Column 15 (attributes)
"""

import csv
import re
from collections import defaultdict

# Valid attribute terms - these match BERVO:8 concept labels
# Based on actual BERVO:8 entries in the ontology
VALID_ATTRIBUTES = {
    'Equilibrium constant', 'Concentration', 'Flux', 'Uptake', 'Diffusivity',
    'Mass', 'Michaelis constant', 'Rate constant', 'Content', 'Heat flux',
    'Volume', 'Depth', 'Temperature', 'Area', 'Height', 'Count', 'Erosion',
    'Angle', 'Solubility', 'Activity', 'Density', 'Pressure',
    'Growth respiration efficiency', 'Specific oxidation rate', 'Rate',
    'Gibbs free energy change', 'Coefficient', 'Fixation',
    'Inhibition constant', 'Fraction',
    # Newly created attributes (Jan 8 2026)
    'Emission', 'Respiration', 'Resistance', 'Loss', 'Mineralization',
    'Absorptivity', 'Capacity', 'Amendment', 'Primary productivity',
    'Litterfall', 'Production', 'Transmission', 'Water flux'
}

def extract_attribute_from_label(label, category):
    """Extract attribute from the label using pattern matching"""
    if not label:
        return None
    
    label_lower = label.lower()
    
    # Direct attribute patterns (most specific first)
    
    # Equilibrium constants
    if 'equilibrium constant' in label_lower:
        return 'Equilibrium constant'
    
    # Michaelis constant
    if 'michaelis constant' in label_lower or 'half-saturation constant' in label_lower:
        return 'Michaelis constant'
    
    # Rate constant
    if 'rate constant' in label_lower:
        return 'Rate constant'
    
    # Inhibition constant
    if 'inhibition constant' in label_lower:
        return 'Inhibition constant'
    
    # Gibbs free energy
    if 'gibbs free energy' in label_lower:
        return 'Gibbs free energy change'
    
    # Heat flux
    if 'heat flux' in label_lower or label_lower.endswith(' heat'):
        return 'Heat flux'
    
    # Water flux
    if 'water flux' in label_lower:
        return 'Water flux'
    
    # Flux (general)
    if label_lower.endswith(' flux') or ' flux ' in label_lower:
        return 'Flux'
    
    # Concentration
    if 'concentration' in label_lower:
        return 'Concentration'
    
    # Diffusivity
    if 'diffusivity' in label_lower or 'diffusion coefficient' in label_lower:
        return 'Diffusivity'
    
    # Uptake
    if 'uptake' in label_lower or 'demand' in label_lower:
        return 'Uptake'
    
    # Mass
    if label_lower.startswith('mass ') or ' mass ' in label_lower or label_lower.endswith(' mass'):
        return 'Mass'
    
    # Content
    if 'content' in label_lower:
        return 'Content'
    
    # Temperature
    if 'temperature' in label_lower:
        return 'Temperature'
    
    # Pressure
    if 'pressure' in label_lower:
        return 'Pressure'
    
    # Depth
    if 'depth' in label_lower:
        return 'Depth'
    
    # Height
    if 'height' in label_lower:
        return 'Height'
    
    # Area
    if label_lower.startswith('area ') or ' area ' in label_lower or label_lower.endswith(' area'):
        return 'Area'
    
    # Volume
    if 'volume' in label_lower:
        return 'Volume'
    
    # Density
    if 'density' in label_lower:
        return 'Density'
    
    # Count
    if 'count' in label_lower or 'number of' in label_lower:
        return 'Count'
    
    # Fraction
    if 'fraction' in label_lower or 'proportion' in label_lower:
        return 'Fraction'
    
    # Rate
    if label_lower.startswith('rate ') or ' rate ' in label_lower or label_lower.endswith(' rate'):
        return 'Rate'
    
    # Coefficient
    if 'coefficient' in label_lower:
        return 'Coefficient'
    
    # Angle
    if 'angle' in label_lower:
        return 'Angle'
    
    # Solubility
    if 'solubility' in label_lower:
        return 'Solubility'
    
    # Activity
    if 'activity' in label_lower:
        return 'Activity'
    
    # Erosion
    if 'erosion' in label_lower:
        return 'Erosion'
    
    # Emission
    if 'emission' in label_lower:
        return 'Emission'
    
    # Respiration
    if 'respiration' in label_lower:
        return 'Respiration'
    
    # Primary productivity
    if 'primary productivity' in label_lower or 'gross primary' in label_lower:
        return 'Primary productivity'
    
    # Production
    if 'production' in label_lower:
        return 'Production'
    
    # Fixation
    if 'fixation' in label_lower:
        return 'Fixation'
    
    # Mineralization
    if 'mineralization' in label_lower or 'immobilization' in label_lower:
        return 'Mineralization'
    
    # Litterfall
    if 'litterfall' in label_lower:
        return 'Litterfall'
    
    # Resistance
    if 'resistance' in label_lower:
        return 'Resistance'
    
    # Loss
    if label_lower.startswith('loss ') or ' loss' in label_lower:
        return 'Loss'
    
    # Absorptivity
    if 'absorptivity' in label_lower or 'absorptance' in label_lower:
        return 'Absorptivity'
    
    # Transmission
    if 'transmission' in label_lower or 'transmittance' in label_lower:
        return 'Transmission'
    
    # Capacity
    if 'capacity' in label_lower:
        return 'Capacity'
    
    # Amendment
    if 'amendment' in label_lower:
        return 'Amendment'
    
    # Growth respiration efficiency
    if 'growth respiration efficiency' in label_lower:
        return 'Growth respiration efficiency'
    
    # Specific oxidation rate
    if 'specific oxidation rate' in label_lower:
        return 'Specific oxidation rate'
    
    return None

def infer_attribute_from_category(category, label):
    """Infer attribute based on category"""
    if not category:
        return None
    
    category_lower = category.lower()
    
    # Constants don't usually have attributes, they ARE the attribute in a sense
    if 'constant' in category_lower:
        return None
    
    # Flux variables
    if 'flux' in category_lower:
        if 'heat' in label.lower():
            return 'Heat flux'
        return 'Flux'
    
    return None

def should_have_attribute(row):
    """Determine if an entry should have an attribute"""
    bervo_id = row[0]
    label = row[1]
    category = row[2]
    
    # Root class doesn't need attribute
    if bervo_id == 'BERVO:0000000':
        return False
    
    # BERVO:8 concepts and properties don't need attributes
    if bervo_id.startswith('BERVO:8') or bervo_id.startswith('BERVO:has_') or bervo_id.startswith('BERVO:measured_') or bervo_id.startswith('BERVO:measurement_') or bervo_id.startswith('BERVO:Context') or bervo_id.startswith('BERVO:Qualifier') or bervo_id.startswith('BERVO:Attribute') or bervo_id.startswith('BERVO:involves_'):
        return False
    
    # Generic category parent classes might not need attributes
    if category and label == category:
        return False
    
    return True

def assign_attributes(input_file, output_file):
    """Main function to assign attributes"""
    
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
        current_attr = row[14] if len(row) > 14 else ''
        
        # Check if already has a valid attribute
        if current_attr and current_attr not in ['', 'NA']:
            # Check if all parts are valid attributes
            parts = current_attr.split('|')
            all_valid = all(part.strip() in VALID_ATTRIBUTES for part in parts)
            
            if all_valid:
                # Keep existing valid attributes
                stats['already_valid'] += 1
                continue
            else:
                # Invalid data - needs fixing
                stats['had_invalid_data'] += 1
        
        # Try to assign attribute
        new_attr = extract_attribute_from_label(label, category)
        
        if not new_attr:
            new_attr = infer_attribute_from_category(category, label)
        
        if not new_attr and should_have_attribute(row):
            # Default to NA if no attribute applies
            new_attr = 'NA'
        elif not new_attr:
            new_attr = 'NA'
        
        # Update row
        if current_attr != new_attr:
            old_val = current_attr if current_attr else '(empty)'
            row[14] = new_attr
            changes.append({
                'id': bervo_id,
                'label': label,
                'old': old_val,
                'new': new_attr
            })
            stats['changed'] += 1
            
            # Track attribute types
            if new_attr != 'NA':
                for attr in new_attr.split('|'):
                    stats[f'attribute_{attr}'] += 1
        else:
            stats['unchanged'] += 1
    
    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(rows)
    
    return changes, stats

def main():
    input_file = 'bervo-src.csv'
    output_file = 'bervo-src-with-attributes.csv'
    log_file = 'attributes_changes_log.txt'
    
    print("Starting attribute assignment...")
    changes, stats = assign_attributes(input_file, output_file)
    
    # Write changes log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("BERVO Attributes Assignment Log\n")
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
    print(f"Output written to: {output_file}")
    print(f"Log written to: {log_file}")
    
    # Show statistics
    print("\nAttribute Distribution:")
    for key, value in sorted(stats.items()):
        if key.startswith('attribute_'):
            print(f"  {key.replace('attribute_', '')}: {value}")

if __name__ == '__main__':
    main()
