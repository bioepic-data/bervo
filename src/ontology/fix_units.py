import csv
import re

# Read the file
with open('bervo-src.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
metadata = rows[1]
data_rows = rows[2:]

# Column 13 is has_units (0-indexed: column 12)
# Column 3 is Category (0-indexed: column 2)
# Column 7 is Definition (0-indexed: column 6)

changes_made = 0

for i, row in enumerate(data_rows):
    if len(row) < 13:
        continue
        
    bervo_id = row[0]
    label = row[1]
    category = row[2]
    definition = row[6] if len(row) > 6 else ""
    current_units = row[12]
    
    # Skip if units already exist
    if current_units and current_units.strip():
        continue
    
    new_units = None
    
    # Rule 1: Root Variable class gets NA
    if bervo_id == "BERVO:0000000":
        new_units = "NA"
    
    # Rule 2: Abstract parent classes (category names ending in "variable", "parameters", "Concept") get NA
    elif category in ["Concept", "Variable", "Biogeochemical flux variable", "Ecosystem heat flux",
                       "Plant growth parameters", "Chemical tracer parameters", "Microbial parameters",
                       "Constants for specific chemical reactions", "Constants for specific biochemical reactions",
                       "Plant trait variable", "Soil biogeochemistry variable", "Soil and water variable",
                       "Canopy variable", "Snow variable", "Climate force variable", "Soil variable",
                       "Irrigation water variable", "Root variable", "Water variable", "Soil organic matter variable",
                       "Chemical transport variable", "Soil surface variable", "Sediment variable",
                       "Soil heat variable", "Irrigation variable", "Fertilizer variable",
                       "Plant rate variable", "Plant and microbial rate variable"]:
        # Check if this looks like a parent class (no EcoSIM variable name usually)
        if not row[4]:  # Column 5 (0-indexed 4) is EcoSIM Variable Name
            new_units = "NA"
    
    # Rule 3: Equilibrium constants - extract from definition
    elif "Equilibrium constant" in label or "equilibrium constant" in definition.lower():
        # Look for units in definition like "mol^2 m^-6", "mol m^-3", etc.
        unit_patterns = [
            r'mol\^\d+\s*m\^-\d+',
            r'mol\s*m\^-\d+',
            r'm\^\d+\s*mol\^-\d+',
        ]
        for pattern in unit_patterns:
            match = re.search(pattern, definition)
            if match:
                new_units = match.group(0)
                break
    
    # Rule 4: Dimensionless parameters (fractions, ratios, shape parameters)
    elif any(keyword in label.lower() for keyword in ["fraction", "ratio", "partition", "shape parameter",
                                                       "relative", "parameter for calculating"]):
        new_units = "NONE"
    
    # Rule 5: Diffusivity parameters without specific units
    elif "diffusivity" in label.lower() and category == "Chemical tracer parameters":
        new_units = "NA"  # Parent classes
    
    # Apply the change
    if new_units:
        row[12] = new_units
        changes_made += 1
        print(f"Line {i+3}: {bervo_id} - {label[:60]}... -> {new_units}")

print(f"\n\nTotal changes made: {changes_made}")

# Write back
with open('bervo-src_TEMP.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(metadata)
    writer.writerows(data_rows)

print("Temporary file created: bervo-src_TEMP.csv")
print("Review the changes before replacing the original file")
