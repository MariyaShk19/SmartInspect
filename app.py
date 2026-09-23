import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="SmartInspect",
    page_icon="🏭",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏭 SmartInspect")
st.subheader("Product Quality & Independence Analyzer")

st.write(
    "Upload product inspection data to analyze statistical measures, "
    "failure probabilities, and independence between inspection stages."
)

st.info(
    "💡 SmartInspect checks whether failures at different inspection "
    "stages occur independently using probability calculations."
)

with st.expander("📘 How SmartInspect Works"):

    st.write("### Events")

    st.write(
        "**A** = Product fails Stage 1"
    )

    st.write(
        "**B** = Product fails Stage 2"
    )

    st.write(
        "**C** = Product fails Stage 3"
    )

    st.write("### Pairwise Independence")

    st.latex(
        r"P(A \cap B) = P(A)P(B)"
    )

    st.write(
        "The same comparison is performed for A & C and B & C."
    )

    st.write("### Mutual Independence")

    st.latex(
        r"P(A \cap B \cap C) = P(A)P(B)P(C)"
    )

    st.write(
        "The observed and expected probabilities are compared "
        "to determine approximate independence."
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🏭 SmartInspect")

st.sidebar.markdown("---")

st.sidebar.header("📁 Data Input")

uploaded_file = st.sidebar.file_uploader(
    "Upload Inspection CSV",
    type=["csv"]
)

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Project Focus")

st.sidebar.write(
    "• Statistical Measures\n"
    "• Probability Analysis\n"
    "• Pairwise Independence\n"
    "• Mutual Independence"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Statistical Measures Mini Project"
)

# --------------------------------------------------
# CSV UPLOAD
# --------------------------------------------------

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.success("CSV file uploaded successfully!")

    # Required columns
    required_columns = [
        "Product_ID",
        "Stage_1",
        "Stage_2",
        "Stage_3"
    ]

    # Check CSV format
    if all(column in data.columns for column in required_columns):

        # --------------------------------------------------
        # DASHBOARD
        # --------------------------------------------------

        total_products = len(data)

        stage1_failures = (data["Stage_1"] == "Fail").sum()
        stage2_failures = (data["Stage_2"] == "Fail").sum()
        stage3_failures = (data["Stage_3"] == "Fail").sum()

        stage1_rate = stage1_failures / total_products * 100
        stage2_rate = stage2_failures / total_products * 100
        stage3_rate = stage3_failures / total_products * 100

        st.header("📊 Inspection Dashboard")

        st.markdown(
            """
            This dashboard analyzes product inspection results across
            three quality-control stages and evaluates the independence
            of failure events.
            """
        )

        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "📦 Total Products",
            total_products
        )

        col2.metric(
            "🔍 Stage 1 Failure",
            f"{stage1_rate:.1f}%"
        )

        col3.metric(
            "🔍 Stage 2 Failure",
            f"{stage2_rate:.1f}%"
        )

        col4.metric(
            "🔍 Stage 3 Failure",
            f"{stage3_rate:.1f}%"
        )


        # --------------------------------------------------
        # STATISTICAL MEASURES
        # --------------------------------------------------

        st.header("📐 Statistical Measures")

        numeric_data = data[
            ["Stage_1", "Stage_2", "Stage_3"]
        ].replace({
            "Pass": 0,
            "Fail": 1
        })

        statistical_results = []

        for stage in numeric_data.columns:

            statistical_results.append({
                "Stage": stage.replace("_", " "),
                "Mean": numeric_data[stage].mean(),
                "Median": numeric_data[stage].median(),
                "Mode": numeric_data[stage].mode()[0],
                "Standard Deviation": numeric_data[stage].std()
            })

        statistics_df = pd.DataFrame(
            statistical_results
        )

        statistics_df = statistics_df.round(3)

        st.dataframe(
            statistics_df,
            use_container_width=True,
            hide_index=True
        )


        # --------------------------------------------------
        # PROBABILITY ANALYSIS
        # --------------------------------------------------

        st.header("🎲 Probability Analysis")

        # Events
        A = data["Stage_1"] == "Fail"
        B = data["Stage_2"] == "Fail"
        C = data["Stage_3"] == "Fail"

        # Individual probabilities
        P_A = A.mean()
        P_B = B.mean()
        P_C = C.mean()

        # Joint probabilities
        P_AB = (A & B).mean()
        P_AC = (A & C).mean()
        P_BC = (B & C).mean()
        P_ABC = (A & B & C).mean()


        # Probability cards
        p1, p2, p3 = st.columns(3)

        p1.metric(
            "P(A) – Stage 1 Failure",
            f"{P_A:.3f}"
        )

        p2.metric(
            "P(B) – Stage 2 Failure",
            f"{P_B:.3f}"
        )

        p3.metric(
            "P(C) – Stage 3 Failure",
            f"{P_C:.3f}"
        )


        # Joint probabilities
        st.subheader("Joint Probabilities")

        probability_df = pd.DataFrame({
            "Event": [
                "A ∩ B",
                "A ∩ C",
                "B ∩ C",
                "A ∩ B ∩ C"
            ],
            "Probability": [
                P_AB,
                P_AC,
                P_BC,
                P_ABC
            ]
        })

        probability_df["Probability"] = (
            probability_df["Probability"].round(3)
        )

        st.dataframe(
            probability_df,
            use_container_width=True,
            hide_index=True
        )


        # --------------------------------------------------
        # PAIRWISE INDEPENDENCE
        # --------------------------------------------------

        st.header("🔗 Pairwise Independence Analysis")

        tolerance = 0.05

        expected_AB = P_A * P_B
        expected_AC = P_A * P_C
        expected_BC = P_B * P_C

        difference_AB = abs(P_AB - expected_AB)
        difference_AC = abs(P_AC - expected_AC)
        difference_BC = abs(P_BC - expected_BC)

        pairwise_results = pd.DataFrame({
            "Event Pair": [
                "A & B",
                "A & C",
                "B & C"
            ],
            "Observed P(A ∩ B)": [
                P_AB,
                P_AC,
                P_BC
            ],
            "Expected P(A)P(B)": [
                expected_AB,
                expected_AC,
                expected_BC
            ],
            "Difference": [
                difference_AB,
                difference_AC,
                difference_BC
            ]
        })

        pairwise_results = pairwise_results.round(3)

        st.dataframe(
            pairwise_results,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "For this educational project, a difference of 0.05 or less "
            "is treated as approximately independent."
        )


        # --------------------------------------------------
        # PAIRWISE RESULTS
        # --------------------------------------------------

        st.subheader("Pairwise Independence Results")

        st.write(
            "Two events are approximately independent when "
            "P(A ∩ B) is close to P(A)P(B)."
        )

        pair1, pair2, pair3 = st.columns(3)

        if difference_AB <= tolerance:
            pair1.success(
                "A & B\n\nApproximately Independent"
            )
        else:
            pair1.error(
                "A & B\n\nNot Independent"
            )

        if difference_AC <= tolerance:
            pair2.success(
                "A & C\n\nApproximately Independent"
            )
        else:
            pair2.error(
                "A & C\n\nNot Independent"
            )

        if difference_BC <= tolerance:
            pair3.success(
                "B & C\n\nApproximately Independent"
            )
        else:
            pair3.error(
                "B & C\n\nNot Independent"
            )

        if difference_AB <= tolerance:
            pair1.success("A & B\nApproximately Independent")
        else:
            pair1.error("A & B\nNot Independent")

        if difference_AC <= tolerance:
            pair2.success("A & C\nApproximately Independent")
        else:
            pair2.error("A & C\nNot Independent")

        if difference_BC <= tolerance:
            pair3.success("B & C\nApproximately Independent")
        else:
            pair3.error("B & C\nNot Independent")


        # --------------------------------------------------
        # MUTUAL INDEPENDENCE
        # --------------------------------------------------

        st.header("🔗 Mutual Independence Analysis")

        st.write(
            "For mutual independence, all three events must satisfy:"
        )

        st.latex(
            r"P(A \cap B \cap C) = P(A)P(B)P(C)"
        )

        expected_ABC = P_A * P_B * P_C

        mutual_difference = abs(
            P_ABC - expected_ABC
        )

        # Results
        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Observed P(A ∩ B ∩ C)",
            f"{P_ABC:.3f}"
        )

        m2.metric(
            "Expected P(A)P(B)P(C)",
            f"{expected_ABC:.3f}"
        )

        m3.metric(
            "Difference",
            f"{mutual_difference:.3f}"
        )

        if mutual_difference <= tolerance:

            st.success(
                "✅ The three inspection stages are "
                "approximately mutually independent."
            )

        else:

            st.error(
                "❌ The three inspection stages are "
                "not mutually independent."
            )

        st.caption(
            "Note: The 0.05 tolerance is used only as an "
            "educational approximation for this project."
        )

        st.write(
            f"**Observed P(A ∩ B ∩ C):** {P_ABC:.3f}"
        )

        st.write(
            f"**Expected P(A)P(B)P(C):** {expected_ABC:.3f}"
        )

        st.write(
            f"**Difference:** {mutual_difference:.3f}"
        )

        if mutual_difference <= tolerance:

            st.success(
                "The three inspection stages are "
                "approximately mutually independent."
            )

        else:

            st.error(
                "The three inspection stages are "
                "not mutually independent."
            )


        # --------------------------------------------------
        # VISUALIZATION
        # --------------------------------------------------

        st.header("📈 Visualizations")

        # Failure rate chart
        stages = [
            "Stage 1",
            "Stage 2",
            "Stage 3"
        ]

        failure_rates = [
            stage1_rate,
            stage2_rate,
            stage3_rate
        ]

        fig1, ax1 = plt.subplots(
            figsize=(8, 5)
        )

        bars = ax1.bar(
            stages,
            failure_rates
        )

        ax1.set_title(
            "Product Failure Rate by Inspection Stage"
        )

        ax1.set_xlabel(
            "Inspection Stage"
        )

        ax1.set_ylabel(
            "Failure Rate (%)"
        )

        for bar, value in zip(
            bars,
            failure_rates
        ):

            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.5,
                f"{value:.1f}%",
                ha="center"
            )

        ax1.set_ylim(
            0,
            max(failure_rates) + 10
        )

        st.pyplot(fig1)


        # --------------------------------------------------
        # OBSERVED VS EXPECTED
        # --------------------------------------------------

        st.subheader(
            "Observed vs Expected Joint Probabilities"
        )

        pairs = [
            "A & B",
            "A & C",
            "B & C"
        ]

        observed = [
            P_AB,
            P_AC,
            P_BC
        ]

        expected = [
            expected_AB,
            expected_AC,
            expected_BC
        ]

        x = np.arange(
            len(pairs)
        )

        width = 0.35

        fig2, ax2 = plt.subplots(
            figsize=(9, 5)
        )

        ax2.bar(
            x - width / 2,
            observed,
            width,
            label="Observed"
        )

        ax2.bar(
            x + width / 2,
            expected,
            width,
            label="Expected if Independent"
        )

        ax2.set_xticks(x)

        ax2.set_xticklabels(
            pairs
        )

        ax2.set_xlabel(
            "Event Pair"
        )

        ax2.set_ylabel(
            "Probability"
        )

        ax2.set_title(
            "Observed vs Expected Joint Probabilities"
        )

        ax2.legend()

        st.pyplot(fig2)


        # --------------------------------------------------
        # RAW DATA
        # --------------------------------------------------

        st.header("📋 Inspection Data")

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="⬇️ Download Inspection Data",
            data=data.to_csv(index=False),
            file_name="smartinspect_results.csv",
            mime="text/csv"
        )


    else:

        st.error(
            "Invalid CSV format. Please upload a CSV containing "
            "Product_ID, Stage_1, Stage_2 and Stage_3 columns."
        )


else:

    st.info(
        "👈 Please upload the inspection_data.csv file "
        "from the sidebar to begin the analysis."
    )