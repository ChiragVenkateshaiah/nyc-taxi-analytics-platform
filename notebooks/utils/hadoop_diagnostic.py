import os
import sys
from pathlib import Path


def diagnose_hadoop_setup():
    """Diagnose Hadoop Setup issues"""
    print("=" * 60)
    print("HADOOP SETUP DIAGNOSTICS")
    print("=" * 60)


    # Check HADOOP_HOME
    hadoop_home = os.environ.get('HADOOP_HOME')
    print(f"\n1. HADOOP_HOME: {hadoop_home}")

    if hadoop_home:
        hadoop_path = Path(hadoop_home)
        bin_path = hadoop_path / "bin"

        # Check directory exists
        print(f"  - Directory exists: {hadoop_path.exists()}")
        print(f"  - Bin directory exists: {bin_path.exists()}")


        # Check for required files
        winutils = bin_path / "winutils.exe"
        hadoop_dll = bin_path / "hadoop.dll"

        print(f"\n2. Required Files:")
        print(f"  - winutils.exe exists: {winutils.exists()}")
        if winutils.exists():
            print(f"    Size: {winutils.stat().st_size:,} bytes")

        print(f"   - hadoop.dll exists: {hadoop_dll.exists()}")
        if hadoop_dll.exists():
            print(f"  - Size: {hadoop_dll.stat().st_size:,} bytes")

        # Check PATH
        print(f"\n3. System PATH includes Hadoop bin:")
        path_dirs = os.environ.get('PATH', '').split(os.pathsep)
        hadoop_in_path = any('hadoop' in p.lower() for p in path_dirs)
        print(f"  - Hadoop in PATH: {hadoop_in_path}")

        print("\n" + "=" * 60)

# Run it
diagnose_hadoop_setup()