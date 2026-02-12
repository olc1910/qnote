#!/usr/bin/env bash
# Test script for qnote config commands

set -e

echo "Testing qnote config commands..."
echo ""

# Set test config path
export QNOTE_CONFIG="/tmp/qnote-test-config.yaml"
rm -f "$QNOTE_CONFIG"

echo "1. Testing config list (should show defaults)..."
qnote config list
echo ""

echo "2. Testing config set..."
qnote config set editor nvim
qnote config set theme dark
qnote config set sync.auto true
echo ""

echo "3. Testing config get..."
qnote config get editor
qnote config get theme
qnote config get sync.auto
echo ""

echo "4. Testing config list again (should show changes)..."
qnote config list
echo ""

echo "5. Testing config path..."
qnote config path
echo ""

echo "6. Verifying config file contents..."
cat "$QNOTE_CONFIG"
echo ""

echo "✓ All config commands working!"

# Cleanup
rm -f "$QNOTE_CONFIG"
