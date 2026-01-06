#!/usr/bin/env python3
"""
Edit iOS screenshots to change time to 9:41 and battery to full/green.
Note: This is a simplified approach. For best results, use Xcode simulator's
status bar override feature to retake screenshots.
"""

import subprocess
import os

screenshots = [
    'assets/screenshots/capture-light.PNG',
    'assets/screenshots/capture-dark.PNG',
    'assets/screenshots/cleanup-light.PNG',
    'assets/screenshots/cleanup-dark.PNG',
    'assets/screenshots/organize-light.PNG',
    'assets/screenshots/organize-dark.PNG',
    'assets/screenshots/review-light.PNG',
    'assets/screenshots/review-dark.PNG',
]

for screenshot in screenshots:
    if not os.path.exists(screenshot):
        print(f"Skipping {screenshot} - file not found")
        continue

    print(f"Processing {screenshot}...")

    # Get image width
    result = subprocess.run(['magick', 'identify', '-format', '%w', screenshot],
                          capture_output=True, text=True)
    width = int(result.stdout.strip())

    # Determine if it's dark or light mode for appropriate colors
    is_dark = 'dark' in screenshot.lower()
    bg_color = '#000000' if is_dark else '#FFFFFF'
    text_color = '#FFFFFF' if is_dark else '#000000'

    # Create output filename
    output = screenshot

    # Status bar is roughly at top 150 pixels
    # Time is usually around 60-80 pixels from left
    # Battery is around 80 pixels from right

    # Overlay white/black rectangle over old time and draw new time
    # Note: Using Helvetica as approximation of SF Pro
    subprocess.run([
        'magick', screenshot,
        '-fill', bg_color,
        # Cover old time (approximate position for 1320px wide screen)
        '-draw', f'rectangle 50,20 150,80',
        # Draw new time
        '-font', 'Helvetica-Bold',
        '-pointsize', '52',
        '-fill', text_color,
        '-annotate', '+55+65', '9:41',
        # Cover old battery indicator (approximate position)
        '-fill', bg_color,
        '-draw', f'rectangle {width-150},20 {width-50},80',
        # Note: Battery icon is complex, would need actual icon overlay
        # For now, we'll just draw a simple green rectangle as placeholder
        '-fill', '#00FF00' if not is_dark else '#30D158',  # iOS green
        '-draw', f'rectangle {width-120},35 {width-65},65',
        '-fill', text_color,
        '-font', 'Helvetica-Bold',
        '-pointsize', '35',
        '-annotate', f'+{width-110}+62', '100',
        output
    ])

    print(f"Updated {screenshot}")

print("\n" + "="*60)
print("IMPORTANT NOTE:")
print("="*60)
print("This script provides a basic edit of the status bar.")
print("For professional-quality results, please use one of these methods:")
print()
print("1. Xcode Simulator Status Bar Override:")
print("   xcrun simctl status_bar booted override \\")
print("     --time '9:41' \\")
print("     --batteryState charged \\")
print("     --batteryLevel 100")
print()
print("2. Use Figma, Photoshop, or a screenshot mockup tool")
print("3. Use a tool like Cleanshot X or Shottr for macOS")
print("="*60)
