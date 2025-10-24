#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts markdown files to professionally formatted PDF documents

Usage:
    python md_to_pdf.py input.md [output.pdf]
    
If output filename is not provided, it will use the input filename with .pdf extension
"""

import sys
import os
import markdown
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration


def convert_md_to_pdf(input_file, output_file=None):
    """
    Convert a markdown file to PDF
    
    Args:
        input_file: Path to input markdown file
        output_file: Path to output PDF file (optional)
    """
    
    # Determine output filename
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.pdf'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    # Read markdown file
    print(f"Reading: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML with extensions
    md = markdown.Markdown(extensions=[
        'extra',           # Tables, code blocks, etc.
        'codehilite',      # Syntax highlighting
        'toc',             # Table of contents
        'fenced_code',     # Fenced code blocks
        'tables',          # Tables support
    ])
    html_content = md.convert(md_content)
    
    # Extract title from markdown (first h1 or filename)
    title = os.path.splitext(os.path.basename(input_file))[0]
    if md_content.startswith('# '):
        first_line = md_content.split('\n')[0]
        title = first_line.replace('#', '').strip()
    
    # Create complete HTML with CSS styling
    html_doc = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm 2cm 2.5cm 2cm;
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }}
            @bottom-right {{
                content: "{title}";
                font-size: 9pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #333;
            max-width: 100%;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 24pt;
            font-weight: bold;
            margin-top: 0;
            margin-bottom: 16pt;
            padding-bottom: 8pt;
            border-bottom: 3px solid #3498db;
            page-break-after: avoid;
        }}
        
        h2 {{
            color: #34495e;
            font-size: 16pt;
            font-weight: bold;
            margin-top: 20pt;
            margin-bottom: 10pt;
            padding-top: 8pt;
            border-bottom: 2px solid #95a5a6;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #34495e;
            font-size: 13pt;
            font-weight: bold;
            margin-top: 16pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #555;
            font-size: 11pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
        }}
        
        p {{
            margin: 8pt 0;
            text-align: justify;
        }}
        
        ul, ol {{
            margin: 8pt 0 8pt 20pt;
            padding-left: 0;
        }}
        
        li {{
            margin: 4pt 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }}
        
        thead {{
            background-color: #3498db;
            color: white;
        }}
        
        th {{
            padding: 8pt;
            text-align: left;
            font-weight: bold;
            border: 1px solid #2980b9;
        }}
        
        td {{
            padding: 6pt 8pt;
            border: 1px solid #bdc3c7;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: #ecf0f1;
        }}
        
        tbody tr:hover {{
            background-color: #d5dbdb;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2pt 4pt;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #c7254e;
        }}
        
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-left: 4px solid #3498db;
            padding: 12pt;
            margin: 12pt 0;
            overflow-x: auto;
            border-radius: 4px;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #333;
            font-size: 9pt;
            line-height: 1.4;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #bdc3c7;
            margin: 20pt 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 16pt;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: bold;
        }}
        
        /* Prevent widows and orphans */
        p, li, td, th {{
            orphans: 3;
            widows: 3;
        }}
        
        /* Page break controls */
        .page-break {{
            page-break-after: always;
        }}
        
        /* Table of contents styling */
        .toc {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 16pt;
            margin: 16pt 0;
            border-radius: 4px;
        }}
        
        .toc ul {{
            list-style-type: none;
        }}
        
        /* Warning/Note boxes */
        .warning {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 12pt;
            margin: 12pt 0;
        }}
        
        .critical {{
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 12pt;
            margin: 12pt 0;
        }}
        
        /* Header styling for sections */
        .section-header {{
            background-color: #3498db;
            color: white;
            padding: 8pt 12pt;
            margin: 16pt 0 12pt 0;
            border-radius: 4px;
        }}
        
        /* Checklist styling */
        input[type="checkbox"] {{
            margin-right: 8pt;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Generate PDF
    print(f"Converting to PDF...")
    HTML(string=html_doc).write_pdf(
        output_file,
        font_config=font_config
    )
    
    print(f"✓ PDF successfully created: {output_file}")
    
    # Show file size
    size_bytes = os.path.getsize(output_file)
    size_kb = size_bytes / 1024
    print(f"  File size: {size_kb:.1f} KB")
    
    return True


def main():
    """Main function to handle command line arguments"""
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Markdown to PDF Converter")
        print("=" * 50)
        print("\nUsage:")
        print("  python md_to_pdf.py input.md [output.pdf]")
        print("\nExamples:")
        print("  python md_to_pdf.py README.md")
        print("  python md_to_pdf.py document.md my-document.pdf")
        print("\nIf output filename is not specified, it will use")
        print("the input filename with .pdf extension")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Convert
    success = convert_md_to_pdf(input_file, output_file)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()