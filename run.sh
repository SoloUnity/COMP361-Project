#!/bin/bash

if [ ! -f "SpaceY.spec" ] || [ ! -f "main.py" ]; then
    echo "❌ Error: This script must be run from the project root directory"
    echo "   Please cd to the root directory"
    exit 1
fi

echo "🧹 Cleaning previous build artifacts..."
rm -rf build dist

echo "🔨 Building executable with PyInstaller..."
pyinstaller -y SpaceY.spec > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Build complete!"
    echo "🚀 Running application..."
    ./dist/SpaceY
else
    echo "❌ Build failed! See errors above."
    exit 1
fi