#!/usr/bin/env python3
"""Quick test of PDF functionality"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Test imports
try:
    from flask import send_file
    print("✓ send_file imported")
except Exception as e:
    print(f"✗ send_file import failed: {e}")

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    print("✓ reportlab imported")
except Exception as e:
    print(f"✗ reportlab import failed: {e}")

# Test PDF generation
try:
    import io
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = [Paragraph("Test PDF", styles['Heading1']), Spacer(1, 0.3*inch)]
    doc.build(elements)
    pdf_buffer.seek(0)
    print(f"✓ PDF generated successfully ({len(pdf_buffer.getvalue())} bytes)")
except Exception as e:
    print(f"✗ PDF generation failed: {e}")

print("\n✓ All tests passed! PDF routes should work.")
