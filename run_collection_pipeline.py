import subprocess
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_pipeline():
    print("=" * 60)
    print("🚀 STARTING DATA COLLECTION PIPELINE")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    scripts = ['download_data.py', 'clean_data.py', 'validate_data.py']
    
    for script in scripts:
        script_path = os.path.join('scripts', script)
        print(f"\n▶️ Running: {script}")
        print("-" * 40)
        
        result = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"⚠️ Errors/Warnings:\n{result.stderr}")
        
        print("-" * 40)

    # Commit and push changes to GitHub
    print("\n📤 Pushing updates to GitHub...")
    os.system('git add data/ scripts/')
    os.system(f'git commit -m "Pipeline run - {datetime.now().strftime("%Y-%m-%d")}"')
    os.system('git push')
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE!")
    print("📊 Latest data available in: data/clean/")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
