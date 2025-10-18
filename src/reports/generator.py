"""
Report Generation Module - Automated PDF/HTML report generation
"""
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate automated analytics reports"""
    
    def __init__(self, output_dir: str = "reports/generated"):
        """
        Initialize report generator
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles"""
        # Only add if they don't exist
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=TA_CENTER
            ))
        
        if 'SectionHeader' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2e5c8a'),
                spaceAfter=12,
                spaceBefore=12
            ))
        
        if 'BodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='BodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            ))
    
    def generate_comprehensive_report(self, df: pd.DataFrame, metadata: Dict[str, Any],
                                     report_type: str = "comprehensive",
                                     include_visualizations: bool = True) -> Path:
        """
        Generate comprehensive analytics report
        
        Args:
            df: Analyzed DataFrame
            metadata: Dataset metadata
            report_type: Type of report
            include_visualizations: Whether to include charts
            
        Returns:
            Path to generated report
        """
        logger.info(f"Generating {report_type} report")
        
        try:
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analytics_report_{timestamp}.pdf"
            output_path = self.output_dir / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Title page
            story.extend(self._create_title_page(metadata))
            story.append(PageBreak())
            
            # Executive summary
            story.extend(self._create_executive_summary(df, metadata))
            story.append(PageBreak())
            
            # Data overview
            story.extend(self._create_data_overview(df))
            story.append(Spacer(1, 0.2*inch))
            
            # Statistical summary
            story.extend(self._create_statistical_summary(df))
            story.append(Spacer(1, 0.2*inch))
            
            # Key findings
            story.extend(self._create_key_findings(df))
            story.append(PageBreak())
            
            # Recommendations
            story.extend(self._create_recommendations(df))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Report generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    def _create_title_page(self, metadata: Dict[str, Any]) -> List:
        """Create report title page"""
        elements = []
        
        # Add spacing
        elements.append(Spacer(1, 2*inch))
        
        # Title
        title = Paragraph(
            "Analytics Intelligence Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle with dataset info
        subtitle = Paragraph(
            f"<b>Dataset:</b> {metadata.get('filename', 'Unknown')}<br/>"
            f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M')}<br/>"
            f"<b>Records:</b> {metadata.get('rows', 0):,}<br/>"
            f"<b>Variables:</b> {metadata.get('columns', 0)}",
            self.styles['Normal']
        )
        elements.append(subtitle)
        
        return elements
    
    def _create_executive_summary(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> List:
        """Create executive summary section"""
        elements = []
        
        # Section header
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Generate summary text
        summary_text = f"""
        This report provides a comprehensive analysis of the {metadata.get('filename', 'uploaded')} dataset,
        containing {len(df):,} records across {len(df.columns)} variables. The analysis includes descriptive
        statistics, trend identification, correlation analysis, and actionable recommendations.
        
        Key highlights include automated data quality assessment, identification of significant patterns and
        trends, and strategic recommendations for data-driven decision making.
        """
        
        elements.append(Paragraph(summary_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_data_overview(self, df: pd.DataFrame) -> List:
        """Create data overview section"""
        elements = []
        
        elements.append(Paragraph("Data Overview", self.styles['SectionHeader']))
        
        # Create overview table
        overview_data = [
            ['Metric', 'Value'],
            ['Total Records', f"{len(df):,}"],
            ['Total Variables', str(len(df.columns))],
            ['Numeric Variables', str(len(df.select_dtypes(include=['number']).columns))],
            ['Categorical Variables', str(len(df.select_dtypes(include=['object']).columns))],
            ['Missing Values', f"{df.isnull().sum().sum():,}"],
            ['Duplicate Records', f"{df.duplicated().sum():,}"]
        ]
        
        table = Table(overview_data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_statistical_summary(self, df: pd.DataFrame) -> List:
        """Create statistical summary section"""
        elements = []
        
        elements.append(Paragraph("Statistical Summary", self.styles['SectionHeader']))
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            # Create summary for first few numeric columns
            summary_data = [['Variable', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']]
            
            for col in numeric_cols[:5]:  # Limit to first 5 columns
                summary_data.append([
                    col,
                    f"{df[col].mean():.2f}",
                    f"{df[col].median():.2f}",
                    f"{df[col].std():.2f}",
                    f"{df[col].min():.2f}",
                    f"{df[col].max():.2f}"
                ])
            
            table = Table(summary_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No numeric variables found in dataset.", self.styles['Normal']))
        
        return elements
    
    def _create_key_findings(self, df: pd.DataFrame) -> List:
        """Create key findings section"""
        elements = []
        
        elements.append(Paragraph("Key Findings", self.styles['SectionHeader']))
        
        findings = []
        
        # Data quality finding
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct < 5:
            findings.append(f"✓ <b>Data Quality:</b> Excellent - only {missing_pct:.1f}% missing values")
        elif missing_pct < 15:
            findings.append(f"⚠ <b>Data Quality:</b> Good - {missing_pct:.1f}% missing values detected")
        else:
            findings.append(f"⚠ <b>Data Quality:</b> Attention needed - {missing_pct:.1f}% missing values")
        
        # Duplicate finding
        dup_count = df.duplicated().sum()
        if dup_count == 0:
            findings.append("✓ <b>Data Integrity:</b> No duplicate records found")
        else:
            findings.append(f"⚠ <b>Data Integrity:</b> {dup_count:,} duplicate records identified")
        
        # Numeric columns finding
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            findings.append(f"✓ <b>Analytics Readiness:</b> {len(numeric_cols)} numeric variables available for quantitative analysis")
        
        # Add findings as bullet points
        for finding in findings:
            elements.append(Paragraph(finding, self.styles['BodyText']))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_recommendations(self, df: pd.DataFrame) -> List:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        
        recommendations = []
        
        # Data quality recommendations
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 10:
            recommendations.append(
                "1. <b>Data Quality Improvement:</b> Investigate and address missing values, "
                "particularly in critical variables. Consider data imputation strategies or "
                "additional data collection."
            )
        
        # Duplicate recommendations
        if df.duplicated().sum() > 0:
            recommendations.append(
                "2. <b>Data Deduplication:</b> Remove or investigate duplicate records to ensure "
                "accurate analysis and prevent skewed results."
            )
        
        # Analysis recommendations
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) >= 2:
            recommendations.append(
                "3. <b>Deeper Analysis:</b> Conduct correlation analysis and predictive modeling "
                "to uncover relationships between variables and forecast future trends."
            )
        
        recommendations.append(
            "4. <b>Continuous Monitoring:</b> Establish regular analytics cycles to track "
            "changes over time and identify emerging patterns or anomalies."
        )
        
        recommendations.append(
            "5. <b>Stakeholder Engagement:</b> Share insights with relevant stakeholders and "
            "translate findings into actionable business strategies."
        )
        
        # Add recommendations
        for rec in recommendations:
            elements.append(Paragraph(rec, self.styles['BodyText']))
            elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def generate_executive_summary(self, analysis_results: Dict[str, Any],
                                   output_format: str = "pdf") -> Path:
        """
        Generate concise executive summary
        
        Args:
            analysis_results: Complete analysis results
            output_format: Output format ('pdf' or 'html')
            
        Returns:
            Path to generated summary
        """
        logger.info(f"Generating executive summary in {output_format} format")
        
        # Implementation for executive summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"executive_summary_{timestamp}.{output_format}"
        output_path = self.output_dir / filename
        
        # For now, return a placeholder
        with open(output_path, 'w') as f:
            f.write(json.dumps(analysis_results, indent=2))
        
        return output_path

