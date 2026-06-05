import io
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def generate_roadmap_pdf(roadmap_data: Dict[str, Any], candidate_name: Optional[str] = None) -> bytes:
    """
    Generates a production-quality multi-page PDF for the given roadmap.
    Uses ReportLab for rendering. Returns raw PDF bytes.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, PageBreak
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        raise RuntimeError(
            "ReportLab is not installed. Run: pip install reportlab"
        )

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    # ---- Custom Styles ----
    DARK_BG = colors.HexColor("#0f1117")
    ACCENT = colors.HexColor("#6366f1")
    SUCCESS = colors.HexColor("#10b981")
    TEXT_MAIN = colors.HexColor("#e2e8f0")
    TEXT_MUTED = colors.HexColor("#94a3b8")
    CARD_BG = colors.HexColor("#1e2130")
    WARNING = colors.HexColor("#f59e0b")

    h1_style = ParagraphStyle("H1", parent=styles["Heading1"],
                               fontSize=22, textColor=colors.white,
                               fontName="Helvetica-Bold", spaceAfter=8)
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"],
                               fontSize=15, textColor=ACCENT,
                               fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6)
    h3_style = ParagraphStyle("H3", parent=styles["Heading3"],
                               fontSize=11, textColor=TEXT_MAIN,
                               fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle("Body", parent=styles["Normal"],
                                 fontSize=9, textColor=TEXT_MAIN,
                                 fontName="Helvetica", spaceAfter=3, leading=14)
    muted_style = ParagraphStyle("Muted", parent=styles["Normal"],
                                  fontSize=8, textColor=TEXT_MUTED,
                                  fontName="Helvetica", spaceAfter=2)
    label_style = ParagraphStyle("Label", parent=styles["Normal"],
                                  fontSize=8, textColor=ACCENT,
                                  fontName="Helvetica-Bold", spaceAfter=2,
                                  spaceBefore=4)

    story = []

    career = roadmap_data.get("career", "Career")
    difficulty = roadmap_data.get("difficulty", "Intermediate")
    total_weeks = roadmap_data.get("total_weeks", 0)
    total_months = roadmap_data.get("total_months", 0)
    expected_readiness = roadmap_data.get("expected_readiness", 92)
    milestones = roadmap_data.get("milestones", [])
    monthly_roadmap = roadmap_data.get("monthly_roadmap", [])
    progress = roadmap_data.get("progress", {})
    job_market = roadmap_data.get("job_market")
    career_forecast = roadmap_data.get("career_forecast")

    current_readiness = progress.get("completion_percentage", 0)
    name_str = candidate_name or "Candidate"

    # ======================================================
    # PAGE 1: Cover + Career Forecast + Salary Insights
    # ======================================================
    story.append(Paragraph(f"🚀 {career}", h1_style))
    story.append(Paragraph("Personalized Career Intelligence Roadmap", h2_style))
    story.append(Paragraph(f"Prepared for: <b>{name_str}</b>", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 0.3 * cm))

    # Readiness summary table
    readiness_data = [
        ["Metric", "Value"],
        ["Current Readiness", f"{current_readiness}%"],
        ["Projected Readiness", f"{expected_readiness}%"],
        ["Difficulty Level", difficulty],
        ["Total Duration", f"{total_weeks} weeks / {total_months} months"],
    ]
    if career_forecast:
        readiness_data.append(["Success Probability", f"{career_forecast.get('success_probability', 80)}%"])
        readiness_data.append(["Time to Job Ready", career_forecast.get("time_to_job_ready", "—")])
        readiness_data.append(["Skills Mastered", str(career_forecast.get("skills_mastered", 0))])
        readiness_data.append(["Skills Remaining", str(career_forecast.get("skills_remaining", 0))])

    rt = Table(readiness_data, colWidths=[8 * cm, 8 * cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 1), (-1, -1), CARD_BG),
        ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_MAIN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CARD_BG, colors.HexColor("#252840")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2d3150")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.5 * cm))

    # Eligible roles
    if career_forecast and career_forecast.get("eligible_roles"):
        story.append(Paragraph("Eligible Roles After Completion", h3_style))
        for role in career_forecast["eligible_roles"]:
            story.append(Paragraph(f"• {role}", body_style))
        story.append(Spacer(1, 0.3 * cm))

    # Salary Insights
    if job_market:
        story.append(Paragraph("💰 Job Market Intelligence", h2_style))
        india_sal = job_market.get("india_salary", {})
        global_sal = job_market.get("global_salary", {})
        sal_data = [
            ["Market", "Salary Range", "Demand", "YoY Growth", "Openings"],
            [
                "🇮🇳 India",
                india_sal.get("formatted", "—"),
                job_market.get("demand_level", "—"),
                job_market.get("yoy_growth", "—"),
                f"{job_market.get('estimated_job_openings', 0):,}"
            ],
            [
                "🌍 Global",
                global_sal.get("formatted", "—"),
                job_market.get("hiring_trend", "—"),
                job_market.get("trend_direction", "—").title(),
                "Remote Friendly" if job_market.get("remote_friendly") else "On-site"
            ],
        ]
        st = Table(sal_data, colWidths=[3 * cm, 4 * cm, 3 * cm, 2.5 * cm, 3.5 * cm])
        st.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), SUCCESS),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BACKGROUND", (0, 1), (-1, -1), CARD_BG),
            ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_MAIN),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2d3150")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(st)

        if job_market.get("top_employers"):
            story.append(Spacer(1, 0.25 * cm))
            story.append(Paragraph("Top Hiring Companies", h3_style))
            story.append(Paragraph(", ".join(job_market["top_employers"]), muted_style))

        if job_market.get("certification_boost"):
            story.append(Spacer(1, 0.2 * cm))
            story.append(Paragraph("Recommended Certifications", h3_style))
            for cert in job_market["certification_boost"]:
                story.append(Paragraph(f"✓ {cert}", body_style))

    story.append(PageBreak())

    # ======================================================
    # PAGE 2: Timeline + Skill Gap
    # ======================================================
    story.append(Paragraph("🗺️ Monthly Learning Timeline", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT))
    story.append(Spacer(1, 0.3 * cm))

    timeline_data = [["Month", "Focus Area", "Skills"]]
    for month in monthly_roadmap:
        timeline_data.append([
            f"Month {month.get('month_number', '?')}",
            month.get("title", ""),
            ", ".join(month.get("skills", []))[:80]
        ])

    tt = Table(timeline_data, colWidths=[2.5 * cm, 7 * cm, 7 * cm])
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 1), (-1, -1), CARD_BG),
        ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_MAIN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CARD_BG, colors.HexColor("#252840")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#2d3150")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("WORDWRAP", (0, 0), (-1, -1), True),
    ]))
    story.append(tt)
    story.append(PageBreak())

    # ======================================================
    # PAGE 3: Milestones + Resources
    # ======================================================
    story.append(Paragraph("🏆 Milestones & Learning Resources", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT))
    story.append(Spacer(1, 0.3 * cm))

    for ms in milestones:
        status = "✅ Complete" if ms.get("complete") else "⏳ In Progress"
        story.append(Paragraph(f"{ms.get('title', '')}  [{status}]", h3_style))
        skills_str = ", ".join(ms.get("skills", []))
        story.append(Paragraph(f"Skills: {skills_str}", muted_style))

        resources = ms.get("resources", [])
        if resources:
            story.append(Paragraph("Resources:", label_style))
            for res in resources[:4]:
                story.append(Paragraph(f"  [{res.get('type', 'Course')}] {res.get('name', '')} — {res.get('url', '')}", muted_style))

        story.append(Spacer(1, 0.2 * cm))

    story.append(PageBreak())

    # ======================================================
    # PAGE 4: Portfolio Projects
    # ======================================================
    story.append(Paragraph("🛠️ Recommended Portfolio Projects", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT))
    story.append(Spacer(1, 0.3 * cm))

    for ms in milestones:
        projects = ms.get("projects", [])
        if not projects:
            continue
        story.append(Paragraph(ms.get("title", ""), h3_style))
        for proj in projects:
            diff = proj.get("difficulty", "Intermediate")
            diff_color = "#f87171" if diff == "Advanced" else ("#fbbf24" if diff == "Intermediate" else "#34d399")
            story.append(Paragraph(
                f"<b>{proj.get('title', '')}</b> <font color='{diff_color}' size='8'>[{diff}]</font>",
                body_style
            ))
            story.append(Paragraph(proj.get("description", ""), muted_style))
            tech = proj.get("tech", [])
            if tech:
                story.append(Paragraph(f"Tech: {', '.join(tech)}", label_style))
            story.append(Spacer(1, 0.15 * cm))

    # ======================================================
    # Build PDF
    # ======================================================
    doc.build(story)
    buffer.seek(0)
    return buffer.read()
