"""
roadmap_pdf_service.py  –  Phase 9 Premium PDF Report (Redesigned)

Generates a professional 7-page consulting-style PDF using ReportLab.
Structure:
  Page 1 – Cover Page         (branded dark strip, score pills, tagline)
  Page 2 – Executive Summary  (readiness, ATS, success probability)
  Page 3 – Career Recommendation & Skill Gap Analysis
  Page 4 – Learning Timeline  (monthly roadmap + weekly overview)
  Page 5 – Milestones & Resources
  Page 6 – Portfolio Projects
  Page 7 – Action Plan & Certifications

Design Tokens (matching frontend palette):
  Primary:  #06b6d4 (cyan)    Secondary: #10b981 (emerald)
  Success:  #10b981            Warning:   #f59e0b
  Danger:   #ef4444            Info:      #06b6d4
  BG dark:  #0f172a            Card:      #1e293b
"""

import io
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def generate_roadmap_pdf(roadmap_data: Dict[str, Any], candidate_name: Optional[str] = None) -> bytes:
    """
    Generates a premium multi-page PDF career report.
    Returns raw PDF bytes.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm, mm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, PageBreak, KeepTogether
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
        from reportlab.platypus.flowables import HRFlowable
    except ImportError:
        raise RuntimeError("ReportLab is not installed. Run: pip install reportlab")

    buffer = io.BytesIO()
    page_w, page_h = A4

    # ── Color Palette ──────────────────────────────────────────────────────────
    C_BG        = colors.white
    C_CARD      = colors.HexColor("#f8fafc")
    C_CARD2     = colors.HexColor("#f1f5f9")
    C_CARD3     = colors.HexColor("#e2e8f0")
    C_PRIMARY   = colors.HexColor("#06b6d4")
    C_PRIMARY2  = colors.HexColor("#10b981")
    C_PRIMARY_D = colors.HexColor("#0891b2")
    C_SUCCESS   = colors.HexColor("#10b981")
    C_SUCCESS_D = colors.HexColor("#059669")
    C_WARNING   = colors.HexColor("#f59e0b")
    C_WARNING_D = colors.HexColor("#d97706")
    C_ERROR     = colors.HexColor("#ef4444")
    C_INFO      = colors.HexColor("#06b6d4")
    C_INFO_D    = colors.HexColor("#0891b2")
    C_WHITE     = colors.white
    C_TEXT      = colors.HexColor("#0f172a")
    C_MUTED     = colors.HexColor("#475569")
    C_SUBTLE    = colors.HexColor("#64748b")
    C_BORDER    = colors.HexColor("#e2e8f0")
    C_ACCENT    = colors.HexColor("#0891b2")
    C_COVER_BG  = colors.HexColor("#f1f5f9")   # light cover strip

    # ── Typography Styles ──────────────────────────────────────────────────────
    styles = getSampleStyleSheet()

    def mk(name, base="Normal", **kwargs):
        return ParagraphStyle(name, parent=styles[base], **kwargs)

    # Cover page
    cover_eyebrow = mk("CoverEyebrow", fontSize=9, textColor=C_ACCENT,
                        fontName="Helvetica", spaceAfter=6, alignment=TA_CENTER,
                        letterSpacing=2)
    cover_title   = mk("CoverTitle",  "Heading1", fontSize=30, textColor=C_TEXT,
                        fontName="Helvetica-Bold", spaceAfter=4, alignment=TA_CENTER,
                        leading=38)
    cover_role    = mk("CoverRole",   fontSize=15, textColor=C_ACCENT,
                        fontName="Helvetica-Bold", spaceAfter=2, alignment=TA_CENTER)
    cover_meta    = mk("CoverMeta",   fontSize=9,  textColor=C_MUTED,
                        fontName="Helvetica", spaceAfter=3, alignment=TA_CENTER)
    cover_tagline = mk("CoverTag",    fontSize=8,  textColor=C_SUBTLE,
                        fontName="Helvetica", spaceAfter=2, alignment=TA_CENTER,
                        leading=12)

    # Headings
    h1 = mk("H1", "Heading1", fontSize=17, textColor=C_TEXT,
             fontName="Helvetica-Bold", spaceBefore=2, spaceAfter=4, leading=22)
    h2 = mk("H2", "Heading2", fontSize=12, textColor=C_ACCENT,
             fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4, leading=16)
    h3 = mk("H3", "Heading3", fontSize=10, textColor=C_TEXT,
             fontName="Helvetica-Bold", spaceBefore=5, spaceAfter=3, leading=14)

    # Body
    body     = mk("Body",    fontSize=9,   textColor=C_TEXT,  fontName="Helvetica",
                  spaceAfter=3, leading=14)
    body_j   = mk("BodyJ",   fontSize=9,   textColor=C_TEXT,  fontName="Helvetica",
                  spaceAfter=3, leading=14, alignment=TA_JUSTIFY)
    muted    = mk("Muted",   fontSize=8,   textColor=C_MUTED, fontName="Helvetica",
                  spaceAfter=2, leading=12)
    label    = mk("Label",   fontSize=8,   textColor=C_PRIMARY, fontName="Helvetica-Bold",
                  spaceAfter=2, spaceBefore=3)
    success_s= mk("SuccessS",fontSize=8.5, textColor=C_SUCCESS, fontName="Helvetica-Bold")
    center   = mk("Center",  fontSize=9,   textColor=C_TEXT,  fontName="Helvetica",
                  alignment=TA_CENTER)
    center_m = mk("CenterM", fontSize=8,   textColor=C_MUTED, fontName="Helvetica",
                  alignment=TA_CENTER)
    right_m  = mk("RightM",  fontSize=8,   textColor=C_MUTED, fontName="Helvetica",
                  alignment=TA_RIGHT)

    # ── Flowable Helpers ───────────────────────────────────────────────────────
    def hr(color=C_PRIMARY, thickness=0.5, space_before=4, space_after=6):
        return HRFlowable(width="100%", thickness=thickness, color=color,
                          spaceBefore=space_before, spaceAfter=space_after)

    def sp(h=0.3):
        return Spacer(1, h * cm)

    # ── Section Header Band ────────────────────────────────────────────────────
    def section_header(title: str, icon: str = "", accent: colors.Color = None,
                       subtitle: str = "") -> list:
        """Returns a visually rich section header: colored band + optional subtitle."""
        acc = accent or C_PRIMARY
        # darken variant for left accent cell
        title_text = f"{icon}  {title}" if icon else title
        rows = [[Paragraph(title_text, mk(f"SH_{title[:6]}", fontSize=14,
                                          textColor=C_WHITE, fontName="Helvetica-Bold",
                                          leading=18))]]
        tbl = Table(rows, colWidths=[page_w - 4 * cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), acc),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ]))
        elements = [tbl]
        if subtitle:
            elements.append(Paragraph(subtitle, muted))
        elements.append(sp(0.25))
        return elements

    # ── Score Pill Badge ───────────────────────────────────────────────────────
    def score_pill(label_text: str, value_text: str,
                   accent: colors.Color = None) -> Table:
        """A small colored pill: [LABEL | VALUE] rendered as a 2-cell table."""
        acc = accent or C_PRIMARY
        pill = Table(
            [[Paragraph(label_text, mk(f"PL_{label_text[:4]}", fontSize=7.5,
                                       textColor=C_MUTED, fontName="Helvetica-Bold",
                                       alignment=TA_CENTER)),
              Paragraph(value_text,  mk(f"PV_{label_text[:4]}", fontSize=11,
                                       textColor=C_WHITE, fontName="Helvetica-Bold",
                                       alignment=TA_CENTER))]],
            colWidths=[3.5 * cm, 2.2 * cm]
        )
        pill.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, 0), C_CARD2),
            ("BACKGROUND",    (1, 0), (1, 0), acc),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
            ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return pill

    # ── Standard Table Style ───────────────────────────────────────────────────
    def tbl_style(header_color=C_PRIMARY, alt=True):
        commands = [
            ("BACKGROUND",    (0, 0), (-1, 0),  header_color),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  C_WHITE),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
            ("BACKGROUND",    (0, 1), (-1, -1), C_CARD),
            ("TEXTCOLOR",     (0, 1), (-1, -1), C_TEXT),
            ("GRID",          (0, 0), (-1, -1), 0.4, C_BORDER),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("WORDWRAP",      (0, 0), (-1, -1), True),
        ]
        if alt:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_CARD, C_CARD2]))
        return TableStyle(commands)

    # ── Inline stat row (2-column label/value pair) ────────────────────────────
    def kv_row(k: str, v: str, accent: colors.Color = None) -> Table:
        acc = accent or C_PRIMARY
        t = Table(
            [[Paragraph(k, mk(f"KK_{k[:4]}", fontSize=8, textColor=C_MUTED,
                              fontName="Helvetica-Bold")),
              Paragraph(v, mk(f"KV_{k[:4]}", fontSize=9, textColor=C_TEXT,
                              fontName="Helvetica", alignment=TA_RIGHT))]],
            colWidths=[8 * cm, 8 * cm]
        )
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C_CARD),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("LINEBELOW",     (0, 0), (-1, 0),  0.3, C_BORDER),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return t

    # ── Extract data ───────────────────────────────────────────────────────────
    career          = roadmap_data.get("career", "Career")
    difficulty      = roadmap_data.get("difficulty", "Intermediate")
    total_weeks     = roadmap_data.get("total_weeks", 0)
    total_months    = roadmap_data.get("total_months", 0)
    exp_readiness   = roadmap_data.get("expected_readiness", 92)
    milestones      = roadmap_data.get("milestones", [])
    monthly_roadmap = roadmap_data.get("monthly_roadmap", [])
    progress        = roadmap_data.get("progress", {})
    job_market      = roadmap_data.get("job_market") or {}
    career_forecast = roadmap_data.get("career_forecast") or {}
    skill_gap       = roadmap_data.get("skill_gap") or {}

    curr_readiness  = progress.get("completion_percentage", 0)
    ats_score       = roadmap_data.get("ats_score") or progress.get("ats_score")
    name_str        = candidate_name or "Candidate"
    today           = datetime.now().strftime("%B %d, %Y")
    success_prob    = career_forecast.get("success_probability", 80)
    time_to_ready   = career_forecast.get("time_to_job_ready", f"{total_months} months")
    eligible_roles  = career_forecast.get("eligible_roles", [])
    skills_mastered = career_forecast.get("skills_mastered", 0)
    skills_remaining= career_forecast.get("skills_remaining", 0)

    story = []

    # ============================================================
    # PAGE 1 — COVER
    # ============================================================
    story.append(sp(2.5))
    story.append(Paragraph("ILMORA", cover_eyebrow))
    story.append(sp(0.3))
    story.append(Paragraph("Career Intelligence Report", cover_title))
    story.append(sp(0.2))
    story.append(Paragraph(career, cover_role))
    story.append(hr(C_PRIMARY, 1.2, space_before=6, space_after=6))
    story.append(sp(0.4))

    story.append(Paragraph(f"Prepared for <b>{name_str}</b>", cover_meta))
    story.append(Paragraph(f"Generated on {today}  ·  {difficulty} Level  ·  {total_weeks} weeks", cover_meta))
    story.append(sp(1.2))

    # Score pills row
    pill_items = [
        ("Career Readiness",   f"{curr_readiness}%",    C_SUCCESS),
        ("Target Readiness",   f"{exp_readiness}%",     C_PRIMARY),
        ("Success Probability",f"{success_prob}%",      C_WARNING),
    ]
    if ats_score:
        pill_items.append(("ATS Score", f"{ats_score}%", C_INFO))

    pills_row = [score_pill(lbl, val, acc) for lbl, val, acc in pill_items]
    n_pills = len(pills_row)
    pill_col_w = (page_w - 4 * cm) / n_pills
    pills_tbl = Table([pills_row], colWidths=[pill_col_w] * n_pills)
    pills_tbl.setStyle(TableStyle([
        ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 4),
    ]))
    story.append(pills_tbl)
    story.append(sp(0.8))

    # Key stats compact table
    cover_rows = [
        ["Roadmap Duration",  f"{total_weeks} weeks  ({total_months} months)"],
        ["Skills Mastered",   str(skills_mastered)],
        ["Skills Remaining",  str(skills_remaining)],
        ["Est. Job-Ready",    time_to_ready],
    ]
    ct = Table(cover_rows, colWidths=[8 * cm, 8 * cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_CARD),
        ("TEXTCOLOR",     (0, 0), (0, -1),  C_MUTED),
        ("TEXTCOLOR",     (1, 0), (1, -1),  C_TEXT),
        ("FONTNAME",      (0, 0), (0, -1),  "Helvetica-Bold"),
        ("FONTNAME",      (1, 0), (1, -1),  "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [C_CARD, C_CARD2]),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(ct)
    story.append(sp(0.8))

    if eligible_roles:
        story.append(Paragraph("Target Roles After Completion:", h3))
        story.append(Paragraph(
            "  ·  ".join(eligible_roles[:5]),
            mk("RoleList", fontSize=9, textColor=C_ACCENT, fontName="Helvetica",
               alignment=TA_CENTER, spaceAfter=4)
        ))

    story.append(sp(1.5))
    story.append(Paragraph(
        "This report was automatically generated by the Ilmora platform. "
        "All data is derived from your resume analysis, skill gap assessment, and personalised career roadmap.",
        cover_tagline
    ))
    story.append(PageBreak())

    # ============================================================
    # PAGE 2 — EXECUTIVE SUMMARY
    # ============================================================
    for el in section_header("Executive Summary", "📊", C_SUCCESS,
                              subtitle="Snapshot of your current career readiness and market position"):
        story.append(el)

    # Summary metric table
    exec_data = [
        ["Metric",              "Current",             "Target / Notes"],
        ["Career Readiness",    f"{curr_readiness}%",  f"{exp_readiness}% (target)"],
        ["Success Probability", f"{success_prob}%",    "Based on live market demand"],
        ["Roadmap Duration",    f"{total_weeks} wks",  f"{total_months} months total"],
    ]
    if ats_score:
        exec_data.insert(2, ["ATS Resume Score", f"{ats_score}%", "Resume compatibility score"])
    et = Table(exec_data, colWidths=[6 * cm, 5 * cm, 5.5 * cm])
    et.setStyle(tbl_style(C_SUCCESS))
    story.append(et)
    story.append(sp(0.5))

    # Job market intelligence
    if job_market:
        story.append(Paragraph("💼 Job Market Intelligence", h2))
        india    = job_market.get("india_salary", {})
        glbl     = job_market.get("global_salary", {})
        demand   = job_market.get("demand_level", "High")
        growth   = job_market.get("yoy_growth", "Growing")
        openings = job_market.get("estimated_job_openings", 0)
        remote   = "Yes" if job_market.get("remote_friendly") else "On-site"
        employers= ", ".join(job_market.get("top_employers", [])[:5])

        mkt_data = [
            ["Market",    "Salary Range",              "Demand", "YoY Growth", "Openings"],
            ["🇮🇳 India", india.get("formatted", "—"), demand,   growth,       f"{openings:,}"],
            ["🌍 Global", glbl.get("formatted", "—"),  demand,   growth,       remote],
        ]
        mt = Table(mkt_data, colWidths=[3 * cm, 4 * cm, 2.5 * cm, 2.5 * cm, 3.5 * cm])
        mt.setStyle(tbl_style(C_INFO))
        story.append(mt)
        story.append(sp(0.25))
        if employers:
            story.append(Paragraph(f"🏢 Top Hiring Companies: <b>{employers}</b>", body))

    story.append(sp(0.5))

    # Career Strategy Overview
    story.append(Paragraph("Career Strategy Overview", h2))
    summary_lines = [
        f"• <b>Target Role:</b> {career} — {difficulty} difficulty level",
        f"• <b>Current Readiness:</b> {curr_readiness}% with a target of {exp_readiness}%",
        f"• <b>Timeline:</b> {total_weeks} weeks of structured learning curriculum",
        f"• <b>Milestones:</b> {len(milestones)} major milestones covering all critical skill domains",
        f"• <b>Outcome:</b> {success_prob}% estimated probability of landing a role in {time_to_ready}",
    ]
    if ats_score:
        summary_lines.insert(2, f"• <b>ATS Score:</b> {ats_score}% resume compatibility with industry standards")
    for line in summary_lines:
        story.append(Paragraph(line, body))

    story.append(PageBreak())

    # ============================================================
    # PAGE 3 — SKILL GAP ANALYSIS & RECOMMENDATIONS
    # ============================================================
    for el in section_header("Career Recommendation & Skill Gap", "🎯", C_WARNING,
                              subtitle="Your current skill strengths, gaps, and recommended focus areas"):
        story.append(el)

    if skill_gap:
        matched  = skill_gap.get("matched_skills", [])
        missing  = skill_gap.get("missing_skills", [])
        optional = skill_gap.get("optional_skills", [])

        if matched:
            story.append(Paragraph("✅ Your Matched Skills", h2))
            # Display in compact chip-style rows (3 per row)
            chunks = [matched[i:i+4] for i in range(0, len(matched), 4)]
            for chunk in chunks[:5]:
                chip_row = [[
                    Paragraph(sk, mk(f"Chip{j}", fontSize=8, textColor=C_SUCCESS,
                                     fontName="Helvetica-Bold", alignment=TA_CENTER))
                    for j, sk in enumerate(chunk)
                ]]
                pad = 4 - len(chunk)
                if pad:
                    chip_row[0] += [Paragraph("", body)] * pad
                ct2 = Table(chip_row, colWidths=[(page_w - 4 * cm) / 4] * 4)
                ct2.setStyle(TableStyle([
                    ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#0d2318")),
                    ("TOPPADDING",    (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#1a3a2a")),
                    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
                ]))
                story.append(ct2)
                story.append(sp(0.05))
            story.append(sp(0.3))

        if missing:
            story.append(Paragraph("⚠️ Skills to Acquire", h2))
            miss_data = [["#", "Skill", "Priority", "Action"]]
            for i, skill in enumerate(missing[:12], 1):
                priority = "🔴 High" if i <= 4 else ("🟡 Medium" if i <= 8 else "🟢 Low")
                action   = "Start now" if i <= 4 else ("Queue next" if i <= 8 else "Optional")
                miss_data.append([str(i), skill, priority, action])

            ms_t = Table(miss_data, colWidths=[1 * cm, 8.5 * cm, 3 * cm, 4 * cm])
            ms_t.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, 0),  C_WARNING),
                ("TEXTCOLOR",     (0, 0), (-1, 0),  C_WHITE),
                ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
                ("BACKGROUND",    (0, 1), (-1, -1), C_CARD),
                ("TEXTCOLOR",     (0, 1), (-1, -1), C_TEXT),
                ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_CARD, C_CARD2]),
                ("GRID",          (0, 0), (-1, -1), 0.4, C_BORDER),
                ("TOPPADDING",    (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING",   (0, 0), (-1, -1), 8),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
                ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ]))
            story.append(ms_t)
            story.append(sp(0.3))

        if optional:
            story.append(Paragraph("💡 Optional / Nice-to-Have Skills", h3))
            story.append(Paragraph("  ·  ".join(optional[:10]), muted))
    else:
        if eligible_roles:
            story.append(Paragraph("Eligible Target Roles", h2))
            for role in eligible_roles:
                story.append(Paragraph(f"• {role}", body))
        story.append(sp(0.3))
        story.append(Paragraph(
            "Complete a resume upload and ATS analysis to see your detailed skill gap breakdown.",
            muted
        ))

    story.append(sp(0.5))
    story.append(Paragraph("📌 Recommended Action Areas", h2))
    rec_items = [
        ("ATS Optimization",  "Align resume language precisely with job description keywords"),
        ("Skill Development",  f"Complete all {skills_remaining} remaining skills in the roadmap"),
        ("Portfolio Building", "Build 2–3 showcase projects demonstrating your top-priority skills"),
        ("Interview Practice", "Complete at least 5 mock interviews across all interview types"),
        ("Network Building",   "Connect with professionals in your target role on LinkedIn"),
    ]
    rec_data = [["Action Area", "Recommendation"]] + [[a, r] for a, r in rec_items]
    rt = Table(rec_data, colWidths=[5 * cm, 11.5 * cm])
    rt.setStyle(tbl_style(C_PRIMARY))
    story.append(rt)

    story.append(PageBreak())

    # ============================================================
    # PAGE 4 — MONTHLY LEARNING TIMELINE
    # ============================================================
    for el in section_header("Monthly Learning Timeline", "🗺️", C_INFO,
                              subtitle="Your structured month-by-month curriculum and weekly milestone overview"):
        story.append(el)

    if monthly_roadmap:
        timeline_data = [["Month", "Focus Area", "Core Skills", "Wks"]]
        for month in monthly_roadmap:
            skills_str = ", ".join(month.get("skills", []))[:72]
            timeline_data.append([
                Paragraph(f"Month {month.get('month_number', '?')}",
                          mk("MonthNum", fontSize=8.5, textColor=C_ACCENT,
                             fontName="Helvetica-Bold")),
                Paragraph(month.get("title", ""), body),
                Paragraph(skills_str or "—", muted),
                str(month.get("weeks", 4)),
            ])
        tt = Table(timeline_data, colWidths=[2.5 * cm, 5.5 * cm, 7 * cm, 1.5 * cm])
        tt.setStyle(tbl_style(C_INFO))
        story.append(tt)
    else:
        story.append(Paragraph("No monthly timeline data available for this roadmap.", muted))

    story.append(sp(0.6))
    story.append(Paragraph("📅 Weekly Milestone Overview", h2))

    milestone_summary = [["Milestone", "Duration", "Skills", "Status"]]
    for ms in milestones:
        status   = "✅ Complete" if ms.get("complete") else "⏳ Pending"
        n_skills = len(ms.get("skills", []))
        weeks    = ms.get("duration_weeks", "—")
        milestone_summary.append([
            Paragraph(ms.get("title", "")[:48], body),
            f"{weeks} wks",
            str(n_skills),
            Paragraph(status, success_s if ms.get("complete") else muted),
        ])

    if len(milestone_summary) > 1:
        mst = Table(milestone_summary, colWidths=[8 * cm, 2.5 * cm, 2 * cm, 4 * cm])
        mst.setStyle(tbl_style(C_PRIMARY_D))
        story.append(mst)

    story.append(PageBreak())

    # ============================================================
    # PAGE 5 — MILESTONES & RESOURCES
    # ============================================================
    for el in section_header("Milestones & Learning Resources", "🏆", C_PRIMARY2,
                              subtitle="Detailed breakdown of each milestone, skills, and curated learning resources"):
        story.append(el)

    for i, ms in enumerate(milestones):
        is_done   = ms.get("complete", False)
        status    = "✅ Complete" if is_done else "⏳ In Progress"
        skills    = ", ".join(ms.get("skills", []))
        resources = ms.get("resources", [])
        acc_color = C_SUCCESS if is_done else C_PRIMARY

        # Milestone header bar
        ms_header = Table(
            [[Paragraph(f"{ms.get('title', '')}",
                        mk(f"MS{i}H", fontSize=11, textColor=C_WHITE,
                           fontName="Helvetica-Bold", leading=14)),
              Paragraph(status,
                        mk(f"MS{i}S", fontSize=8.5, textColor=C_WHITE,
                           fontName="Helvetica-Bold", alignment=TA_RIGHT))]],
            colWidths=[12 * cm, 4.5 * cm]
        )
        ms_header.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), acc_color),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))

        block = [ms_header]
        if skills:
            block.append(Paragraph(f"<b>Skills covered:</b> {skills}", muted))
        if resources:
            block.append(Paragraph("Learning Resources:", label))
            res_data = [["Type", "Resource", "URL"]]
            for res in resources[:4]:
                res_data.append([
                    Paragraph(res.get("type", "Course")[:12], muted),
                    Paragraph(res.get("name", "")[:50], body),
                    Paragraph(res.get("url", "")[:42], muted),
                ])
            rt2 = Table(res_data, colWidths=[2 * cm, 7.5 * cm, 7 * cm])
            rt2.setStyle(tbl_style(C_CARD, alt=False))
            block.append(rt2)
        block.append(sp(0.15))
        story.append(KeepTogether(block))

    story.append(PageBreak())

    # ============================================================
    # PAGE 6 — PORTFOLIO PROJECTS
    # ============================================================
    for el in section_header("Recommended Portfolio Projects", "🛠️", C_ERROR,
                              subtitle="Projects to build hands-on experience and impress hiring managers"):
        story.append(el)

    proj_count = 0
    for ms in milestones:
        projects = ms.get("projects", [])
        if not projects:
            continue
        story.append(Paragraph(ms.get("title", ""), h2))
        for proj in projects:
            proj_count += 1
            diff    = proj.get("difficulty", "Intermediate")
            c_diff  = {
                "Advanced":    "#f87171",
                "Intermediate":"#fbbf24",
                "Beginner":    "#34d399"
            }.get(diff, "#94a3b8")
            tech = ", ".join(proj.get("tech", []))

            proj_block = [
                Paragraph(
                    f"<b>{proj_count}. {proj.get('title', '')}</b>  "
                    f"<font color='{c_diff}' size='7.5'>[{diff}]</font>",
                    body
                ),
                Paragraph(proj.get("description", ""), muted),
            ]
            if tech:
                proj_block.append(Paragraph(f"<b>Tech Stack:</b> {tech}", label))
            proj_block.append(sp(0.1))
            story.append(KeepTogether(proj_block))

    if proj_count == 0:
        story.append(Paragraph(
            "No portfolio projects are defined for this roadmap yet. "
            "Check back after completing your first milestone.",
            muted
        ))

    story.append(PageBreak())

    # ============================================================
    # PAGE 7 — ACTION PLAN & CERTIFICATIONS
    # ============================================================
    for el in section_header("Action Plan & Next Steps", "🚀", C_SUCCESS,
                              subtitle="Your personalised 90-day sprint plan and certification roadmap"):
        story.append(el)

    # 30/60/90 day plan
    story.append(Paragraph("📅 30 / 60 / 90 Day Action Plan", h2))
    r30 = min(curr_readiness + 20, 85)
    plan_data = [
        ["Period",         "Goals & Targets"],
        ["First 30 Days",
         f"Complete Month 1 curriculum · Set up local dev environment · "
         f"Upload & optimise resume to ATS standards · Score ≥60% in 2 mock interviews"],
        ["Days 31–60",
         f"Finish Month 2–3 modules · Build first portfolio project · "
         f"Reach {r30}% career readiness · Apply to 5 target roles"],
        ["Days 61–90",
         f"Complete final milestones · Finish all {skills_remaining} remaining skills · "
         f"Achieve target readiness of {exp_readiness}% · Schedule 10 real interviews"],
    ]
    pt = Table(plan_data, colWidths=[3.5 * cm, 13 * cm])
    pt.setStyle(tbl_style(C_SUCCESS))
    story.append(pt)
    story.append(sp(0.5))

    # Certifications
    certs = job_market.get("certification_boost", [])
    if certs:
        story.append(Paragraph("🏅 Recommended Certifications", h2))
        cert_data = [["#", "Certification"]]
        for i, cert in enumerate(certs, 1):
            cert_data.append([str(i), cert])
        cert_t = Table(cert_data, colWidths=[1.5 * cm, 15 * cm])
        cert_t.setStyle(tbl_style(C_PRIMARY2))
        story.append(cert_t)
        story.append(sp(0.4))

    # Interview preparation targets
    story.append(Paragraph("🎤 Interview Preparation Targets", h2))
    interview_plan = [
        ["Interview Type",    "Sessions Target", "Focus Area"],
        ["AI Mock Interview", "3+ sessions",      "Role-specific behavioural questions"],
        ["Technical",         "3+ sessions",      "DSA, System Design, domain topics"],
        ["HR / Culture Fit",  "2 sessions",        "Professional scenarios & values alignment"],
        ["Behavioural (STAR)","2 sessions",        "Leadership, conflict resolution, teamwork"],
        ["Coding Challenges", "5+ sessions",       "Arrays, Trees, Dynamic Programming"],
    ]
    it = Table(interview_plan, colWidths=[5 * cm, 3.5 * cm, 8 * cm])
    it.setStyle(tbl_style(C_PRIMARY2))
    story.append(it)
    story.append(sp(0.6))

    # Closing note
    story.append(hr(C_BORDER, 0.4))
    story.append(sp(0.2))
    story.append(Paragraph(
        f"Report generated by <b>Ilmora</b>  ·  {today}  ·  "
        f"All data is personalised based on your resume, skill gap analysis, and career roadmap.  "
        f"Good luck, {name_str.split()[0]}! 🚀",
        mk("ClosingNote", fontSize=8, textColor=C_MUTED,
           fontName="Helvetica", alignment=TA_CENTER, leading=13)
    ))

    # ── Page decorations (header, footer, watermark) ───────────────────────────
    def add_page_decorations(canvas, doc):
        """Draw running header/footer on every page, watermark, and cover strip."""
        canvas.saveState()
        page_num = doc.page
        W, H     = A4

        # ── COVER PAGE (page 1): branded accent strip at top ────────────────
        if page_num == 1:
            # Dark gradient strip (simulated with a tall rect)
            canvas.setFillColor(C_COVER_BG)
            canvas.rect(0, H - 3.8 * cm, W, 3.8 * cm, fill=True, stroke=False)
            # Accent bottom border of strip
            canvas.setFillColor(C_PRIMARY)
            canvas.rect(0, H - 3.8 * cm, W, 0.18 * cm, fill=True, stroke=False)
            # "CONFIDENTIAL" watermark — faint diagonal text
            canvas.setFillColor(colors.HexColor("#1e293b"))
            canvas.setFont("Helvetica-Bold", 52)
            canvas.saveState()
            canvas.translate(W / 2, H / 2)
            canvas.rotate(35)
            canvas.drawCentredString(0, 0, "CONFIDENTIAL")
            canvas.restoreState()
        else:
            # ── ALL OTHER PAGES: watermark ────────────────────────────────
            canvas.setFillColor(colors.HexColor("#151e2e"))
            canvas.setFont("Helvetica-Bold", 48)
            canvas.saveState()
            canvas.translate(W / 2, H / 2)
            canvas.rotate(35)
            canvas.drawCentredString(0, 0, "CONFIDENTIAL")
            canvas.restoreState()

            # Running header
            canvas.setFont("Helvetica-Bold", 7)
            canvas.setFillColor(C_PRIMARY)
            canvas.drawString(2 * cm, H - 1.2 * cm,
                              "Ilmora – Career Intelligence Report")

            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(C_MUTED)
            canvas.drawRightString(W - 2 * cm, H - 1.2 * cm,
                                   f"Page {page_num}")

            # Header divider
            canvas.setStrokeColor(C_BORDER)
            canvas.setLineWidth(0.3)
            canvas.line(2 * cm, H - 1.45 * cm, W - 2 * cm, H - 1.45 * cm)

        # ── FOOTER (all pages) ────────────────────────────────────────────
        canvas.setStrokeColor(C_BORDER)
        canvas.setLineWidth(0.3)
        canvas.line(2 * cm, 1.25 * cm, W - 2 * cm, 1.25 * cm)

        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(C_MUTED)
        canvas.drawString(2 * cm, 0.85 * cm,
                          f"Prepared for: {name_str}  ·  Target: {career}")
        canvas.drawRightString(W - 2 * cm, 0.85 * cm, today)

        canvas.restoreState()

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"Career Intelligence Report – {name_str}",
        author="Ilmora",
        subject=f"Career Intelligence Report: {career}",
        creator="Ilmora Platform",
    )

    doc.build(story,
              onFirstPage=add_page_decorations,
              onLaterPages=add_page_decorations)
    buffer.seek(0)
    return buffer.read()
