#!/usr/bin/env python3
"""
Comprehensive Qualifiers Fixer for BERVO Ontology
Assigns appropriate BERVO:8 concept terms to Column 14 (qualifiers)
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

ONTOLOGY_DIR = Path(__file__).resolve().parents[1]


def ontology_path(filename):
    return ONTOLOGY_DIR / filename

# Valid qualifier terms (text, not IDs) - these match BERVO:8 concept labels
# Based on actual BERVO:8 entries in the ontology
VALID_QUALIFIERS = {
    'Total',       # BERVO:8000254
    'Net',         # BERVO:8000262
    'Maximum',     # BERVO:8000253
    'Minimum',     # BERVO:8000252
    'Initial',     # BERVO:8000265
    'Final',       # BERVO:8000266
    'Mean',        # BERVO:8000259
    'Daily',       # BERVO:8000282
    'Hourly',      # BERVO:8000283
    'Monthly',     # BERVO:8000280
    'Yearly',      # BERVO:8000279
    'Aqueous',     # BERVO:8000196
    'Critical',    # BERVO:8000005
    'Net exchange',  # BERVO:8000041
    'Standard ambient temperature',  # BERVO:8000249
    'Standard deviation',  # BERVO:8000362
    'Standard error',      # BERVO:8000363
    # Newly created qualifiers (Jan 8 2026)
    'Current',     # BERVO:8000532
    'Previous',    # BERVO:8000533
    'Cumulative',  # BERVO:8000534
    'Logarithmic', # BERVO:8000535
    'Hydrological',# BERVO:8000536
    'Negative',    # BERVO:8000537
}

def extract_qualifier_from_label(label):
    """Extract qualifier from the label using pattern matching"""
    if not label:
        return None
    
    label_lower = label.lower()
    
    # Check for multiple qualifiers in order of specificity
    qualifiers = []
    
    # Time-based qualifiers
    if 'cumulative' in label_lower or label_lower.startswith('cumulative '):
        qualifiers.append('Total')
    if 'daily' in label_lower:
        qualifiers.append('Daily')
    if 'hourly' in label_lower:
        qualifiers.append('Hourly')
    if 'monthly' in label_lower:
        qualifiers.append('Monthly')
    if 'yearly' in label_lower or 'annual' in label_lower:
        qualifiers.append('Yearly')
    
    # State qualifiers
    if 'current' in label_lower and 'current' in label:
        qualifiers.append('Current')
    if 'previous' in label_lower or 'previous time step' in label_lower:
        qualifiers.append('Previous')
    if 'initial' in label_lower:
        qualifiers.append('Initial')
    if 'final' in label_lower:
        qualifiers.append('Final')
    
    # Statistical qualifiers
    if re.search(r'\bmaximum\b', label_lower) or label_lower.startswith('maximum ') or label_lower.endswith(' maximum'):
        qualifiers.append('Maximum')
    if re.search(r'\bminimum\b', label_lower) or label_lower.startswith('minimum ') or label_lower.endswith(' minimum'):
        qualifiers.append('Minimum')
    if 'mean' in label_lower or 'average' in label_lower:
        qualifiers.append('Mean')
    if 'standard deviation' in label_lower or 'std dev' in label_lower:
        qualifiers.append('Standard deviation')
    if 'standard error' in label_lower:
        qualifiers.append('Standard error')
    
    # Net/Total qualifiers (check these after time-based to avoid conflicts)
    if label_lower.startswith('total ') or ' total ' in label_lower or label_lower.endswith(' total'):
        if 'Total' not in qualifiers:
            qualifiers.append('Total')
    if label_lower.startswith('net ') or ' net ' in label_lower:
        qualifiers.append('Net')
    
    # Phase qualifiers
    if 'aqueous' in label_lower:
        qualifiers.append('Aqueous')
    if 'gaseous' in label_lower or 'gas phase' in label_lower:
        qualifiers.append('Gaseous')
    
    # Special qualifiers
    if 'critical' in label_lower:
        qualifiers.append('Critical')
    
    return '|'.join(qualifiers) if qualifiers else None

def infer_qualifier_from_category(category, label):
    """Infer qualifier based on category and label patterns"""
    if not category or not label:
        return None
    
    category_lower = category.lower()
    label_lower = label.lower()
    
    # Constants and parameters generally don't need qualifiers
    if 'constant' in category_lower or 'parameter' in category_lower:
        # Unless they're specifically time-based or statistical
        if any(word in label_lower for word in ['maximum', 'minimum', 'mean', 'initial', 'final']):
            return extract_qualifier_from_label(label)
        return None
    
    # Fluxes often have Net or Total qualifiers
    if 'flux' in category_lower:
        if 'net' in label_lower:
            return 'Net'
    
    return None

def should_have_qualifier(row):
    """Determine if an entry should have a qualifier"""
    bervo_id = row[0]
    label = row[1]
    category = row[2]
    
    # Root class doesn't need qualifier
    if bervo_id == 'BERVO:0000000':
        return False
    
    # Abstract parent classes might not need qualifiers
    qualifier_words = ['current', 'previous', 'maximum', 'minimum', 'total', 'net', 'cumulative', 'mean', 
                       'initial', 'final', 'daily', 'hourly', 'monthly', 'yearly', 'critical', 'aqueous', 'gaseous']
    if category and 'variable' in category.lower() and not any(word in label.lower() for word in qualifier_words):
        # Generic category classes don't need qualifiers
        if label == category:
            return False
    
    return True

def assign_qualifiers(input_file, output_file):
    """Main function to assign qualifiers"""
    
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
        current_qualifier = row[13] if len(row) > 13 else ''
        
        # Check if already has a valid qualifier
        if current_qualifier and current_qualifier not in ['', 'NA']:
            # Check if all parts are valid qualifiers
            parts = current_qualifier.split('|')
            all_valid = all(part.strip() in VALID_QUALIFIERS for part in parts)
            
            if all_valid:
                # Keep existing valid qualifiers
                stats['already_valid'] += 1
                continue
            else:
                # Invalid data (units, "Class", etc.) - needs fixing
                stats['had_invalid_data'] += 1
        
        # Try to assign qualifier
        new_qualifier = extract_qualifier_from_label(label)
        
        if not new_qualifier:
            new_qualifier = infer_qualifier_from_category(category, label)
        
        if not new_qualifier and should_have_qualifier(row):
            # Default to NA if no qualifier applies
            new_qualifier = 'NA'
        elif not new_qualifier:
            new_qualifier = 'NA'
        
        # Update row
        if current_qualifier != new_qualifier:
            old_val = current_qualifier if current_qualifier else '(empty)'
            row[13] = new_qualifier
            changes.append({
                'id': bervo_id,
                'label': label,
                'old': old_val,
                'new': new_qualifier
            })
            stats['changed'] += 1
            
            # Track qualifier types
            if new_qualifier != 'NA':
                for qual in new_qualifier.split('|'):
                    stats[f'qualifier_{qual}'] += 1
        else:
            stats['unchanged'] += 1
    
    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(rows)
    
    return changes, stats

def main():
    input_file = ontology_path('bervo-src.csv')
    output_file = ontology_path('bervo-src-with-qualifiers.csv')
    log_file = ontology_path('qualifiers_changes_log.txt')
    
    print("Starting qualifier assignment...")
    changes, stats = assign_qualifiers(input_file, output_file)
    
    # Write changes log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("BERVO Qualifiers Assignment Log\n")
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
    print("\nQualifier Distribution:")
    for key, value in sorted(stats.items()):
        if key.startswith('qualifier_'):
            print(f"  {key.replace('qualifier_', '')}: {value}")

if __name__ == '__main__':
    main()
