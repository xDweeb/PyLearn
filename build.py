# build.py
# Build script for PyLearn Desktop Windows executable
# Usage: python build.py

import os
import sys
import subprocess
import shutil

# Project configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DIST_FOLDER = os.path.join(PROJECT_ROOT, 'dist')
BUILD_FOLDER = os.path.join(PROJECT_ROOT, 'build')
SPEC_FILE = os.path.join(PROJECT_ROOT, 'pylearn.spec')


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
        return True
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        return True


def check_pyside6():
    """Check if PySide6 is installed."""
    try:
        import PySide6
        print(f"✓ PySide6 {PySide6.__version__} found")
        return True
    except ImportError:
        print("✗ PySide6 not found. Please install it: pip install PySide6")
        return False


def clean_build():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous builds...")
    for folder in [DIST_FOLDER, BUILD_FOLDER]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed: {folder}")


def build_executable():
    """Build the executable using PyInstaller."""
    print("\n🔨 Building executable...")
    
    # Run PyInstaller with the spec file
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        SPEC_FILE
    ]
    
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if result.returncode == 0:
        exe_path = os.path.join(DIST_FOLDER, 'PyLearnDesktop.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n✅ Build successful!")
            print(f"   Executable: {exe_path}")
            print(f"   Size: {size_mb:.2f} MB")
            return True
    
    print("\n❌ Build failed!")
    return False


def main():
    """Main build process."""
    print("=" * 60)
    print("   PyLearn Desktop - Windows Build Script")
    print("=" * 60)
    
    # Checks
    if not check_pyside6():
        sys.exit(1)
    
    check_pyinstaller()
    
    # Clean and build
    clean_build()
    
    if build_executable():
        print("\n" + "=" * 60)
        print("   Build complete! 🎉")
        print("=" * 60)
        print(f"\nYour executable is ready at:")
        print(f"  {os.path.join(DIST_FOLDER, 'PyLearnDesktop.exe')}")
        print("\nNote: On first run, the app will create a database in:")
        print("  %APPDATA%\\PyLearnDesktop\\pylearn.db")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
