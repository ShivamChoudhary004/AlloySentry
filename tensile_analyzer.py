import pandas as pd
import matplotlib.pyplot as plt
import json
import os

filename = 'Tensile Data.csv'

# 1. Load the data (skipping headers to reach the raw data block)
df = pd.read_csv(filename, skiprows=20)
df = df.drop(0) # Remove unit row

# Convert data to numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 2. Extract Key Results
uts_val = df['Tensile stress'].max()
max_strain = df['Tensile strain (Extension)'].max()

# 3. Create Visualization
plt.figure(figsize=(10, 6))
plt.plot(df['Tensile strain (Extension)'], df['Tensile stress'], color='#2c3e50', linewidth=2)

plt.title('AlloySentry: Stress-Strain Profile (Sample 24120074)', fontsize=14)
plt.xlabel('Engineering Strain (%)', fontsize=12)
plt.ylabel('Engineering Stress (MPa)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

# Highlight UTS
plt.scatter(df.loc[df['Tensile stress'].idxmax(), 'Tensile strain (Extension)'], 
            uts_val, color='red', label=f'UTS: {uts_val:.2f} MPa')

plt.legend()
plt.savefig('tensile_plot.png')
print("--- Tensile Graph Generated: tensile_plot.png ---")

# 4. Export JSON for the Gemma 4 Pipeline
tensile_results = {
    "uts_mpa": round(float(uts_val), 2),
    "elongation_at_break_pct": round(float(max_strain), 2),
    "test_type": "Tensile"
}

with open('tensile_results.json', 'w') as f:
    json.dump(tensile_results, f)

print("--- tensile_results.json Exported Successfully ---")