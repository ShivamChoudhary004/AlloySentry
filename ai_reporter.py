import ollama
import json
import os

# 1. Configuration
MODEL_NAME = 'gemma4-e4b:latest' 

def generate_report():
    # 2. Load the lab data from your other scripts
    try:
        with open('tensile_results.json', 'r') as t_file:
            t_data = json.load(t_file)
        with open('wear_results.json', 'r') as w_file:
            w_data = json.load(w_file)
        print("✅ Lab data loaded successfully.")
    except FileNotFoundError:
        print("❌ Error: JSON files not found! Run tensile_analyzer.py and final_wear.py first.")
        return

    # Extract values safely
    uts = t_data.get('uts_mpa', 'N/A')
    elongation = t_data.get('elongation_at_break_pct', 'N/A')
    
    # Matching the keys from final_wear.py
    friction = w_data.get('avg_cof', 'N/A')
    wear_depth = w_data.get('max_wear_um', 'N/A') # FIXED: Matches final_wear.py key

    # 3. Format the context for Gemma 4
    lab_context = f"""
    <|think|>
    Analyze the following AlloySentry metallurgical results for a professional report:
    - Tensile Strength (UTS): {uts} MPa
    - Ductility (Elongation): {elongation}%
    - Friction Coefficient: {friction}
    - Max Wear Depth: {wear_depth} um

    Is this material likely a cast alloy or a wrought alloy? 
    Discuss the hardness-toughness trade-off based on these specific UTS and wear results.
    """

    print(f"🤖 Generating analysis using {MODEL_NAME}...")
    
    try:
        # 4. Generate the Report
        response = ollama.chat(model=MODEL_NAME, messages=[
            {
                'role': 'user',
                'content': lab_context,
            },
        ])

        # Output the report to the terminal
        print("\n" + "="*55)
        print("🔬 ALLOYSENTRY: FINAL METALLURGICAL ANALYSIS REPORT")
        print("="*55)
        print(response['message']['content'])
        print("="*55)
        
        # Also save it to a file automatically so you don't have to copy-paste
        with open('AlloySentry_Report.txt', 'w', encoding='utf-8') as f:
            f.write(response['message']['content'])
        print("\n📝 Report also saved to 'AlloySentry_Report.txt'")
        
    except Exception as e:
        print(f"❌ Error during AI generation: {e}")

if __name__ == "__main__":
    generate_report()