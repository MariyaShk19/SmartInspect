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
    page_title="SmartInspect",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #F7F4EF;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #F7F4EF;
    }

    [data-testid="stHeader"] {
        background-color: #F7F4EF;
    }

    /* Main text */
    h1, h2, h3, h4 {
        color: #292622 !important;
    }

    p, label {
        color: #5F574E !important;
    }

    /* Header */
    .main-header {
        padding: 10px 0 25px 0;
        border-bottom: 1px solid #DED5C9;
        margin-bottom: 30px;
    }

    .main-header h1 {
        font-family: Georgia, serif;
        font-size: 38px;
        margin-bottom: 2px;
        color: #292622;
    }

    .main-header p {
        color: #81766A;
        font-size: 13px;
        letter-spacing: 1px;
        margin: 0;
    }

    /* Hero */
    .hero-box {
        background-color: #FFFDF9;
        border: 1px solid #E5DDD2;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 25px;
    }

    .hero-box h2 {
        font-family: Georgia, serif;
        font-size: 31px;
        color: #292622;
        margin-bottom: 10px;
    }

    .hero-box p {
        color: #756C62;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* Cards */
    .metric-card {
        background-color: #FFFDF9;
        border: 1px solid #E5DDD2;
        border-radius: 15px;
        padding: 20px;
        text-align: left;
    }

    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #FFFDF9 !important;
        border: 1px dashed #B9A68D !important;
        border-radius: 15px !important;
    }

    /* Tabs */
    [data-baseweb="tab-list"] {
        background-color: #EDE6DD;
        padding: 5px;
        border-radius: 12px;
        gap: 4px;
    }

    [data-baseweb="tab"] {
        color: #756C62 !important;
        border-radius: 9px;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFDF9 !important;
        color: #292622 !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background-color: #3D3833;
        color: white;
        border-radius: 10px;
        border: none;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #5A5149;
        color: white;
    }

    /* Inputs */
    .stTextInput input {
        background-color: #FFFDF9;
        color: #292622;
        border: 1px solid #DDD3C6;
        border-radius: 10px;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: #FFFDF9;
        border: 1px solid #E4DBCF;
        border-radius: 12px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9B9084;
        font-size: 10px;
        letter-spacing: 1.5px;
        padding: 35px 0 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <h1>SmartInspect.</h1>
        <p>STATISTICAL QUALITY ANALYTICS · SY BSc IT</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">
        <h2>Understand your inspection data before problems become patterns.</h2>
        <p>
            SmartInspect analyses multi-stage product inspection data
            using descriptive statistics, probability, independence
            testing and failure-pattern analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD SECTION
# ============================================================

st.subheader("Upload Inspection Dataset")

st.write(
    "Upload a CSV containing Product_ID, Stage_1, Stage_2 and Stage_3."
)

uploaded_file = st.file_uploader(
    "Choose your CSV file",
    type=["csv"]
)


# ============================================================
# BEFORE FILE UPLOAD
# ============================================================

if uploaded_file is None:

    st.info(
        "Required columns: Product_ID, Stage_1, Stage_2, Stage_3. "
        "Stage values must be Pass or Fail."
    )

    st.subheader("Analysis Workflow")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("01", "Upload")

    with col2:
        st.metric("02", "Measure")

    with col3:
        st.metric("03", "Analyse")

    with col4:
        st.metric("04", "Interpret")

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
    "Stage_3"
]

missing_columns = [
    column
    for column in required_columns
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
    "Stage_3"
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
        failure_counts[stage]
        / total_products
        * 100
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
# TOP SUMMARY
# ============================================================

st.subheader("Dataset Snapshot")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Total Products",
        total_products
    )

with m2:
    st.metric(
        "Stage 1 Failures",
        failure_counts["Stage_1"]
    )

with m3:
    st.metric(
        "Stage 2 Failures",
        failure_counts["Stage_2"]
    )

with m4:
    st.metric(
        "Stage 3 Failures",
        failure_counts["Stage_3"]
    )


# ============================================================
# HORIZONTAL NAVIGATION
# ============================================================

(
    overview_tab,
    statistics_tab,
    probability_tab,
    independence_tab,
    patterns_tab,
    data_tab
) = st.tabs(
    [
        "Overview",
        "Statistics",
        "Probability",
        "Independence",
        "Patterns",
        "Data"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with overview_tab:

    st.header("Inspection Overview")

    st.write(
        "A summary of how products perform across the three "
        "inspection stages."
    )

    # Failure rate table

    failure_rate_df = pd.DataFrame(
        {
            "Stage": [
                "Stage 1",
                "Stage 2",
                "Stage 3"
            ],
            "Failures": [
                failure_counts["Stage_1"],
                failure_counts["Stage_2"],
                failure_counts["Stage_3"]
            ],
            "Passes": [
                pass_counts["Stage_1"],
                pass_counts["Stage_2"],
                pass_counts["Stage_3"]
            ],
            "Failure Rate (%)": [
                failure_rates["Stage_1"],
                failure_rates["Stage_2"],
                failure_rates["Stage_3"]
            ]
        }
    )

    st.subheader("Failure Rate by Stage")

    st.bar_chart(
        failure_rate_df.set_index("Stage")[
            "Failure Rate (%)"
        ]
    )

    st.dataframe(
        failure_rate_df.style.format(
            {
                "Failure Rate (%)": "{:.2f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # Dataset health

    st.subheader("Dataset Health")

    duplicate_ids = int(
        df["Product_ID"].duplicated().sum()
    )

    missing_values = int(
        df.isnull().sum().sum()
    )

    h1, h2, h3, h4 = st.columns(4)

    with h1:
        st.metric("Rows", len(df))

    with h2:
        st.metric("Columns", len(df.columns))

    with h3:
        st.metric("Duplicate IDs", duplicate_ids)

    with h4:
        st.metric("Missing Values", missing_values)

    # Insights

    st.subheader("Automated Insights")

    highest_stage = max(
        failure_rates,
        key=failure_rates.get
    )

    lowest_stage = min(
        failure_rates,
        key=failure_rates.get
    )

    complete_failures = int(
        (A & B & C).sum()
    )

    st.info(
        f"{highest_stage.replace('_', ' ')} has the highest "
        f"failure rate at {failure_rates[highest_stage]:.2f}%."
    )

    st.info(
        f"{lowest_stage.replace('_', ' ')} has the lowest "
        f"failure rate at {failure_rates[lowest_stage]:.2f}%."
    )

    st.info(
        f"{complete_failures} products failed all three stages."
    )


# ============================================================
# STATISTICS
# ============================================================

with statistics_tab:

    st.header("Statistical Profile")

    st.write(
        "Descriptive statistics summarize the numerical behaviour "
        "of the inspection outcomes."
    )

    # Binary encoding

    numeric_df = df[stage_columns].replace(
        {
            "Pass": 0,
            "Fail": 1
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
                "Maximum": values.max()
            }
        )

    statistics_df = pd.DataFrame(
        statistics_rows
    )

    st.dataframe(
        statistics_df.style.format(
            {
                "Mean": "{:.3f}",
                "Median": "{:.3f}",
                "Mode": "{:.0f}",
                "Variance": "{:.3f}",
                "Standard Deviation": "{:.3f}",
                "Minimum": "{:.0f}",
                "Maximum": "{:.0f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # Distribution

    st.subheader("Pass vs Fail Distribution")

    distribution_df = pd.DataFrame(
        {
            "Stage 1": [
                pass_counts["Stage_1"],
                failure_counts["Stage_1"]
            ],
            "Stage 2": [
                pass_counts["Stage_2"],
                failure_counts["Stage_2"]
            ],
            "Stage 3": [
                pass_counts["Stage_3"],
                failure_counts["Stage_3"]
            ]
        },
        index=["Pass", "Fail"]
    )

    st.bar_chart(distribution_df)

    # Explanation

    with st.expander("Why are Pass and Fail converted into numbers?"):

        st.write(
            "To calculate mathematical statistics, the inspection "
            "results are represented using binary encoding."
        )

        st.write("Pass = 0")
        st.write("Fail = 1")

        st.write(
            "This allows SmartInspect to calculate measures such "
            "as mean, variance and standard deviation."
        )


# ============================================================
# PROBABILITY
# ============================================================

with probability_tab:

    st.header("Probability Analysis")

    st.write(
        "Probability measures the likelihood of individual and "
        "combined inspection failures."
    )

    # Individual probability

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric(
            "P(A)",
            f"{P_A:.3f}"
        )

        st.caption("Probability of Stage 1 failure")

    with p2:
        st.metric(
            "P(B)",
            f"{P_B:.3f}"
        )

        st.caption("Probability of Stage 2 failure")

    with p3:
        st.metric(
            "P(C)",
            f"{P_C:.3f}"
        )

        st.caption("Probability of Stage 3 failure")

    # Joint probability

    st.subheader("Joint Probability")

    probability_df = pd.DataFrame(
        {
            "Event": [
                "A ∩ B",
                "A ∩ C",
                "B ∩ C",
                "A ∩ B ∩ C"
            ],
            "Meaning": [
                "Stage 1 and Stage 2 fail",
                "Stage 1 and Stage 3 fail",
                "Stage 2 and Stage 3 fail",
                "All three stages fail"
            ],
            "Probability": [
                P_AB,
                P_AC,
                P_BC,
                P_ABC
            ]
        }
    )

    st.dataframe(
        probability_df.style.format(
            {
                "Probability": "{:.3f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # Conditional probability

    st.subheader("Conditional Probability")

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
                "P(C | B)"
            ],
            "Probability": [
                P_B_given_A,
                P_C_given_A,
                P_C_given_B
            ]
        }
    )

    st.dataframe(
        conditional_df.style.format(
            {
                "Probability": "{:.3f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Example: P(B | A) means the probability of failing "
        "Stage 2 given that the product already failed Stage 1."
    )


# ============================================================
# INDEPENDENCE
# ============================================================

with independence_tab:

    st.header("Independence Analysis")

    st.write(
        "This section compares observed joint probabilities "
        "with values expected under independence."
    )

    # Expected probabilities

    expected_AB = P_A * P_B
    expected_AC = P_A * P_C
    expected_BC = P_B * P_C

    pairwise_df = pd.DataFrame(
        {
            "Event Pair": [
                "A & B",
                "A & C",
                "B & C"
            ],
            "Observed Probability": [
                P_AB,
                P_AC,
                P_BC
            ],
            "Expected if Independent": [
                expected_AB,
                expected_AC,
                expected_BC
            ],
            "Absolute Difference": [
                abs(P_AB - expected_AB),
                abs(P_AC - expected_AC),
                abs(P_BC - expected_BC)
            ]
        }
    )

    st.subheader("Pairwise Independence")

    st.dataframe(
        pairwise_df.style.format(
            {
                "Observed Probability": "{:.3f}",
                "Expected if Independent": "{:.3f}",
                "Absolute Difference": "{:.3f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # Chi-Square

    st.subheader("Chi-Square Independence Test")

    if not SCIPY_AVAILABLE:

        st.warning(
            "SciPy is not installed. Run "
            "'pip install scipy' to enable the Chi-Square test."
        )

    else:

        chi_results = []

        pairs = [
            (
                "Stage 1 × Stage 2",
                "Stage_1",
                "Stage_2"
            ),
            (
                "Stage 1 × Stage 3",
                "Stage_1",
                "Stage_3"
            ),
            (
                "Stage 2 × Stage 3",
                "Stage_2",
                "Stage_3"
            )
        ]

        # FIXED: the loop must contain "in pairs"
        for name, col1, col2 in pairs:

            contingency = pd.crosstab(
                df[col1],
                df[col2]
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

                interpretation = (
                    "Evidence of association"
                )

            else:

                interpretation = (
                    "No significant association detected"
                )

            chi_results.append(
                {
                    "Comparison": name,
                    "Chi-Square": chi2,
                    "p-value": p_value,
                    "Phi": phi,
                    "Interpretation": interpretation
                }
            )

        chi_df = pd.DataFrame(
            chi_results
        )

        st.dataframe(
            chi_df.style.format(
                {
                    "Chi-Square": "{:.3f}",
                    "p-value": "{:.4f}",
                    "Phi": "{:.3f}"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "A p-value below 0.05 provides statistical evidence "
            "of an association between the two stages. A p-value "
            "above 0.05 means the test did not detect significant "
            "evidence of association."
        )

    # Contingency tables

    st.subheader("Contingency Tables")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.write("Stage 1 × Stage 2")

        table_12 = pd.crosstab(
            df["Stage_1"],
            df["Stage_2"]
        )

        st.dataframe(
            table_12,
            use_container_width=True
        )

    with c2:

        st.write("Stage 1 × Stage 3")

        table_13 = pd.crosstab(
            df["Stage_1"],
            df["Stage_3"]
        )

        st.dataframe(
            table_13,
            use_container_width=True
        )

    with c3:

        st.write("Stage 2 × Stage 3")

        table_23 = pd.crosstab(
            df["Stage_2"],
            df["Stage_3"]
        )

        st.dataframe(
            table_23,
            use_container_width=True
        )

    # Mutual independence

    st.subheader("Mutual Independence")

    expected_ABC = P_A * P_B * P_C

    mutual_difference = abs(
        P_ABC - expected_ABC
    )

    mutual_df = pd.DataFrame(
        {
            "Measure": [
                "Observed P(A ∩ B ∩ C)",
                "Expected if Mutually Independent",
                "Absolute Difference"
            ],
            "Value": [
                P_ABC,
                expected_ABC,
                mutual_difference
            ]
        }
    )

    st.dataframe(
        mutual_df.style.format(
            {
                "Value": "{:.4f}"
            }
        ),
        use_container_width=True,
        hide_index=True
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

    st.header("Inspection Failure Patterns")

    st.write(
        "Each product is represented as a three-stage sequence "
        "to identify repeated inspection patterns."
    )

    # Create pattern

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
        axis=1
    )

    pattern_counts = (
        df["Inspection_Pattern"]
        .value_counts()
        .rename_axis("Pattern")
        .reset_index(
            name="Products"
        )
    )

    pattern_counts["Percentage"] = (
        pattern_counts["Products"]
        / total_products
        * 100
    )

    st.subheader("Pattern Distribution")

    st.bar_chart(
        pattern_counts.set_index("Pattern")[
            "Products"
        ]
    )

    st.dataframe(
        pattern_counts.style.format(
            {
                "Percentage": "{:.2f}%"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Pattern key: P = Pass and F = Fail. "
        "For example, F → P → F means Fail, Pass, Fail."
    )

    # Failure combinations

    st.subheader("Failure Combinations")

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
                "All Three Stages"
            ],
            "Products": [
                only_stage_1,
                only_stage_2,
                only_stage_3,
                stages_1_2,
                stages_1_3,
                stages_2_3,
                all_three
            ]
        }
    )

    st.dataframe(
        failure_combination_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DATA
# ============================================================

with data_tab:

    st.header("Inspection Dataset")

    st.write(
        "Search individual products and export the analysis results."
    )

    # Search

    search = st.text_input(
        "Search Product ID",
        placeholder="Type a Product ID..."
    )

    if search:

        filtered_df = df[
            df["Product_ID"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    else:

        filtered_df = df

    st.write(
        f"Showing {len(filtered_df)} of {len(df)} records."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # Downloads

    st.subheader("Download Results")

    d1, d2, d3 = st.columns(3)

    with d1:

        st.download_button(
            "Download Dataset",
            data=df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="smartinspect_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with d2:

        st.download_button(
            "Download Statistics",
            data=statistics_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="smartinspect_statistics.csv",
            mime="text/csv",
            use_container_width=True
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
                "P(A and B and C)"
            ],
            "Value": [
                P_A,
                P_B,
                P_C,
                P_AB,
                P_AC,
                P_BC,
                P_ABC
            ]
        }
    )

    with d3:

        st.download_button(
            "Download Probability",
            data=probability_export.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="smartinspect_probability.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        SMARTINSPECT · STATISTICAL QUALITY ANALYTICS · SY BSc IT
    </div>
    """,
    unsafe_allow_html=True
)