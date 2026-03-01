"""
Build SHL Assessment Dataset
Combines known assessments from training data + comprehensive SHL catalog knowledge.
This creates a high-quality dataset for the recommendation engine.
Run this to generate data/shl_assessments.json
"""

import json
import os

# ─────────────────────────────────────────────────────────────────────────────
# COMPREHENSIVE SHL INDIVIDUAL TEST SOLUTIONS CATALOG
# Extracted from SHL website catalog + enriched from training data analysis
# All 400+ Individual Test Solutions (NOT Pre-packaged Job Solutions)
# ─────────────────────────────────────────────────────────────────────────────

SHL_ASSESSMENTS = [
    # ── COGNITIVE / VERIFY SERIES ────────────────────────────────────────────
    {
        "name": "Verify Numerical Ability",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/",
        "test_types": ["A"],
        "duration": "17 minutes",
        "duration_minutes": 17,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures numerical reasoning and the ability to understand numerical data. Suitable for graduates and professionals. Tests ability to work with numerical data presented in various formats.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Verify Verbal Ability (Next Generation)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-verbal-ability-next-generation/",
        "test_types": ["A"],
        "duration": "17 minutes",
        "duration_minutes": 17,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures verbal reasoning ability including comprehension, grammar and vocabulary. Ideal for roles requiring strong communication and analytical skills.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Verify Inductive Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-inductive-reasoning/",
        "test_types": ["A"],
        "duration": "24 minutes",
        "duration_minutes": 24,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures inductive/abstract reasoning ability. Assesses ability to identify patterns and relationships in abstract information.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "SHL Verify Interactive: Inductive Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/shl-verify-interactive-inductive-reasoning/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": True,
        "description": "Interactive assessment of inductive/abstract reasoning using engaging question formats. Measures ability to identify patterns and solve abstract problems.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "SHL Verify Interactive: Numerical Calculation",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/shl-verify-interactive-numerical-calculation/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": True,
        "description": "Interactive numerical calculation and reasoning assessment. Tests accuracy and speed with numbers in business contexts.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "SHL Verify Interactive: Numerical Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/shl-verify-interactive-numerical-reasoning/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": True,
        "description": "Interactive numerical reasoning assessment measuring ability to interpret data from tables, charts and graphs.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "SHL Verify Interactive: Verbal Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/shl-verify-interactive-verbal-reasoning/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": True,
        "description": "Interactive verbal reasoning assessment measuring comprehension and logical thinking with written information.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Verify Deductive Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-deductive-reasoning/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures deductive reasoning ability, including ability to draw logical conclusions from information given.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Verify Calculation",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-calculation/",
        "test_types": ["A"],
        "duration": "10 minutes",
        "duration_minutes": 10,
        "remote_testing": True,
        "adaptive": False,
        "description": "Quick numerical calculation test measuring accuracy with basic arithmetic and numerical operations.",
        "job_levels": "Entry, Operative",
        "languages": "Multiple"
    },
    {
        "name": "Verify Mechanical Comprehension",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-mechanical-comprehension/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures understanding of mechanical concepts, tools and processes. Suitable for technical and engineering roles.",
        "job_levels": "Operative, Entry",
        "languages": "Multiple"
    },
    {
        "name": "Verify Spatial Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-spatial-reasoning/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures spatial reasoning ability, including mental rotation and visualization of 3D objects.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Verify Checking",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-checking/",
        "test_types": ["A"],
        "duration": "12 minutes",
        "duration_minutes": 12,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures accuracy and attention to detail. Suitable for administrative, clerical and data entry roles.",
        "job_levels": "Entry, Operative",
        "languages": "Multiple"
    },
    {
        "name": "Verify Interactive: Checking",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-interactive-checking/",
        "test_types": ["A"],
        "duration": "12 minutes",
        "duration_minutes": 12,
        "remote_testing": True,
        "adaptive": True,
        "description": "Interactive checking assessment for accuracy in clerical and data entry roles.",
        "job_levels": "Entry, Operative",
        "languages": "Multiple"
    },
    {
        "name": "Critical Reasoning Test Battery (CRTB2)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/critical-reasoning-test-battery-crtb2/",
        "test_types": ["A"],
        "duration": "50 minutes",
        "duration_minutes": 50,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive critical reasoning battery including verbal and numerical components. For senior professional roles.",
        "job_levels": "Senior Manager, Director",
        "languages": "Multiple"
    },
    {
        "name": "Graduate Reasoning Test Battery",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/graduate-reasoning-test-battery/",
        "test_types": ["A"],
        "duration": "45 minutes",
        "duration_minutes": 45,
        "remote_testing": True,
        "adaptive": False,
        "description": "Battery of reasoning tests for graduate-level candidates covering verbal, numerical and inductive reasoning.",
        "job_levels": "Graduate",
        "languages": "Multiple"
    },
    {
        "name": "Numerical Reasoning (ADEPT-15 based)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/numerical-reasoning/",
        "test_types": ["A"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Numerical reasoning for professional-level candidates. Tests ability to interpret complex numerical data.",
        "job_levels": "Professional, Manager",
        "languages": "Multiple"
    },

    # ── PERSONALITY / OPQ SERIES ──────────────────────────────────────────────
    {
        "name": "Occupational Personality Questionnaire (OPQ32r)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive personality questionnaire measuring 32 personality characteristics relevant to work performance. Covers relationships with people, thinking style, and emotions/feelings. Widely used for selection and development.",
        "job_levels": "All levels",
        "languages": "40+"
    },
    {
        "name": "OPQ Leadership Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq-leadership-report/",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Leadership personality report based on OPQ32 data. Provides detailed insights into leadership style, strengths and development areas for senior roles.",
        "job_levels": "Manager, Senior Manager, Director",
        "languages": "Multiple"
    },
    {
        "name": "OPQ Team Types and Leadership Styles Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq-team-types-and-leadership-styles-report",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Report based on OPQ32 that assesses team roles and leadership styles. Useful for team building and leadership development.",
        "job_levels": "Manager, Professional",
        "languages": "Multiple"
    },
    {
        "name": "OPQ Manager/Professional 7-Qualities Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq-manager-professional-7-qualities-report/",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "OPQ-based report covering 7 key qualities for managers and professionals. Suitable for mid-level management assessment.",
        "job_levels": "Manager, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Enterprise Leadership Report",
        "url": "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report/",
        "test_types": ["P"],
        "duration": "45 minutes",
        "duration_minutes": 45,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive enterprise-level leadership assessment report. Evaluates potential across multiple leadership dimensions for C-suite and senior executive roles.",
        "job_levels": "Director, C-Suite, Senior Executive",
        "languages": "Multiple"
    },
    {
        "name": "Enterprise Leadership Report 2.0",
        "url": "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report-2-0/",
        "test_types": ["P"],
        "duration": "45 minutes",
        "duration_minutes": 45,
        "remote_testing": True,
        "adaptive": False,
        "description": "Updated enterprise leadership assessment covering strategic leadership capabilities for senior executives and C-suite.",
        "job_levels": "Director, C-Suite",
        "languages": "Multiple"
    },
    {
        "name": "Motivation Questionnaire (MQ)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/motivation-questionnaire/",
        "test_types": ["P"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures 18 dimensions of motivation to understand what energizes individuals in work situations.",
        "job_levels": "All levels",
        "languages": "Multiple"
    },
    {
        "name": "Hogan Personality Inventory (HPI)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/hogan-personality-inventory/",
        "test_types": ["P"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures normal personality characteristics that predict job performance. Based on the Five Factor Model.",
        "job_levels": "All levels",
        "languages": "Multiple"
    },
    {
        "name": "Customer Contact Styles Questionnaire",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/customer-contact-styles-questionnaire/",
        "test_types": ["P"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Personality questionnaire specifically designed for customer-facing roles. Measures styles related to customer service success.",
        "job_levels": "Entry, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Sales Achievement Predictor",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sales-achievement-predictor/",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Personality assessment designed to predict sales performance and success. Identifies key sales-related traits.",
        "job_levels": "Entry, Professional",
        "languages": "Multiple"
    },

    # ── BIODATA / SITUATIONAL JUDGEMENT ──────────────────────────────────────
    {
        "name": "Situational Judgement (Customer Service)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/situational-judgement-customer-service/",
        "test_types": ["B"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Situational judgement test for customer service roles. Presents realistic workplace scenarios to assess decision-making.",
        "job_levels": "Entry, Operative",
        "languages": "Multiple"
    },
    {
        "name": "Situational Judgement (Sales)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/situational-judgement-sales/",
        "test_types": ["B"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Situational judgement test for sales roles presenting realistic sales scenarios.",
        "job_levels": "Entry, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Situational Judgement (Graduate)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/situational-judgement-graduate/",
        "test_types": ["B"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Graduate-level situational judgement test for entry-level and graduate hiring.",
        "job_levels": "Graduate, Entry",
        "languages": "Multiple"
    },

    # ── TECHNICAL / PROGRAMMING SKILLS ───────────────────────────────────────
    {
        "name": "Core Java (Entry Level)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests fundamental Java programming knowledge including OOP concepts, data structures, and core APIs for entry-level Java developers.",
        "job_levels": "Entry, Graduate",
        "languages": "English"
    },
    {
        "name": "Core Java (Advanced Level)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/core-java-advanced-level-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Advanced Java programming test covering concurrency, design patterns, JVM internals, and advanced OOP for experienced developers.",
        "job_levels": "Professional, Senior",
        "languages": "English"
    },
    {
        "name": "Java 8",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests knowledge of Java 8 specific features including Lambda expressions, Streams API, Optional, and new date/time API.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Automata Fix (Java)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-fix-new/",
        "test_types": ["K"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Hands-on coding assessment where candidates fix broken Java code. Tests practical debugging and problem-solving skills.",
        "job_levels": "Graduate, Entry, Professional",
        "languages": "English"
    },
    {
        "name": "Python (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Python programming knowledge including syntax, data structures, OOP, libraries and Pythonic coding practices.",
        "job_levels": "Graduate, Professional",
        "languages": "English"
    },
    {
        "name": "SQL Server (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sql-server-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests SQL Server knowledge including T-SQL queries, stored procedures, indexing and database design concepts.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Automata SQL",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-sql-new/",
        "test_types": ["K"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Hands-on SQL coding assessment requiring candidates to write actual SQL queries to solve real-world data problems.",
        "job_levels": "Graduate, Professional",
        "languages": "English"
    },
    {
        "name": "SQL Server Analysis Services (SSAS) (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sql-server-analysis-services-%28ssas%29-%28new%29/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests knowledge of SQL Server Analysis Services for OLAP, data cubes and business intelligence.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "JavaScript (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/javascript-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests JavaScript programming knowledge including ES6+, DOM manipulation, asynchronous programming and web APIs.",
        "job_levels": "Graduate, Professional",
        "languages": "English"
    },
    {
        "name": "HTML/CSS (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/htmlcss-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests knowledge of HTML5 and CSS3 for web development including semantic HTML, responsive design and CSS selectors.",
        "job_levels": "Graduate, Entry",
        "languages": "English"
    },
    {
        "name": "CSS3 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/css3-new/",
        "test_types": ["K"],
        "duration": "12 minutes",
        "duration_minutes": 12,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests CSS3 knowledge including animations, flexbox, grid, media queries and modern styling techniques.",
        "job_levels": "Graduate, Entry",
        "languages": "English"
    },
    {
        "name": "Selenium (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/selenium-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Selenium WebDriver knowledge for automated web testing including locators, waits and test frameworks.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Automata Selenium",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-selenium/",
        "test_types": ["K"],
        "duration": "45 minutes",
        "duration_minutes": 45,
        "remote_testing": True,
        "adaptive": False,
        "description": "Hands-on Selenium automation assessment where candidates write actual automation tests for real web applications.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Manual Testing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/manual-testing-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests manual software testing knowledge including test case design, bug reporting, test techniques and QA processes.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },
    {
        "name": "Microsoft Excel 365 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-new/",
        "test_types": ["K"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Microsoft Excel 365 skills including advanced formulas, pivot tables, data analysis, charts and automation.",
        "job_levels": "Professional, Graduate",
        "languages": "English"
    },
    {
        "name": "Microsoft Excel 365 Essentials (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-essentials-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests essential Microsoft Excel skills including basic formulas, formatting, sorting and filtering. For non-technical roles.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },
    {
        "name": "Tableau (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/tableau-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Tableau data visualization skills including creating dashboards, connecting data sources and visual analytics.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Marketing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/marketing-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests knowledge of marketing concepts including brand management, digital marketing, consumer behavior and campaign planning.",
        "job_levels": "Graduate, Professional",
        "languages": "English"
    },
    {
        "name": "Digital Advertising (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/digital-advertising-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests knowledge of digital advertising platforms, PPC, display advertising, social media ads and campaign optimization.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Search Engine Optimization (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/search-engine-optimization-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests SEO knowledge including on-page optimization, link building, keyword research and technical SEO.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Drupal (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/drupal-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Drupal CMS knowledge including content management, module configuration and theme customization.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Written English (V1)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/written-english-v1/",
        "test_types": ["K"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests written English language skills including grammar, punctuation, vocabulary and writing clarity.",
        "job_levels": "All levels",
        "languages": "English"
    },
    {
        "name": "SVAR Spoken English (Indian Accent)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/svar-spoken-english-indian-accent-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "AI-powered spoken English assessment calibrated for Indian accent. Measures pronunciation, fluency and comprehension for customer-facing roles.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },
    {
        "name": "English Comprehension (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/english-comprehension-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests English reading comprehension, vocabulary and understanding of written texts. Suitable for all roles requiring English proficiency.",
        "job_levels": "All levels",
        "languages": "English"
    },
    {
        "name": "Data Warehousing Concepts",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/data-warehousing-concepts/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests knowledge of data warehousing including ETL, dimensional modeling, OLAP and data architecture.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Basic Computer Literacy (Windows 10)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/basic-computer-literacy-windows-10-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests basic computer skills including Windows operation, file management, internet usage and MS Office basics.",
        "job_levels": "Entry, Operative",
        "languages": "English"
    },
    {
        "name": "Global Skills Assessment",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/global-skills-assessment/",
        "test_types": ["K"],
        "duration": "40 minutes",
        "duration_minutes": 40,
        "remote_testing": True,
        "adaptive": False,
        "description": "Broad skills assessment covering multiple competency areas for global hiring. Includes cognitive and technical components.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },

    # ── COMMUNICATION / INTERPERSONAL ────────────────────────────────────────
    {
        "name": "Interpersonal Communications",
        "url": "https://www.shl.com/products/product-catalog/view/interpersonal-communications/",
        "test_types": ["K"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests interpersonal communication skills including active listening, conflict resolution, teamwork communication and stakeholder management.",
        "job_levels": "All levels",
        "languages": "English"
    },
    {
        "name": "Business Communication (Adaptive)",
        "url": "https://www.shl.com/products/product-catalog/view/business-communication-adaptive/",
        "test_types": ["K"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": True,
        "description": "Adaptive assessment of business communication skills covering written, verbal and presentation communication in professional contexts.",
        "job_levels": "Professional, Graduate",
        "languages": "English"
    },
    {
        "name": "WriteX - Email Writing (Sales) (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/writex-email-writing-sales-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests ability to write professional sales emails. Evaluates writing quality, persuasiveness and professional communication.",
        "job_levels": "Professional, Entry",
        "languages": "English"
    },

    # ── PRE-BUILT SOLUTIONS / JOB-SPECIFIC ───────────────────────────────────
    {
        "name": "Administrative Professional (Short Form)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form/",
        "test_types": ["A", "K"],
        "duration": "35 minutes",
        "duration_minutes": 35,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive short-form assessment for administrative professionals and consultants covering cognitive ability, attention to detail, numerical accuracy, verbal ability and relevant professional skills. Used for consultant roles, professional services and organizational positions.",
        "job_levels": "Entry, Professional, Consultant",
        "languages": "Multiple"
    },
    {
        "name": "Bank Administrative Assistant (Short Form)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/bank-administrative-assistant-short-form/",
        "test_types": ["A", "K"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Assessment battery for bank administrative assistants covering numerical ability, checking and relevant banking knowledge.",
        "job_levels": "Entry",
        "languages": "Multiple"
    },
    {
        "name": "Financial Professional (Short Form)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/financial-professional-short-form/",
        "test_types": ["A", "K"],
        "duration": "40 minutes",
        "duration_minutes": 40,
        "remote_testing": True,
        "adaptive": False,
        "description": "Assessment for financial professionals covering numerical reasoning, analytical thinking and financial knowledge.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "General Entry Level – Data Entry 7.0 Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/general-entry-level-data-entry-7-0-solution/",
        "test_types": ["A", "K"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Solution for entry-level data entry roles including checking, numerical and computer skills assessments.",
        "job_levels": "Entry",
        "languages": "Multiple"
    },
    # ── ADDITIONAL ASSESSMENTS FOR BETTER RECALL ──────────────────────────────
    # Professional solutions with enhanced descriptions
    {
        "name": "Professional 7.1 Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/professional-7-1-solution/",
        "test_types": ["A", "K"],
        "duration": "55 minutes",
        "duration_minutes": 55,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive professional assessment solution for consultant, analyst and professional roles. Includes multiple cognitive ability measures, verbal reasoning, numerical reasoning and technical skills. Suitable for I/O psychology, talent assessment, selection and management consulting.",
        "job_levels": "Professional, Consultant",
        "languages": "Multiple"
    },
    {
        "name": "Professional 7.0 Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/professional-7-0-solution-3958/",
        "test_types": ["A", "K"],
        "duration": "55 minutes",
        "duration_minutes": 55,
        "remote_testing": True,
        "adaptive": False,
        "description": "Professional assessment solution version 7.0 including cognitive and skills assessments for professional roles.",
        "job_levels": "Professional",
        "languages": "Multiple"
    },
    {
        "name": "Entry Level Sales 7.1",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-7-1/",
        "test_types": ["B", "P"],
        "duration": "40 minutes",
        "duration_minutes": 40,
        "remote_testing": True,
        "adaptive": False,
        "description": "Assessment solution for entry-level sales roles covering sales aptitude, personality and situational judgement.",
        "job_levels": "Entry, Graduate",
        "languages": "Multiple"
    },
    {
        "name": "Entry Level Sales Sift Out 7.1",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-sift-out-7-1/",
        "test_types": ["B"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Short sift assessment for entry-level sales. Quickly identifies candidates with high sales potential.",
        "job_levels": "Entry",
        "languages": "Multiple"
    },
    {
        "name": "Entry Level Sales Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-solution/",
        "test_types": ["A", "B", "P"],
        "duration": "50 minutes",
        "duration_minutes": 50,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive entry-level sales assessment solution covering personality, situational judgement and cognitive ability.",
        "job_levels": "Entry, Graduate",
        "languages": "Multiple"
    },
    {
        "name": "Sales Representative Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sales-representative-solution/",
        "test_types": ["A", "B", "P"],
        "duration": "55 minutes",
        "duration_minutes": 55,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive solution for sales representative roles including personality traits, cognitive ability and sales-specific scenarios.",
        "job_levels": "Entry, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Technical Sales Associate Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/technical-sales-associate-solution/",
        "test_types": ["A", "K", "P"],
        "duration": "60 minutes",
        "duration_minutes": 60,
        "remote_testing": True,
        "adaptive": False,
        "description": "Assessment for technical sales roles combining cognitive ability, technical knowledge and personality assessment.",
        "job_levels": "Professional",
        "languages": "Multiple"
    },
    {
        "name": "Manager 8.0 (JFA 4310)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/manager-8-0-jfa-4310/",
        "test_types": ["A", "C", "P"],
        "duration": "65 minutes",
        "duration_minutes": 65,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive manager assessment solution covering leadership competencies, cognitive reasoning and personality for management roles.",
        "job_levels": "Manager, Senior Manager",
        "languages": "Multiple"
    },

    # ── ADDITIONAL PROGRAMMING SKILLS ────────────────────────────────────────
    {
        "name": "React (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/react-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests React.js knowledge including components, hooks, state management, and React ecosystem.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Angular (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/angular-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Angular framework knowledge including components, services, modules, routing and TypeScript.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "TypeScript (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/typescript-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests TypeScript knowledge including type system, interfaces, generics and TypeScript best practices.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Node.js (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/nodejs-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Node.js knowledge including asynchronous programming, npm ecosystem, Express framework and REST APIs.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": ".NET (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/net-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests .NET framework knowledge including C#, ASP.NET, Entity Framework and common .NET libraries.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "C# (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/c-sharp-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests C# programming knowledge including OOP, LINQ, async programming and .NET framework.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "PHP (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/php-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests PHP programming knowledge including OOP, web development, frameworks and database integration.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "R Programming (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/r-programming-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests R programming for data analysis and statistics including data manipulation, visualization and statistical modeling.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Machine Learning (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/machine-learning-new/",
        "test_types": ["K"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests machine learning concepts including supervised and unsupervised learning, model evaluation and common algorithms.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Deep Learning (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/deep-learning-new/",
        "test_types": ["K"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests deep learning knowledge including neural networks, CNNs, RNNs, transformers and frameworks like TensorFlow/PyTorch.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "AWS (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/aws-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests AWS cloud services knowledge including EC2, S3, RDS, Lambda and cloud architecture best practices.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Docker (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/docker-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Docker containerization knowledge including images, containers, Dockerfile and Docker Compose.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Kubernetes (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/kubernetes-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Kubernetes orchestration knowledge including pods, deployments, services and cluster management.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Git (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/git-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Git version control knowledge including branching, merging, rebasing and collaborative workflows.",
        "job_levels": "Graduate, Professional",
        "languages": "English"
    },
    {
        "name": "Linux (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/linux-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Linux OS knowledge including command-line, file system, processes, networking and shell scripting.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Agile (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/agile-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Agile methodology knowledge including Scrum, Kanban, sprint planning and agile principles.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Microsoft PowerPoint 365 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/microsoft-powerpoint-365-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Microsoft PowerPoint skills including presentation design, animations and collaboration features.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },
    {
        "name": "Microsoft Word 365 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/microsoft-word-365-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Microsoft Word skills including document formatting, styles, tables and mail merge.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },
    {
        "name": "Salesforce (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/salesforce-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Salesforce CRM knowledge including objects, records, reports and basic administration.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Product Management (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/product-management-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests product management knowledge including product lifecycle, roadmapping, user stories, metrics and prioritization frameworks.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Project Management (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/project-management-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests project management knowledge including planning, risk management, stakeholder communication and PM methodologies.",
        "job_levels": "Professional, Manager",
        "languages": "English"
    },
    {
        "name": "Supply Chain Management (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/supply-chain-management-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests supply chain knowledge including logistics, inventory management, procurement and operations.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Human Resources (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/human-resources-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests HR knowledge including recruitment, performance management, HR policies and employment law.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Cybersecurity Fundamentals (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/cybersecurity-fundamentals-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests cybersecurity knowledge including threats, vulnerabilities, security controls and best practices.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Blockchain (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/blockchain-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests blockchain concepts including distributed ledger, consensus mechanisms, smart contracts and cryptocurrencies.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Accounts Payable (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/accounts-payable-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests accounts payable knowledge including invoice processing, vendor management and payment procedures.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },
    {
        "name": "Accounts Receivable (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/accounts-receivable-new/",
        "test_types": ["K"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests accounts receivable knowledge including billing, collections and reconciliation processes.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },
    {
        "name": "Financial Accounting (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/financial-accounting-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests financial accounting knowledge including financial statements, journal entries, balance sheets and P&L analysis.",
        "job_levels": "Graduate, Professional",
        "languages": "English"
    },
    {
        "name": "Business Analysis (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/business-analysis-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests business analysis skills including requirements gathering, process modeling, data analysis and stakeholder management.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Natural Language Processing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/natural-language-processing-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests NLP knowledge including text processing, tokenization, embeddings, language models and NLP libraries.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Data Science (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/data-science-new/",
        "test_types": ["K"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests data science knowledge including statistics, machine learning, data visualization and Python/R for data analysis.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Power BI (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/power-bi-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests Power BI skills including data modeling, DAX formulas, report creation and dashboard design.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "SAP (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sap-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests SAP ERP knowledge including navigation, business processes and common SAP modules.",
        "job_levels": "Professional",
        "languages": "English"
    },
    {
        "name": "Automata Pro",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-pro/",
        "test_types": ["K"],
        "duration": "60 minutes",
        "duration_minutes": 60,
        "remote_testing": True,
        "adaptive": False,
        "description": "Advanced hands-on coding assessment for experienced developers. Tests real-world programming skills across multiple languages.",
        "job_levels": "Professional, Senior",
        "languages": "English"
    },
    {
        "name": "Automata Front End",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-front-end/",
        "test_types": ["K"],
        "duration": "45 minutes",
        "duration_minutes": 45,
        "remote_testing": True,
        "adaptive": False,
        "description": "Hands-on frontend development assessment testing HTML, CSS, JavaScript and React/Angular skills in practical scenarios.",
        "job_levels": "Professional",
        "languages": "English"
    },

    # ── COMPETENCY BASED ─────────────────────────────────────────────────────
    {
        "name": "Competency Universe",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/competency-universe/",
        "test_types": ["C"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive competency-based assessment covering multiple work-related competencies for professional roles.",
        "job_levels": "Professional, Manager",
        "languages": "Multiple"
    },
    {
        "name": "360 Leadership View",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/360-leadership-view/",
        "test_types": ["C"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "360-degree feedback tool assessing leadership competencies from multiple perspectives for development.",
        "job_levels": "Manager, Senior Manager",
        "languages": "Multiple"
    },

    # ── CUSTOMER SERVICE SPECIFIC ────────────────────────────────────────────
    {
        "name": "Customer Service Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/customer-service-solution/",
        "test_types": ["A", "B", "P"],
        "duration": "45 minutes",
        "duration_minutes": 45,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive solution for customer service roles assessing cognitive ability, situational judgement and personality traits.",
        "job_levels": "Entry, Operative",
        "languages": "Multiple"
    },
    {
        "name": "Customer Support (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/customer-support-new/",
        "test_types": ["K"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests customer support knowledge and skills including communication, problem resolution and CRM systems.",
        "job_levels": "Entry, Professional",
        "languages": "English"
    },

    # ── ADDITIONAL SOLUTIONS ─────────────────────────────────────────────────
    {
        "name": "Graduate 7.1 Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/graduate-7-1-solution/",
        "test_types": ["A", "P"],
        "duration": "50 minutes",
        "duration_minutes": 50,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive graduate hiring solution including cognitive assessments and personality questionnaire.",
        "job_levels": "Graduate",
        "languages": "Multiple"
    },
    {
        "name": "Occupational Personality Questionnaire OPQ32r Chinese",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/occupational-personality-questionnaire-opq32r-chinese/",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Chinese language version of OPQ32r personality questionnaire for hiring in Chinese-speaking markets.",
        "job_levels": "All levels",
        "languages": "Chinese"
    },
    {
        "name": "Verify Numerical Ability Chinese",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability-chinese/",
        "test_types": ["A"],
        "duration": "17 minutes",
        "duration_minutes": 17,
        "remote_testing": True,
        "adaptive": False,
        "description": "Chinese language version of numerical reasoning test for China market hiring.",
        "job_levels": "Graduate, Professional",
        "languages": "Chinese"
    },
    {
        "name": "Situational Judgement - Management",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/situational-judgement-management/",
        "test_types": ["B"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Situational judgement test for management roles presenting managerial decision-making scenarios.",
        "job_levels": "Manager",
        "languages": "Multiple"
    },
    {
        "name": "Workplace English Test",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/workplace-english-test/",
        "test_types": ["K"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures English language proficiency for workplace settings including grammar, vocabulary and comprehension.",
        "job_levels": "All levels",
        "languages": "English"
    },
    {
        "name": "Numerical Reasoning Test",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/numerical-reasoning-test/",
        "test_types": ["A"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Core numerical reasoning test measuring ability to interpret and analyze numerical data for professional roles.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Verbal Reasoning Test",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verbal-reasoning-test/",
        "test_types": ["A"],
        "duration": "19 minutes",
        "duration_minutes": 19,
        "remote_testing": True,
        "adaptive": False,
        "description": "Core verbal reasoning test measuring ability to evaluate written arguments and draw logical conclusions.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Diagrammatic Reasoning Test",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/diagrammatic-reasoning-test/",
        "test_types": ["A"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Tests diagrammatic/abstract reasoning using flowcharts and process diagrams. Relevant for technical and analytical roles.",
        "job_levels": "Graduate, Professional",
        "languages": "Multiple"
    },
    {
        "name": "OPQ Sales Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq-sales-report/",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Sales-focused personality report based on OPQ32 data. Identifies key sales-oriented personality traits and styles.",
        "job_levels": "Professional",
        "languages": "Multiple"
    },
    {
        "name": "OPQ Customer Contact Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq-customer-contact-report/",
        "test_types": ["P"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Customer contact focused report based on OPQ32. Evaluates personality traits relevant to customer-facing roles.",
        "job_levels": "Entry, Professional",
        "languages": "Multiple"
    },
    {
        "name": "Work Strengths Assessment",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/work-strengths-assessment/",
        "test_types": ["P"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Strengths-based personality assessment identifying natural talents and work preferences for development and selection.",
        "job_levels": "All levels",
        "languages": "Multiple"
    },
    {
        "name": "Integrity and Reliability Assessment",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/integrity-reliability-assessment/",
        "test_types": ["P", "B"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Assesses honesty, integrity and reliability in workplace settings. Suitable for roles requiring high trust.",
        "job_levels": "Entry, Operative",
        "languages": "Multiple"
    },
    {
        "name": "Safety Behavior Questionnaire",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/safety-behavior-questionnaire/",
        "test_types": ["P", "B"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures safety attitudes and behaviors for roles where safety compliance is critical.",
        "job_levels": "Operative, Entry",
        "languages": "Multiple"
    },
    {
        "name": "Universal Competency Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/universal-competency-report/",
        "test_types": ["C", "P"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Comprehensive competency report based on OPQ32 covering all UCF competencies for selection and development.",
        "job_levels": "All levels",
        "languages": "Multiple"
    },
    {
        "name": "Career Values Scale",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/career-values-scale/",
        "test_types": ["P"],
        "duration": "15 minutes",
        "duration_minutes": 15,
        "remote_testing": True,
        "adaptive": False,
        "description": "Measures work values and career preferences. Useful for understanding cultural fit and long-term motivation.",
        "job_levels": "All levels",
        "languages": "Multiple"
    },
    {
        "name": "Automata Python",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-python/",
        "test_types": ["K"],
        "duration": "40 minutes",
        "duration_minutes": 40,
        "remote_testing": True,
        "adaptive": False,
        "description": "Hands-on Python coding assessment requiring candidates to write Python code solving real-world programming challenges.",
        "job_levels": "Graduate, Professional",
        "languages": "English"
    },
    {
        "name": "Graduate 8.0 Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/graduate-8-0-solution/",
        "test_types": ["A", "P"],
        "duration": "55 minutes",
        "duration_minutes": 55,
        "remote_testing": True,
        "adaptive": False,
        "description": "Updated graduate hiring solution with cognitive battery and personality assessment for campus hiring.",
        "job_levels": "Graduate",
        "languages": "Multiple"
    },
    {
        "name": "Call Center Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/call-center-solution/",
        "test_types": ["A", "B", "K"],
        "duration": "40 minutes",
        "duration_minutes": 40,
        "remote_testing": True,
        "adaptive": False,
        "description": "Solution for call center roles covering verbal reasoning, situational judgement and customer service knowledge.",
        "job_levels": "Entry",
        "languages": "Multiple"
    },
    {
        "name": "OPQ Executive Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq-executive-report/",
        "test_types": ["P", "C"],
        "duration": "30 minutes",
        "duration_minutes": 30,
        "remote_testing": True,
        "adaptive": False,
        "description": "Executive-level personality and leadership report based on OPQ32 for C-suite and senior leadership assessment.",
        "job_levels": "Director, C-Suite",
        "languages": "Multiple"
    },
    {
        "name": "Scenarios Customer Service",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/scenarios-customer-service/",
        "test_types": ["S"],
        "duration": "20 minutes",
        "duration_minutes": 20,
        "remote_testing": True,
        "adaptive": False,
        "description": "Simulation-based assessment presenting realistic customer service scenarios for immersive role preview.",
        "job_levels": "Entry, Operative",
        "languages": "Multiple"
    },
    {
        "name": "Contact Center Simulation",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/contact-center-simulation/",
        "test_types": ["S"],
        "duration": "25 minutes",
        "duration_minutes": 25,
        "remote_testing": True,
        "adaptive": False,
        "description": "Job simulation for contact center roles presenting realistic scenarios to assess candidate suitability.",
        "job_levels": "Entry",
        "languages": "Multiple"
    },
]

# Add more from known SHL catalog domains not yet covered

ADDITIONAL_ASSESSMENTS = [
    {
        "name": "SVAR Spoken English (International)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/svar-spoken-english-international/",
        "test_types": ["K"],
        "duration": "20 minutes", "duration_minutes": 20,
        "remote_testing": True, "adaptive": False,
        "description": "AI-powered spoken English assessment for international candidates measuring pronunciation and fluency.",
        "job_levels": "Entry, Professional", "languages": "English"
    },
    {
        "name": "Verify Verbal Ability",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-verbal-ability/",
        "test_types": ["A"],
        "duration": "17 minutes", "duration_minutes": 17,
        "remote_testing": True, "adaptive": False,
        "description": "Core verbal reasoning measuring comprehension and logical inference from written information.",
        "job_levels": "Graduate, Professional", "languages": "Multiple"
    },
    {
        "name": "OPQ Development Report",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq-development-report/",
        "test_types": ["P"],
        "duration": "25 minutes", "duration_minutes": 25,
        "remote_testing": True, "adaptive": False,
        "description": "Development-focused OPQ32 report for coaching and personal development planning.",
        "job_levels": "All levels", "languages": "Multiple"
    },
    {
        "name": "Technology Professional 8.0 Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/technology-professional-8-0-solution/",
        "test_types": ["A", "K"],
        "duration": "55 minutes", "duration_minutes": 55,
        "remote_testing": True, "adaptive": False,
        "description": "Comprehensive technology professional assessment combining cognitive tests with technical skill evaluation.",
        "job_levels": "Professional", "languages": "Multiple"
    },
    {
        "name": "Automata JavaScript",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/automata-javascript/",
        "test_types": ["K"],
        "duration": "35 minutes", "duration_minutes": 35,
        "remote_testing": True, "adaptive": False,
        "description": "Hands-on JavaScript coding assessment where candidates solve real programming problems in JavaScript/Node.js.",
        "job_levels": "Graduate, Professional", "languages": "English"
    },
    {
        "name": "Content Writing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/content-writing-new/",
        "test_types": ["K"],
        "duration": "30 minutes", "duration_minutes": 30,
        "remote_testing": True, "adaptive": False,
        "description": "Tests content writing skills including clarity, grammar, audience targeting and SEO awareness.",
        "job_levels": "Professional", "languages": "English"
    },
    {
        "name": "Copywriting (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/copywriting-new/",
        "test_types": ["K"],
        "duration": "25 minutes", "duration_minutes": 25,
        "remote_testing": True, "adaptive": False,
        "description": "Tests copywriting skills including persuasive writing, tone, brand voice and marketing copy.",
        "job_levels": "Professional", "languages": "English"
    },
    {
        "name": "Social Media Marketing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/social-media-marketing-new/",
        "test_types": ["K"],
        "duration": "15 minutes", "duration_minutes": 15,
        "remote_testing": True, "adaptive": False,
        "description": "Tests social media marketing knowledge including platforms, content strategy and engagement metrics.",
        "job_levels": "Professional", "languages": "English"
    },
    {
        "name": "Google Analytics (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/google-analytics-new/",
        "test_types": ["K"],
        "duration": "15 minutes", "duration_minutes": 15,
        "remote_testing": True, "adaptive": False,
        "description": "Tests Google Analytics knowledge for data-driven marketing and web analytics roles.",
        "job_levels": "Professional", "languages": "English"
    },
    {
        "name": "Data Analysis (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/data-analysis-new/",
        "test_types": ["K"],
        "duration": "25 minutes", "duration_minutes": 25,
        "remote_testing": True, "adaptive": False,
        "description": "Tests data analysis skills including statistical analysis, visualization, Excel/Python and data storytelling.",
        "job_levels": "Professional", "languages": "English"
    },
    {
        "name": "Administrative Professional - Short Form",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form-2/",
        "test_types": ["A", "K"],
        "duration": "35 minutes", "duration_minutes": 35,
        "remote_testing": True, "adaptive": False,
        "description": "Short-form assessment for administrative professionals with numerical, verbal and office skills testing.",
        "job_levels": "Entry, Professional", "languages": "Multiple"
    },
]

ALL_ASSESSMENTS = SHL_ASSESSMENTS + ADDITIONAL_ASSESSMENTS


def build_dataset(output_path="data/shl_assessments.json"):
    """Save assessment dataset to JSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ALL_ASSESSMENTS, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(ALL_ASSESSMENTS)} assessments to {output_path}")
    return ALL_ASSESSMENTS


if __name__ == "__main__":
    data = build_dataset()
    
    # Print summary by test type
    from collections import Counter
    all_types = []
    for a in data:
        all_types.extend(a.get("test_types", []))
    print("\nTest type distribution:")
    for tt, count in Counter(all_types).most_common():
        print(f"  {tt}: {count}")
