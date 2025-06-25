#!/usr/bin/env bash
#
# flash_and_read.sh  –  one-command workflow
#
#   1. Compiles the sketch with arduino-cli
#   2. Uploads it to /dev/ttyACM0 (Mega 2560)
#   3. Launches the Python fuel-reader
#
# Assumes:
#   • arduino-cli is already on PATH
#   • user is in the dialout group
#   • pyserial is installed for the current user
#q
# Project tree (relative paths):
#   firmware/firmware.ino
#   scripts/readfueldatascriptpy        ← your Python file
#
export PATH="$HOME/workspace/readserial/bin:$PATH"   # <- add this
set -e  # exit immediately on any command failure

# ---------- USER CONFIG ------------------
PORT="/dev/ttyACM0"
FQBN="arduino:avr:mega"

SKETCH_DIR="$(dirname "$0")/firmware"
PY_READER="$(dirname "$0")/scripts/readfueldatascriptpy"
# -----------------------------------------

echo "=== Step 1: Compiling firmware…"
arduino-cli compile --fqbn "$FQBN" "$SKETCH_DIR"

echo "=== Step 2: Uploading to $PORT…"
arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$SKETCH_DIR"

# Give the Mega a moment to reboot after upload
sleep 2

echo "=== Step 3: Starting Python monitor…"
python3 "$PY_READER"
