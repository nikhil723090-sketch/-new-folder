"""Generate PDF reports from conversations, charts, maps, and recommendations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class CrimeReport:
    """PDF report content."""

    officer_name: str
    title: str
    crime_summary: str
    conversation: list[dict[str, str]]
    recommendations: list[str]
    chart_paths: list[str] = field(default_factory=list)
    map_paths: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class CrimePdfReportGenerator:
    """ReportLab PDF generator."""

    def generate(self, report: CrimeReport, output_path: str | Path) -> Path:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer

        output = Path(output_path)
        doc = SimpleDocTemplate(str(output), pagesize=A4)
        styles = getSampleStyleSheet()
        story = [
            Paragraph(report.title, styles["Title"]),
            Paragraph(f"Officer: {report.officer_name}", styles["Normal"]),
            Paragraph(f"Timestamp: {report.timestamp.isoformat(timespec='seconds')}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph("Crime Summary", styles["Heading2"]),
            Paragraph(report.crime_summary, styles["BodyText"]),
            Spacer(1, 12),
            Paragraph("Conversation", styles["Heading2"]),
        ]

        for turn in report.conversation:
            story.append(Paragraph(f"User: {turn.get('user', '')}", styles["BodyText"]))
            story.append(Paragraph(f"AI: {turn.get('ai', '')}", styles["BodyText"]))
            story.append(Spacer(1, 6))

        story.append(Paragraph("Recommendations", styles["Heading2"]))
        for item in report.recommendations:
            story.append(Paragraph(f"- {item}", styles["BodyText"]))

        for chart in report.chart_paths:
            path = Path(chart)
            if path.exists() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                story.append(Spacer(1, 12))
                story.append(Image(str(path), width=420, height=240))

        if report.map_paths:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Maps are attached as separate HTML files.", styles["BodyText"]))

        doc.build(story)
        return output
