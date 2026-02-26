"""
============================================
 PDF Generator — Travel Itinerary to PDF
============================================
Converts the generated Markdown itinerary into
a clean, downloadable PDF file using ReportLab.

This module is used by app.py to provide the
"Download as PDF" feature.
============================================
"""

# ── Imports ──────────────────────────────────────────────
import io
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


# ══════════════════════════════════════════════════════════
#  STYLE CONFIGURATION
# ══════════════════════════════════════════════════════════

def _get_styles():
    """Create custom paragraph styles for the PDF."""
    styles = getSampleStyleSheet()

    # Title style — large, bold, dark blue
    styles.add(ParagraphStyle(
        name="TripTitle",
        parent=styles["Heading1"],
        fontSize=22,
        spaceAfter=12,
        textColor=HexColor("#203A43"),
    ))

    # Section heading style — medium, bold, teal
    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8,
        textColor=HexColor("#2C5364"),
    ))

    # Sub-heading style — for Day headings
    styles.add(ParagraphStyle(
        name="SubHeading",
        parent=styles["Heading3"],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
        textColor=HexColor("#203A43"),
    ))

    # Body text style
    styles.add(ParagraphStyle(
        name="BodyText2",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=4,
    ))

    # Small footer style
    styles.add(ParagraphStyle(
        name="Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=HexColor("#7a8b9a"),
        alignment=1,  # center
    ))

    return styles


# ══════════════════════════════════════════════════════════
#  MARKDOWN TABLE PARSER
# ══════════════════════════════════════════════════════════

def _parse_md_table(text):
    """
    Parse a markdown table string into a list of rows.
    Each row is a list of cell strings.

    Args:
        text (str): Markdown table text.

    Returns:
        list[list[str]]: Parsed table data.
    """
    rows = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Skip separator rows like |---|---|
        if re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if cells:
            rows.append(cells)
    return rows


# ══════════════════════════════════════════════════════════
#  CLEAN TEXT — remove markdown formatting for PDF
# ══════════════════════════════════════════════════════════

def _clean_text(text):
    """Remove markdown formatting characters for clean PDF text."""
    # Remove bold markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    # Remove italic markers
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    # Remove emoji (keep them actually — ReportLab handles some)
    # Remove backticks
    text = text.replace("`", "")
    return text.strip()


# ══════════════════════════════════════════════════════════
#  MAIN FUNCTION — generate PDF bytes
# ══════════════════════════════════════════════════════════

def generate_pdf(itinerary_text, destination="Travel Plan"):
    """
    Convert a Markdown itinerary into a PDF file.

    Args:
        itinerary_text (str) : The full itinerary in Markdown format.
        destination    (str) : Destination name (used in the title).

    Returns:
        bytes : The PDF file content as bytes, ready for download.
    """
    # ── Create an in-memory buffer for the PDF ───────────
    buffer = io.BytesIO()

    # ── Set up the PDF document ──────────────────────────
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = _get_styles()
    elements = []

    # ── Title ────────────────────────────────────────────
    elements.append(Paragraph(
        f"Travel Plan — {_clean_text(destination)}",
        styles["TripTitle"],
    ))
    elements.append(HRFlowable(
        width="100%", thickness=2,
        color=HexColor("#2C5364"), spaceAfter=12,
    ))

    # ── Process the Markdown line by line ────────────────
    lines = itinerary_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Skip horizontal rules
        if line == "---":
            elements.append(Spacer(1, 8))
            elements.append(HRFlowable(
                width="100%", thickness=1,
                color=HexColor("#e0e0e0"), spaceAfter=8,
            ))
            i += 1
            continue

        # ── H2 heading (## Section) ──────────────────────
        if line.startswith("## "):
            heading_text = _clean_text(line[3:])
            elements.append(Paragraph(heading_text, styles["SectionHeading"]))
            i += 1
            continue

        # ── H3 heading (### Day X) ───────────────────────
        if line.startswith("### "):
            heading_text = _clean_text(line[4:])
            elements.append(Paragraph(heading_text, styles["SubHeading"]))
            i += 1
            continue

        # ── Markdown table ───────────────────────────────
        if line.startswith("|"):
            # Collect all consecutive table lines
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            table_text = "\n".join(table_lines)
            table_data = _parse_md_table(table_text)

            if table_data and len(table_data) > 0:
                # Create a ReportLab table
                # Clean text in cells
                cleaned_data = []
                for row in table_data:
                    cleaned_row = [_clean_text(cell) for cell in row]
                    cleaned_data.append(cleaned_row)

                # Determine column widths based on number of columns
                num_cols = len(cleaned_data[0])
                available_width = doc.width
                col_widths = [available_width / num_cols] * num_cols

                # Wrap cell text in Paragraphs for text wrapping
                para_data = []
                for row_idx, row in enumerate(cleaned_data):
                    para_row = []
                    for cell in row:
                        if row_idx == 0:
                            # Header row — bold
                            para_row.append(Paragraph(
                                f"<b>{cell}</b>",
                                styles["BodyText2"],
                            ))
                        else:
                            para_row.append(Paragraph(
                                cell, styles["BodyText2"],
                            ))
                    para_row.extend(
                        [Paragraph("", styles["BodyText2"])]
                        * (num_cols - len(para_row))
                    )
                    para_data.append(para_row)

                t = Table(para_data, colWidths=col_widths)
                t.setStyle(TableStyle([
                    # Header row styling
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2C5364")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                    # Alternating row colors
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f9fbfd")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [HexColor("#ffffff"), HexColor("#f0f4f8")]),
                    # Grid
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#d0d8e0")),
                    # Padding
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    # Alignment
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]))
                elements.append(Spacer(1, 4))
                elements.append(t)
                elements.append(Spacer(1, 8))

            continue

        # ── Bullet points ────────────────────────────────
        if line.startswith(("- ", "• ", "* ")):
            bullet_text = _clean_text(line[2:])
            elements.append(Paragraph(
                f"• {bullet_text}",
                styles["BodyText2"],
            ))
            i += 1
            continue

        # ── Regular text ─────────────────────────────────
        text = _clean_text(line)
        if text:
            elements.append(Paragraph(text, styles["BodyText2"]))

        i += 1

    # ── Footer ───────────────────────────────────────────
    elements.append(Spacer(1, 24))
    elements.append(HRFlowable(
        width="100%", thickness=1,
        color=HexColor("#e0e0e0"), spaceAfter=8,
    ))
    elements.append(Paragraph(
        "Generated by AI Travel Planner — Powered by Groq & Streamlit",
        styles["Footer"],
    ))

    # ── Build the PDF ────────────────────────────────────
    doc.build(elements)

    # ── Return the bytes ─────────────────────────────────
    buffer.seek(0)
    return buffer.getvalue()
