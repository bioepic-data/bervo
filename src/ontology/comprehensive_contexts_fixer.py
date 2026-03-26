#!/usr/bin/env python3
"""
Comprehensive contexts assignment for BERVO ontology.
Assigns contexts based on label, attribute, measured_in, and measurement_of analysis.
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

def normalize_context(context, bervo_labels):
    """Normalize context to match BERVO concept if available."""
    if not context:
        return context
    
    # Try exact match first
    if context.lower() in bervo_labels:
        return bervo_labels[context.lower()]
    
    return context

def extract_contexts(label, attribute, measured_in, measurement_of):
    """Extract contexts from label and other metadata."""
    label_lower = label.lower()
    contexts = []
    
    # Ecosystem-level processes
    if any(term in label_lower for term in ['ecosystem', 'biome', 'net biome']):
        contexts.append('Ecosystem')
    
    # Irrigation contexts
    if 'surface irrigation' in label_lower or 'surface irrign' in label_lower:
        contexts.append('Surface irrigation')
    elif 'subsurface irrigation' in label_lower or 'subsurface irrign' in label_lower:
        contexts.append('Subsurface irrigation')
    elif 'irrigation' in label_lower and 'Irrigation' not in contexts:
        contexts.append('Irrigation')
    
    # Band vs non-band fertilization
    if 'non-band' in label_lower or 'nonband' in label_lower:
        contexts.append('Non-band')
    elif ' band' in label_lower or 'in band' in label_lower:
        contexts.append('Band')
    
    # Fertilizer application
    if 'fertilizer' in label_lower or 'fertilization' in label_lower:
        if 'Fertilizer' not in contexts:
            contexts.append('Fertilizer')
    
    # Fire-related
    if 'fire' in label_lower:
        contexts.append('Fire')
    
    # Precipitation
    if any(term in label_lower for term in ['precipitation', 'rainfall', 'rain ']):
        contexts.append('Precipitation')
    
    # Runoff
    if 'runoff' in label_lower:
        contexts.append('Runoff')
    
    # Snowpack context
    if 'snowpack' in label_lower or 'snow melt' in label_lower:
        contexts.append('Snowpack')
    
    # Growth and development
    if any(term in label_lower for term in ['growth stage', 'growth yield', 'growing', 'phenological']):
        contexts.append('Growth')
    
    # Temperature contexts
    if 'standard ambient temperature' in label_lower or 'at 25c' in label_lower:
        contexts.append('Standard ambient temperature')
    elif 'dewpoint' in label_lower:
        contexts.append('Dewpoint')
    
    # Photosynthesis contexts
    if 'c4 photosynthesis' in label_lower or 'c4 carbon fixation' in label_lower:
        contexts.append('C4 carbon fixation')
    
    # Infection/symbiosis
    if 'infection' in label_lower or 'nodule' in label_lower:
        contexts.append('Infection')
    
    # Lake/water body
    if 'lake' in label_lower:
        contexts.append('Lake')
    
    # Atmosphere
    if 'atmospheric' in label_lower or 'atmosphere' in label_lower:
        contexts.append('Atmosphere')
    
    # Landscape level
    if 'landscape' in label_lower:
        contexts.append('Landscape')
    
    # Surface vs subsurface
    if 'surface' in label_lower and not any(ctx in contexts for ctx in ['Surface irrigation', 'Subsurface irrigation', 'Subsurface']):
        # Check if it's a specific surface reference
        if any(term in label_lower for term in ['soil surface', 'ground surface', 'at surface']):
            contexts.append('Surface')
    
    if 'subsurface' in label_lower and 'Subsurface irrigation' not in contexts:
        contexts.append('Subsurface')
    
    # Soil context - for soil processes not already covered
    if measured_in and 'Soil' in measured_in:
        if not contexts and any(term in label_lower for term in [
            'mineraln', 'immobiln', 'nitrification', 'denitrification',
            'decomposition', 'respiration', 'uptake'
        ]):
            contexts.append('Soil')
    
    # Plant context - for plant processes
    if measured_in and 'Plant' in measured_in:
        if not contexts and any(term in label_lower for term in [
            'photosynthesis', 'fixation', 'transpiration'
        ]):
            contexts.append('Plant')
    
    # Root-specific processes
    if measured_in and 'Root' in measured_in:
        if not contexts and any(term in label_lower for term in [
            'root uptake', 'root nitrogen fixation', 'root respiration'
        ]):
            contexts.append('Root')
    
    # Canopy processes
    if measured_in and 'Canopy' in measured_in:
        if not contexts and any(term in label_lower for term in [
            'canopy', 'clumping'
        ]):
            contexts.append('Canopy')
    
    # Branch-specific
    if measured_in and 'Branch' in measured_in:
        if not contexts and 'branch' in label_lower:
            contexts.append('Branch')
    
    # Litter layer
    if 'litter' in label_lower and measured_in and 'Litter' in measured_in:
        if not contexts:
            contexts.append('Surface litter')
    
    # Boundary layer
    if 'boundary layer' in label_lower:
        contexts.append('Boundary Layer')
    
    # Thermal adaptation
    if 'thermal adaptation' in label_lower:
        contexts.append('Thermal adaptation')
    
    # If no contexts found, return NA
    if not contexts:
        return 'NA'
    
    # Return unique contexts joined by pipe
    return '|'.join(sorted(set(contexts)))

def process_csv():
    """Process the CSV file and assign contexts."""
    bervo_labels = get_bervo_labels()
    
    rows = []
    with open('bervo-src.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    
    changes = 0
    unchanged = 0
    context_counts = {}
    
    for i, row in enumerate(rows):
        if i < 2:  # skip headers
            continue
            
        # Ensure row has enough columns
        while len(row) < 29:
            row.append('')
        
        label = row[1].strip() if len(row) > 1 else ""
        attribute = row[14].strip() if len(row) > 14 else ""
        measured_in = row[15].strip() if len(row) > 15 else ""
        measurement_of = row[16].strip() if len(row) > 16 else ""
        current_context = row[17].strip() if len(row) > 17 else ""
        
        # Only process if context is empty
        if not current_context:
            # Extract contexts
            new_contexts = extract_contexts(label, attribute, measured_in, measurement_of)
            new_contexts = normalize_context(new_contexts, bervo_labels)
            
            row[17] = new_contexts
            changes += 1
            
            # Track assignments
            for ctx in new_contexts.split('|'):
                ctx = ctx.strip()
                if ctx and ctx != 'NA':
                    context_counts[ctx] = context_counts.get(ctx, 0) + 1
        else:
            unchanged += 1
    
    # Write output
    with open('bervo-src-with-contexts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"Completed! Changes: {changes}, Unchanged: {unchanged}")
    print(f"\nTop 40 context assignments:")
    for context, count in sorted(context_counts.items(), key=lambda x: x[1], reverse=True)[:40]:
        print(f"  {count:4d}  {context}")
    
    print(f"\nTotal unique contexts assigned: {len(context_counts)}")

if __name__ == '__main__':
    process_csv()
