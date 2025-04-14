#!/bin/bash

# === STARTUP SCRIPT FOR SUVIE BOT ===
echo "🚀 Starting Suvie..."

# Set working directory
cd "$(dirname "$0")"

# Set PYTHONPATH to current directory for proper relative imports
export PYTHONPATH=$(pwd)

# Print Python path for debug
echo "🔍 PYTHONPATH: $PYTHONPATH"

# Run the bot
echo "🧠 Launching bot with: python3 -m bot.bot"
python3 -m bot.bot

# Capture exit code
exit_code=$?

# Exit code handling
if [ $exit_code -eq 0 ]; then
    echo "✅ Suvie exited successfully."
else
    echo "❌ Suvie exited with error code $exit_code"
fi
