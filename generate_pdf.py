"""
Script to convert PROJECT_REPORT.md to PDF format using ReportLab
"""
import os
import sys
import re
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Installing markdown library...")
    os.system(f"{sys.executable} -m pip install markdown")
    import markdown

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Installing reportlab library...")
    os.system(f"{sys.executable} -m pip install reportlab")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

def clean_text(text):
    """Remove markdown formatting and clean text"""
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown images
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    # Remove markdown code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove markdown bold/italic
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def parse_markdown_to_elements(md_content):
    """Parse markdown content and return list of elements for ReportLab"""
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#000000'),
        spaceAfter=12,
        spaceBefore=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#000000'),
        spaceAfter=10,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#000000'),
        spaceAfter=8,
        spaceBefore=14,
        fontName='Helvetica-Bold'
    )
    
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#000000'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        textColor=colors.HexColor('#333333'),
        fontName='Courier',
        leftIndent=20,
        rightIndent=20,
        backColor=colors.HexColor('#f5f5f5'),
        spaceAfter=10
    )
    
    lines = md_content.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Handle code blocks
        if line.startswith('```'):
            if in_code_block:
                # End of code block
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    elements.append(Preformatted(code_text, code_style))
                    code_lines = []
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # Handle horizontal rules
        if line.strip() == '---' or line.strip() == '***':
            elements.append(Spacer(1, 0.2*inch))
            i += 1
            continue
        
        # Handle headings
        if line.startswith('# '):
            text = clean_text(line[2:])
            if i == 0 or i == 1:
                elements.append(Paragraph(text, title_style))
            else:
                elements.append(Paragraph(text, h1_style))
        elif line.startswith('## '):
            text = clean_text(line[3:])
            elements.append(Paragraph(text, h2_style))
        elif line.startswith('### '):
            text = clean_text(line[4:])
            elements.append(Paragraph(text, h3_style))
        elif line.startswith('#### '):
            text = clean_text(line[5:])
            elements.append(Paragraph(text, h3_style))
        # Handle lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = clean_text(line.strip()[2:])
            bullet_text = f"• {text}"
            elements.append(Paragraph(bullet_text, normal_style))
        elif re.match(r'^\d+\.\s', line.strip()):
            text = clean_text(line.strip())
            elements.append(Paragraph(text, normal_style))
        # Handle tables (simple detection)
        elif '|' in line and line.count('|') >= 2:
            # Skip table separator lines
            if not re.match(r'^\|[\s\-:]+\|', line):
                # Parse table row
                cells = [clean_text(cell.strip()) for cell in line.split('|')[1:-1]]
                if cells:
                    # Create a simple table row
                    table_data = [[Paragraph(cell, normal_style) for cell in cells]]
                    table = Table(table_data, colWidths=[2*inch] * len(cells))
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 0.1*inch))
        # Handle bold text
        elif '**' in line:
            # Simple bold handling
            text = clean_text(line)
            elements.append(Paragraph(text, normal_style))
        # Regular paragraph
        else:
            text = clean_text(line)
            if text:
                elements.append(Paragraph(text, normal_style))
        
        i += 1
    
    return elements

def markdown_to_pdf(md_file_path, pdf_file_path):
    """Convert markdown file to PDF"""
    
    # Read markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        str(pdf_file_path),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Parse markdown and create elements
    elements = parse_markdown_to_elements(md_content)
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"✅ PDF generated successfully: {pdf_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Get project root directory
    project_root = Path(__file__).parent
    md_file = project_root / "PROJECT_REPORT.md"
    pdf_file = project_root / "PROJECT_REPORT.pdf"
    
    if not md_file.exists():
        print(f"❌ Error: {md_file} not found!")
        sys.exit(1)
    
    print(f"📄 Converting {md_file} to PDF...")
    print(f"📁 Output file: {pdf_file}")
    print("⏳ This may take a moment...")
    
    if markdown_to_pdf(md_file, pdf_file):
        file_size = pdf_file.stat().st_size / 1024
        print(f"\n✨ Success! PDF report created at: {pdf_file}")
        print(f"📊 File size: {file_size:.2f} KB")
    else:
        print("\n❌ Failed to generate PDF. Please check the error messages above.")
        sys.exit(1)
