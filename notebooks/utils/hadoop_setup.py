import os
from pathlib import Path


def complete_hadoop_setup():
    """Complete Hadoop setup for Windows"""
    hadoop_home = Path("C:/hadoop")
    bin_dir = hadoop_home / "bin"


    # set HADOOP_NAME
    os.environ['HADOOP_HOME'] = str(hadoop_home)


    # Add to PATH
    if str(bin_dir) not in os.environ['PATH']:
        os.environ['PATH'] = str(bin_dir) + os.pathsep + os.environ['PATH']

    print("✔ HADOOP_HOME set to:, os.environ['HADOOP_HOME']")
    print("✔ Added to PATH:", bin_dir)


    # Verify files
    winutils = bin_dir / "winutils.exe"
    hadoop_dll = bin_dir / "hadoop.dll"

    print(f"\n ✔ winutils.exe: {winutils.exists()}")
    print(f" ✔ hadoop.dll: {hadoop_dll.exists()}")

    if winutils.exists() and hadoop_dll.exists():
        print("\n🎉 Setup complete!")
    else:
        print("\n⚠ Missing files - check above")

complete_hadoop_setup()