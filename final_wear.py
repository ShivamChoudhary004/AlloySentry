import pandas as pd
import matplotlib.pyplot as plt
import json

# Configuration
filename = '24120085.dwf'
load = 19.63 # Newtons (from your lab setup)

def process_wear_data():
    print("--- Running Wear Analysis ---")
    try:
        # 1. Load Data
        df = pd.read_csv(filename, sep=r';\s*', engine='python')
        df.columns = [c.strip('; ') for c in df.columns]

        # 2. Calculation (Using .abs() for depth)
        df['WEAR_FINAL'] = df['WEAR'].abs() 
        avg_cof = (df['FF'] / load).mean()
        max_wear = df['WEAR_FINAL'].max()

        # 3. Save JSON (The key is 'max_wear_um')
        with open('wear_results.json', 'w') as f:
            json.dump({
                "avg_cof": round(float(avg_cof), 4), 
                "max_wear_um": round(float(max_wear), 2)
            }, f)

        # 4. Plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['TIME'], df['WEAR_FINAL'], color='blue', linewidth=2)
        plt.title('AlloySentry: Wear Depth Analysis (Sample 24120085)', fontsize=14)
        plt.xlabel('Time (s)')
        plt.ylabel('Wear Depth (μm)')
        plt.grid(True)

        plt.savefig('wear_test_plot.png')
        print("✅ Wear Graph Generated: wear_test_plot.png")
        print("✅ Data exported to wear_results.json")
        
    except Exception as e:
        print(f"❌ Error in final_wear.py: {e}")

if __name__ == "__main__":
    process_wear_data()