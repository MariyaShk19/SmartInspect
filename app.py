import streamlit as st
import pandas as pd
import numpy as np

# Optional: used for formal Chi-Square tests
try:
    from scipy.stats import chi2_contingency
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartInspect | Inspection Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    :root {
        --bg: #F5F7FA;
        --card: #FFFFFF;
        --navy: #172B4D;
        --blue: #2F80ED;
        --blue-dark: #1F5FB8;
        --teal: #159A9C;
        --green: #2E7D5B;
        --red: #D64545;
        --amber: #D99A2B;
        --text: #172B4D;
        --muted: #64748B;
        --border: #E2E8F0;
        --soft-blue: #EEF5FF;
        --soft-green: #EEF8F3;
        --soft-red: #FFF1F1;
        --soft-amber: #FFF8E8;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stAppViewContainer"] {
        background: var(--bg);
    }

    [data-testid="stHeader"] {
        background: rgba(245, 247, 250, 0.92);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Typography ---------- */
    h1, h2, h3, h4 {
        color: var(--navy) !important;
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        font-weight: 700 !important;
    }

    p, label, span, div {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    p {
        color: var(--muted);
    }

    /* ---------- Header ---------- */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        padding: 6px 0 20px 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 24px;
    }

    .brand-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-mark {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        background: var(--navy);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 5px 14px rgba(23, 43, 77, 0.14);
    }

    .brand-name {
        color: var(--navy);
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 7px 11px;
        border-radius: 999px;
        background: var(--soft-green);
        color: var(--green);
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #D7EDE2;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--green);
    }

    /* ---------- Hero ---------- */
    .hero {
        background: linear-gradient(135deg, #172B4D 0%, #243F68 100%);
        border-radius: 18px;
        padding: 30px 34px;
        margin-bottom: 26px;
        box-shadow: 0 10px 28px rgba(23, 43, 77, 0.13);
        position: relative;
        overflow: hidden;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 50%;
        right: -70px;
        top: -95px;
    }

    .hero-kicker {
        color: #9FC5FF;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.7px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: 31px;
        font-weight: 750;
        letter-spacing: -0.8px;
        margin: 0 0 9px 0;
    }

    .hero-text {
        color: #DCE8F8;
        font-size: 14px;
        line-height: 1.65;
        max-width: 850px;
        margin: 0;
    }

    /* ---------- Section headers ---------- */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 26px 0 13px 0;
    }

    .section-bar {
        width: 4px;
        height: 22px;
        background: var(--blue);
        border-radius: 3px;
    }

    .section-title-text {
        color: var(--navy);
        font-size: 19px;
        font-weight: 750;
    }

    .section-description {
        color: var(--muted);
        font-size: 13px;
        margin: -5px 0 16px 14px;
    }

    /* ---------- Metric cards ---------- */
    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 17px 18px;
        min-height: 112px;
        box-shadow: 0 3px 12px rgba(23, 43, 77, 0.035);
    }

    .metric-label {
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.75px;
        margin-bottom: 7px;
    }

    .metric-value {
        color: var(--navy);
        font-size: 27px;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-caption {
        color: #94A3B8;
        font-size: 11px;
        margin-top: 7px;
    }

    /* ---------- Info cards ---------- */
    .info-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 3px 12px rgba(23, 43, 77, 0.035);
        height: 100%;
    }

    .info-card-title {
        color: var(--navy);
        font-size: 14px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .info-card-text {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.55;
    }

    /* ---------- Upload ---------- */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--card) !important;
        border: 1.5px dashed #AFC4DF !important;
        border-radius: 14px !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--blue) !important;
        background: #FBFDFF !important;
    }

    /* ---------- Tabs ---------- */
    [data-baseweb="tab-list"] {
        gap: 4px;
        background: #EAF0F7;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid var(--border);
    }

    [data-baseweb="tab"] {
        color: #64748B !important;
        border-radius: 8px;
        font-weight: 650 !important;
        font-size: 13px !important;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        color: var(--navy) !important;
        box-shadow: 0 2px 7px rgba(23, 43, 77, 0.08);
    }

    /* ---------- Buttons ---------- */
    .stButton > button,
    .stDownloadButton > button {
        background: var(--navy) !important;
        color: white !important;
        border: 1px solid var(--navy) !important;
        border-radius: 9px !important;
        font-weight: 650 !important;
        transition: 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: var(--blue) !important;
        border-color: var(--blue) !important;
    }

    /* ---------- Inputs ---------- */
    .stTextInput input {
        background: var(--card) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 9px !important;
    }

    .stTextInput input:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 1px var(--blue) !important;
    }

    /* ---------- Dataframes ---------- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    /* ---------- Alerts ---------- */
    .stAlert {
        border-radius: 10px !important;
    }

    /* ---------- Formula cards ---------- */
    .formula-card {
        background: var(--soft-blue);
        border: 1px solid #D7E7FB;
        border-radius: 12px;
        padding: 17px 19px;
        text-align: center;
        height: 100%;
    }

    .formula-label {
        color: var(--blue-dark);
        font-size: 11px;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 8px;
    }

    .formula {
        color: var(--navy);
        font-size: 20px;
        font-weight: 750;
    }

    /* ---------- Tag ---------- */
    .tag {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 750;
        margin-right: 5px;
    }

    .tag-blue {
        background: var(--soft-blue);
        color: var(--blue-dark);
    }

    .tag-green {
        background: var(--soft-green);
        color: var(--green);
    }

    .tag-red {
        background: var(--soft-red);
        color: var(--red);
    }

    /* ---------- Footer ---------- */
    .footer {
        border-top: 1px solid var(--border);
        margin-top: 38px;
        padding-top: 18px;
        text-align: center;
        color: #94A3B8;
        font-size: 10px;
        font-weight: 650;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    /* ---------- Hide unnecessary Streamlit chrome ---------- */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 800px) {
        .brand-header {
            align-items: flex-start;
        }

        .status-pill {
            display: none;
        }

        .hero {
            padding: 24px;
        }

        .hero-title {
            font-size: 25px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def section_header(title, description=None):
    st.markdown(
        f"""
        <div class="section-title">
            <div class="section-bar"></div>
            <div class="section-title-text">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if description:
        st.markdown(
            f'<div class="section-description">{description}</div>',
            unsafe_allow_html=True,
        )


def metric_card(label, value, caption=None):
    caption_html = (
        f'<div class="metric-caption">{caption}</div>'
        if caption
        else ""
    )
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title, text):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-card-title">{title}</div>
            <div class="info-card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# BRAND HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-header">
        <div class="brand-left">
            <div class="brand-mark">◈</div>
            <div>
                <div class="brand-name">SMARTINSPECT</div>
                <div class="brand-subtitle">Multi-Stage Inspection Analytics · Probability 2</div>
            </div>
        </div>
        <div class="status-pill">
            <span class="status-dot"></span>
            Statistical Analysis
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Quality Analytics Platform</div>
        <div class="hero-title">Understand inspection outcomes before problems become patterns.</div>
        <p class="hero-text">
            SmartInspect analyzes multi-stage product inspection data using
            descriptive statistics, probability, conditional probability,
            pairwise independence, mutual independence and failure-pattern analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# UPLOAD SECTION
# ============================================================

section_header(
    "Inspection Dataset",
    "Upload a CSV containing Product_ID, Stage_1, Stage_2 and Stage_3.",
)

uploaded_file = st.file_uploader(
    "Choose your CSV file",
    type=["csv"],
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "Required columns: Product_ID, Stage_1, Stage_2, Stage_3. "
        "Stage values must be Pass or Fail."
    )

    section_header(
        "Analysis Workflow",
        "SmartInspect follows a simple four-step analytical process.",
    )

    w1, w2, w3, w4 = st.columns(4)

    with w1:
        info_card(
            "01 · Upload",
            "Import the inspection dataset in CSV format.",
        )

    with w2:
        info_card(
            "02 · Measure",
            "Summarize product outcomes and failure rates.",
        )

    with w3:
        info_card(
            "03 · Analyse",
            "Calculate probabilities and test independence.",
        )

    with w4:
        info_card(
            "04 · Interpret",
            "Review patterns and statistical evidence.",
        )

    st.markdown(
        """
        <div class="footer">
            SMARTINSPECT · STATISTICAL QUALITY ANALYTICS · SY BSc IT
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ============================================================
# READ CSV
# ============================================================

try:
    df = pd.read_csv(uploaded_file)
except Exception as error:
    st.error(f"Unable to read the CSV file: {error}")
    st.stop()


# ============================================================
# VALIDATE COLUMNS
# ============================================================

required_columns = [
    "Product_ID",
    "Stage_1",
    "Stage_2",
    "Stage_3",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )
    st.info(
        "Your CSV must contain: Product_ID, Stage_1, Stage_2, Stage_3"
    )
    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

stage_columns = [
    "Stage_1",
    "Stage_2",
    "Stage_3",
]

for stage in stage_columns:
    df[stage] = (
        df[stage]
        .astype(str)
        .str.strip()
        .str.title()
    )


# ============================================================
# VALIDATE PASS / FAIL
# ============================================================

valid_values = {"Pass", "Fail"}
invalid_values = {}

for stage in stage_columns:
    values = set(df[stage].dropna().unique())
    invalid = values - valid_values

    if invalid:
        invalid_values[stage] = invalid

if invalid_values:
    st.error("Invalid values were found.")

    for stage, values in invalid_values.items():
        st.write(
            f"**{stage}:** {', '.join(map(str, values))}"
        )

    st.info("Only Pass and Fail are accepted.")
    st.stop()


# ============================================================
# BASIC DATA
# ============================================================

total_products = len(df)

if total_products == 0:
    st.error("The uploaded dataset is empty.")
    st.stop()


# ============================================================
# FAILURE COUNTS
# ============================================================

failure_counts = {}
pass_counts = {}
failure_rates = {}

for stage in stage_columns:
    failure_counts[stage] = int(
        (df[stage] == "Fail").sum()
    )

    pass_counts[stage] = int(
        (df[stage] == "Pass").sum()
    )

    failure_rates[stage] = (
        failure_counts[stage] / total_products * 100
    )


# ============================================================
# EVENTS
# ============================================================

A = df["Stage_1"] == "Fail"
B = df["Stage_2"] == "Fail"
C = df["Stage_3"] == "Fail"

# Individual probabilities
P_A = A.mean()
P_B = B.mean()
P_C = C.mean()

# Joint probabilities
P_AB = (A & B).mean()
P_AC = (A & C).mean()
P_BC = (B & C).mean()
P_ABC = (A & B & C).mean()


# ============================================================
# DATASET SNAPSHOT
# ============================================================

section_header(
    "Dataset Snapshot",
    "A quick view of the uploaded inspection dataset.",
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    metric_card("Total Products", f"{total_products:,}")

with m2:
    metric_card(
        "Stage 1 Failures",
        f"{failure_counts['Stage_1']:,}",
        f"{failure_rates['Stage_1']:.2f}% failure rate",
    )

with m3:
    metric_card(
        "Stage 2 Failures",
        f"{failure_counts['Stage_2']:,}",
        f"{failure_rates['Stage_2']:.2f}% failure rate",
    )

with m4:
    metric_card(
        "Stage 3 Failures",
        f"{failure_counts['Stage_3']:,}",
        f"{failure_rates['Stage_3']:.2f}% failure rate",
    )


# ============================================================
# NAVIGATION
# ============================================================

(
    overview_tab,
    statistics_tab,
    probability_tab,
    independence_tab,
    patterns_tab,
    data_tab,
) = st.tabs(
    [
        "Overview",
        "Statistics",
        "Probability",
        "Independence",
        "Patterns",
        "Data",
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with overview_tab:
    section_header(
        "Inspection Overview",
        "Compare product failure behaviour across the three inspection stages.",
    )

    failure_rate_df = pd.DataFrame(
        {
            "Stage": [
                "Stage 1",
                "Stage 2",
                "Stage 3",
            ],
            "Failures": [
                failure_counts["Stage_1"],
                failure_counts["Stage_2"],
                failure_counts["Stage_3"],
            ],
            "Passes": [
                pass_counts["Stage_1"],
                pass_counts["Stage_2"],
                pass_counts["Stage_3"],
            ],
            "Failure Rate (%)": [
                failure_rates["Stage_1"],
                failure_rates["Stage_2"],
                failure_rates["Stage_3"],
            ],
        }
    )

    chart_col, table_col = st.columns([1.15, 1])

    with chart_col:
        st.markdown("#### Failure Rate by Stage")
        st.bar_chart(
            failure_rate_df.set_index("Stage")["Failure Rate (%)"]
        )

    with table_col:
        st.markdown("#### Stage Summary")
        st.dataframe(
            failure_rate_df.style.format(
                {"Failure Rate (%)": "{:.2f}"}
            ),
            use_container_width=True,
            hide_index=True,
        )

    section_header(
        "Dataset Health",
        "Basic validation checks for the uploaded data.",
    )

    duplicate_ids = int(
        df["Product_ID"].duplicated().sum()
    )

    missing_values = int(
        df.isnull().sum().sum()
    )

    h1, h2, h3, h4 = st.columns(4)

    with h1:
        metric_card("Rows", f"{len(df):,}")

    with h2:
        metric_card("Columns", f"{len(df.columns):,}")

    with h3:
        metric_card("Duplicate IDs", f"{duplicate_ids:,}")

    with h4:
        metric_card("Missing Values", f"{missing_values:,}")

    section_header(
        "Automated Insights",
        "Simple observations generated directly from the uploaded data.",
    )

    highest_stage = max(
        failure_rates,
        key=failure_rates.get,
    )

    lowest_stage = min(
        failure_rates,
        key=failure_rates.get,
    )

    complete_failures = int(
        (A & B & C).sum()
    )

    i1, i2, i3 = st.columns(3)

    with i1:
        st.info(
            f"{highest_stage.replace('_', ' ')} has the highest "
            f"failure rate at {failure_rates[highest_stage]:.2f}%."
        )

    with i2:
        st.info(
            f"{lowest_stage.replace('_', ' ')} has the lowest "
            f"failure rate at {failure_rates[lowest_stage]:.2f}%."
        )

    with i3:
        st.info(
            f"{complete_failures} products failed all three stages."
        )


# ============================================================
# STATISTICS
# ============================================================

with statistics_tab:
    section_header(
        "Statistical Profile",
        "Descriptive statistics calculated after binary encoding of inspection outcomes.",
    )

    numeric_df = df[stage_columns].replace(
        {
            "Pass": 0,
            "Fail": 1,
        }
    )

    statistics_rows = []

    for stage in stage_columns:
        values = numeric_df[stage]

        mode_values = values.mode()

        mode_value = (
            mode_values.iloc[0]
            if len(mode_values) > 0
            else np.nan
        )

        statistics_rows.append(
            {
                "Stage": stage.replace("_", " "),
                "Mean": values.mean(),
                "Median": values.median(),
                "Mode": mode_value,
                "Variance": values.var(),
                "Standard Deviation": values.std(),
                "Minimum": values.min(),
                "Maximum": values.max(),
            }
        )

    statistics_df = pd.DataFrame(statistics_rows)

    st.dataframe(
        statistics_df.style.format(
            {
                "Mean": "{:.3f}",
                "Median": "{:.3f}",
                "Mode": "{:.0f}",
                "Variance": "{:.3f}",
                "Standard Deviation": "{:.3f}",
                "Minimum": "{:.0f}",
                "Maximum": "{:.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    section_header(
        "Pass vs Fail Distribution",
        "Pass = 0 and Fail = 1 for numerical statistical calculations.",
    )

    distribution_df = pd.DataFrame(
        {
            "Stage 1": [
                pass_counts["Stage_1"],
                failure_counts["Stage_1"],
            ],
            "Stage 2": [
                pass_counts["Stage_2"],
                failure_counts["Stage_2"],
            ],
            "Stage 3": [
                pass_counts["Stage_3"],
                failure_counts["Stage_3"],
            ],
        },
        index=["Pass", "Fail"],
    )

    st.bar_chart(distribution_df)

    with st.expander("Why are Pass and Fail converted into numbers?"):
        st.write(
            "To calculate mathematical statistics, inspection results "
            "are represented using binary encoding."
        )
        st.write("Pass = 0")
        st.write("Fail = 1")
        st.write(
            "This allows SmartInspect to calculate measures such as "
            "mean, variance and standard deviation."
        )


# ============================================================
# PROBABILITY
# ============================================================

with probability_tab:
    section_header(
        "Probability Analysis",
        "Measure the likelihood of individual and combined inspection failures.",
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        metric_card(
            "P(A)",
            f"{P_A:.3f}",
            "Probability of Stage 1 failure",
        )

    with p2:
        metric_card(
            "P(B)",
            f"{P_B:.3f}",
            "Probability of Stage 2 failure",
        )

    with p3:
        metric_card(
            "P(C)",
            f"{P_C:.3f}",
            "Probability of Stage 3 failure",
        )

    section_header(
        "Joint Probability",
        "Probability that two or more inspection stages fail together.",
    )

    probability_df = pd.DataFrame(
        {
            "Event": [
                "A ∩ B",
                "A ∩ C",
                "B ∩ C",
                "A ∩ B ∩ C",
            ],
            "Meaning": [
                "Stage 1 and Stage 2 fail",
                "Stage 1 and Stage 3 fail",
                "Stage 2 and Stage 3 fail",
                "All three stages fail",
            ],
            "Probability": [
                P_AB,
                P_AC,
                P_BC,
                P_ABC,
            ],
        }
    )

    st.dataframe(
        probability_df.style.format(
            {"Probability": "{:.3f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    section_header(
        "Conditional Probability",
        "Probability of a later-stage failure given an earlier-stage failure.",
    )

    P_B_given_A = (
        P_AB / P_A
        if P_A != 0
        else 0
    )

    P_C_given_A = (
        P_AC / P_A
        if P_A != 0
        else 0
    )

    P_C_given_B = (
        P_BC / P_B
        if P_B != 0
        else 0
    )

    conditional_df = pd.DataFrame(
        {
            "Conditional Event": [
                "P(B | A)",
                "P(C | A)",
                "P(C | B)",
            ],
            "Probability": [
                P_B_given_A,
                P_C_given_A,
                P_C_given_B,
            ],
        }
    )

    st.dataframe(
        conditional_df.style.format(
            {"Probability": "{:.3f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "Example: P(B | A) means the probability of failing Stage 2 "
        "given that the product already failed Stage 1."
    )


# ============================================================
# INDEPENDENCE
# ============================================================

with independence_tab:
    section_header(
        "Independence Analysis",
        "Compare observed joint probabilities with values expected under independence.",
    )

    # ---------- Pairwise ----------
    st.markdown("#### Pairwise Independence")
    st.caption(
        "For independent events, P(A ∩ B) should equal P(A) × P(B)."
    )

    expected_AB = P_A * P_B
    expected_AC = P_A * P_C
    expected_BC = P_B * P_C

    pairwise_df = pd.DataFrame(
        {
            "Event Pair": [
                "A & B",
                "A & C",
                "B & C",
            ],
            "Observed Probability": [
                P_AB,
                P_AC,
                P_BC,
            ],
            "Expected if Independent": [
                expected_AB,
                expected_AC,
                expected_BC,
            ],
            "Absolute Difference": [
                abs(P_AB - expected_AB),
                abs(P_AC - expected_AC),
                abs(P_BC - expected_BC),
            ],
        }
    )

    st.dataframe(
        pairwise_df.style.format(
            {
                "Observed Probability": "{:.3f}",
                "Expected if Independent": "{:.3f}",
                "Absolute Difference": "{:.3f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    # ---------- Chi-square ----------
    st.markdown("#### Chi-Square Independence Test")

    if not SCIPY_AVAILABLE:
        st.warning(
            "SciPy is not installed. Run 'pip install scipy' "
            "to enable the Chi-Square test."
        )
    else:
        chi_results = []

        pairs = [
            (
                "Stage 1 × Stage 2",
                "Stage_1",
                "Stage_2",
            ),
            (
                "Stage 1 × Stage 3",
                "Stage_1",
                "Stage_3",
            ),
            (
                "Stage 2 × Stage 3",
                "Stage_2",
                "Stage_3",
            ),
        ]

        for name, col1, col2 in pairs:
            contingency = pd.crosstab(
                df[col1],
                df[col2],
            )

            chi2, p_value, degrees, expected = (
                chi2_contingency(contingency)
            )

            phi = (
                np.sqrt(chi2 / total_products)
                if total_products > 0
                else 0
            )

            if p_value < 0.05:
                interpretation = "Evidence of association"
            else:
                interpretation = "No significant association detected"

            chi_results.append(
                {
                    "Comparison": name,
                    "Chi-Square": chi2,
                    "p-value": p_value,
                    "Phi": phi,
                    "Interpretation": interpretation,
                }
            )

        chi_df = pd.DataFrame(chi_results)

        st.dataframe(
            chi_df.style.format(
                {
                    "Chi-Square": "{:.3f}",
                    "p-value": "{:.4f}",
                    "Phi": "{:.3f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "A p-value below 0.05 provides statistical evidence "
            "of an association between the two stages. A p-value "
            "above 0.05 means the test did not detect significant "
            "evidence of association."
        )

    # ---------- Contingency tables ----------
    section_header(
        "Contingency Tables",
        "Observed combinations of Pass and Fail outcomes for each pair of stages.",
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**Stage 1 × Stage 2**")
        table_12 = pd.crosstab(
            df["Stage_1"],
            df["Stage_2"],
        )
        st.dataframe(
            table_12,
            use_container_width=True,
        )

    with c2:
        st.markdown("**Stage 1 × Stage 3**")
        table_13 = pd.crosstab(
            df["Stage_1"],
            df["Stage_3"],
        )
        st.dataframe(
            table_13,
            use_container_width=True,
        )

    with c3:
        st.markdown("**Stage 2 × Stage 3**")
        table_23 = pd.crosstab(
            df["Stage_2"],
            df["Stage_3"],
        )
        st.dataframe(
            table_23,
            use_container_width=True,
        )

    # ---------- Mutual independence ----------
    section_header(
        "Mutual Independence",
        "Compare the observed three-event probability with the value expected under mutual independence.",
    )

    expected_ABC = P_A * P_B * P_C

    mutual_difference = abs(
        P_ABC - expected_ABC
    )

    mutual_df = pd.DataFrame(
        {
            "Measure": [
                "Observed P(A ∩ B ∩ C)",
                "Expected if Mutually Independent",
                "Absolute Difference",
            ],
            "Value": [
                P_ABC,
                expected_ABC,
                mutual_difference,
            ],
        }
    )

    st.dataframe(
        mutual_df.style.format(
            {"Value": "{:.4f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    if mutual_difference <= 0.05:
        st.success(
            "The observed and expected three-event probabilities "
            "are relatively close. The dataset is approximately "
            "consistent with mutual independence."
        )
    else:
        st.warning(
            "The observed and expected three-event probabilities "
            "differ noticeably, suggesting possible dependence."
        )

    st.caption(
        "The 0.05 difference rule is an educational approximation "
        "and is not a formal hypothesis test for mutual independence."
    )


# ============================================================
# PATTERNS
# ============================================================

with patterns_tab:
    section_header(
        "Inspection Failure Patterns",
        "Represent each product as a three-stage sequence to identify repeated outcome patterns.",
    )

    def create_pattern(row):
        stage1 = (
            "F"
            if row["Stage_1"] == "Fail"
            else "P"
        )

        stage2 = (
            "F"
            if row["Stage_2"] == "Fail"
            else "P"
        )

        stage3 = (
            "F"
            if row["Stage_3"] == "Fail"
            else "P"
        )

        return f"{stage1} → {stage2} → {stage3}"

    df["Inspection_Pattern"] = df.apply(
        create_pattern,
        axis=1,
    )

    pattern_counts = (
        df["Inspection_Pattern"]
        .value_counts()
        .rename_axis("Pattern")
        .reset_index(name="Products")
    )

    pattern_counts["Percentage"] = (
        pattern_counts["Products"]
        / total_products
        * 100
    )

    st.markdown("#### Pattern Distribution")

    chart_col, table_col = st.columns([1.1, 1])

    with chart_col:
        st.bar_chart(
            pattern_counts.set_index("Pattern")["Products"]
        )

    with table_col:
        st.dataframe(
            pattern_counts.style.format(
                {"Percentage": "{:.2f}%"}
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.info(
        "Pattern key: P = Pass and F = Fail. "
        "For example, F → P → F means Fail, Pass, Fail."
    )

    section_header(
        "Failure Combinations",
        "Count products that fail at specific combinations of inspection stages.",
    )

    only_stage_1 = int(
        (A & ~B & ~C).sum()
    )

    only_stage_2 = int(
        (~A & B & ~C).sum()
    )

    only_stage_3 = int(
        (~A & ~B & C).sum()
    )

    stages_1_2 = int(
        (A & B & ~C).sum()
    )

    stages_1_3 = int(
        (A & ~B & C).sum()
    )

    stages_2_3 = int(
        (~A & B & C).sum()
    )

    all_three = int(
        (A & B & C).sum()
    )

    failure_combination_df = pd.DataFrame(
        {
            "Failure Combination": [
                "Only Stage 1",
                "Only Stage 2",
                "Only Stage 3",
                "Stages 1 & 2",
                "Stages 1 & 3",
                "Stages 2 & 3",
                "All Three Stages",
            ],
            "Products": [
                only_stage_1,
                only_stage_2,
                only_stage_3,
                stages_1_2,
                stages_1_3,
                stages_2_3,
                all_three,
            ],
        }
    )

    st.dataframe(
        failure_combination_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# DATA
# ============================================================

with data_tab:
    section_header(
        "Inspection Dataset",
        "Search individual products and export the analysis results.",
    )

    search = st.text_input(
        "Search Product ID",
        placeholder="Type a Product ID...",
    )

    if search:
        filtered_df = df[
            df["Product_ID"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False,
            )
        ]
    else:
        filtered_df = df

    st.caption(
        f"Showing {len(filtered_df):,} of {len(df):,} records."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

    section_header(
        "Download Results",
        "Export the original dataset and calculated analysis tables.",
    )

    d1, d2, d3 = st.columns(3)

    with d1:
        st.download_button(
            "Download Dataset",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="smartinspect_dataset.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with d2:
        st.download_button(
            "Download Statistics",
            data=statistics_df.to_csv(index=False).encode("utf-8"),
            file_name="smartinspect_statistics.csv",
            mime="text/csv",
            use_container_width=True,
        )

    probability_export = pd.DataFrame(
        {
            "Measure": [
                "P(A)",
                "P(B)",
                "P(C)",
                "P(A and B)",
                "P(A and C)",
                "P(B and C)",
                "P(A and B and C)",
            ],
            "Value": [
                P_A,
                P_B,
                P_C,
                P_AB,
                P_AC,
                P_BC,
                P_ABC,
            ],
        }
    )

    with d3:
        st.download_button(
            "Download Probability",
            data=probability_export.to_csv(index=False).encode("utf-8"),
            file_name="smartinspect_probability.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        SMARTINSPECT · MULTI-STAGE INSPECTION ANALYTICS · PROBABILITY 2 · SY BSc IT
    </div>
    """,
    unsafe_allow_html=True,
)
