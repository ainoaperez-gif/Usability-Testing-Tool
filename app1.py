import streamlit as st
import pandas as pd
import time
import os

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")


def save_to_csv(data_dict, csv_file):
    # Convert dict to DataFrame with a single row
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Else, we need to append without writing the header!
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def clear_all_data():
    """Delete all collected CSV data files if they exist."""
    for csv_path in [CONSENT_CSV, DEMOGRAPHIC_CSV, TASK_CSV, EXIT_CSV]:
        if os.path.isfile(csv_path):
            os.remove(csv_path)


def main():
    st.title("Usability Testing Tool")

    home, consent, demographics, tasks, exit, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    # ---------------- HOME TAB ----------------
    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.

        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform one or more usability tasks in a separate app.
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)

    # ---------------- CONSENT TAB ----------------
    with consent:
        st.header("Consent Form")

        st.write("""
        You are invited to participate in a usability test for a student project.
        Your responses will be recorded and used only for educational purposes.
        Participation is voluntary and you may stop at any time. No personally
        identifying information is required.
        """)

        consent_given = st.checkbox(
            "I have read the information above and **agree to participate** in this usability test."
        )

        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                # Save the consent acceptance time
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                st.success("Consent recorded. Thank you!")

    # ---------------- DEMOGRAPHICS TAB ----------------
    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            st.write("Please answer a few short questions about yourself.")

            name = st.text_input("Name (optional)")
            age = st.number_input("Age", min_value=18, max_value=120, value=18, step=1)
            occupation = st.text_input("Major / Field of Study")
            familiarity = st.slider(
                "How familiar are you with web apps or dashboards?",
                min_value=1, max_value=5, value=3,
                help="1 = Not familiar at all, 5 = Very familiar"
            )

            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "familiarity": familiarity
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                st.success("Demographic data saved.")

    # ---------------- TASK TAB ----------------
    with tasks:
        st.header("Task Page")

        # --- initialize session_state keys for timing ---
        if "start_time" not in st.session_state:
            st.session_state["start_time"] = None
        if "task_duration" not in st.session_state:
            st.session_state["task_duration"] = None

        st.write("Please select a task from the usability test and record your experience after completing it in the separate app.")

        # Three concrete tasks for your Streamlit learning tools app
        task_options = [
            "Task 1: Look up a word in Vocabulary Builder",
            "Task 2: Complete a Quick Knowledge Quiz question",
            "Task 3: Solve a Math Problem Generator question"
        ]

        selected_task = st.selectbox("Select Task", task_options)

        # Show task-specific instructions
        if selected_task.startswith("Task 1"):
            st.markdown("""
            **Task 1 Instructions – Vocabulary Builder**

            1. Open the *Interactive Educational Tools for Remote Learning* app.
            2. In the sidebar, choose **“Vocabulary Builder”**.
            3. Enter the word **“resilient”**.
            4. Leave part of speech as **“Any”**.
            5. Click **“Define Word”**.
            6. Find the **main definition** and **one synonym** (if available).
            """)
        elif selected_task.startswith("Task 2"):
            st.markdown("""
            **Task 2 Instructions – Quick Knowledge Quiz**

            1. In the sidebar of the learning tools app, choose **“Quick Knowledge Quiz”**.
            2. Set **Category = “Science”**.
            3. Set **Difficulty = “easy”**.
            4. Click **“Load Question”**.
            5. Read the question, choose an answer, and click **“Submit Answer”**.
            """)
        elif selected_task.startswith("Task 3"):
            st.markdown("""
            **Task 3 Instructions – Math Problem Generator**

            1. In the sidebar of the learning tools app, choose **“Math Problem Generator”**.
            2. Set **Difficulty = “Medium”**.
            3. Set **Operation = “Multiplication (×)”**.
            4. Click **“Generate Problem”**.
            5. Enter your answer and click **“Check Answer”**.
            """)

        st.write("---")

        # --- timing controls ---
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Start Task Timer"):
                st.session_state["start_time"] = time.time()
                st.session_state["task_duration"] = None
                st.info("Task timer started.")

        with col2:
            if st.button("Stop Task Timer"):
                if st.session_state["start_time"] is None:
                    st.warning("You need to start the timer before stopping it.")
                else:
                    duration = time.time() - st.session_state["start_time"]
                    st.session_state["task_duration"] = duration
                    st.success(f"Task timer stopped. Duration: {duration:.2f} seconds")

        # Show current recorded duration (if any)
        if st.session_state["task_duration"] is not None:
            st.write(f"**Current recorded duration:** {st.session_state['task_duration']:.2f} seconds")

        success = st.radio(
            "Was the task completed successfully?",
            ["Yes", "No", "Partial"]
        )

        difficulty_rating = st.slider(
            "How difficult was this task? (1 = very easy, 5 = very hard)",
            min_value=1, max_value=5, value=3
        )

        participant_answer = st.text_input(
            "Briefly describe the result you got (e.g., definition, answer, etc.):",
            ""
        )

        notes = st.text_area("Observer Notes (optional)")

        if st.button("Save Task Results"):
            # If user started the timer but forgot to stop, compute duration up to now
            if st.session_state["task_duration"] is None and st.session_state["start_time"] is not None:
                st.session_state["task_duration"] = time.time() - st.session_state["start_time"]

            duration_val = st.session_state["task_duration"]

            if duration_val is None:
                st.error("Please start and stop the timer (or at least start it) before saving task results.")
            else:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val,
                    "difficulty_rating": difficulty_rating,
                    "participant_answer": participant_answer,
                    "notes": notes
                }
                save_to_csv(data_dict, TASK_CSV)

                # Reset any stored time in session_state for next task
                st.session_state["start_time"] = None
                st.session_state["task_duration"] = None

                st.success("Task results saved.")

    # ---------------- EXIT QUESTIONNAIRE TAB ----------------
    with exit:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            st.write("Please rate your overall experience using the educational web app.")

            satisfaction = st.slider(
                "Overall, how satisfied were you with the app?",
                min_value=1, max_value=5, value=4,
                help="1 = Very dissatisfied, 5 = Very satisfied"
            )

            difficulty = st.slider(
                "Overall, how difficult was the app to use?",
                min_value=1, max_value=5, value=2,
                help="1 = Very easy, 5 = Very difficult"
            )

            open_feedback = st.text_area(
                "Is there anything you liked, disliked, or would change about the app?"
            )

            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")

    # ---------------- REPORT TAB ----------------
    with report:
        st.header("Usability Report - Aggregated Results")

        # ---- Data reset / clear section ----
        st.subheader("Data Management")
        st.write(
            "Click the button below to delete all previously collected data "

        )

        if st.button("🚨 Delete ALL collected data and start fresh"):
            clear_all_data()
            st.success("All data files have been deleted. You can now start data collection from a clean slate.")
            # Optional: also clear any session timers
            if "start_time" in st.session_state:
                st.session_state["start_time"] = None
            if "task_duration" in st.session_state:
                st.session_state["task_duration"] = None

        st.write("---")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)

            st.subheader("Aggregated Task Metrics")

            # Make sure duration is numeric
            if "duration_seconds" in task_df.columns:
                task_df["duration_seconds"] = pd.to_numeric(
                    task_df["duration_seconds"], errors="coerce"
                )

            # Success rate: percentage of "Yes"
            def success_rate(series):
                return (series == "Yes").mean() * 100.0

            agg_cols = {"success": success_rate}

            if "duration_seconds" in task_df.columns:
                agg_cols["duration_seconds"] = "mean"
            if "difficulty_rating" in task_df.columns:
                agg_cols["difficulty_rating"] = "mean"

            summary_df = task_df.groupby("task_name").agg(agg_cols).reset_index()

            summary_df = summary_df.rename(columns={
                "success": "success_rate_percent",
                "duration_seconds": "avg_duration_seconds",
                "difficulty_rating": "avg_difficulty_rating"
            })

            st.dataframe(summary_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)

            # Example of aggregated stats (for demonstration only)
            st.subheader("Exit Questionnaire Averages")
            avg_satisfaction = exit_df["satisfaction"].mean()
            avg_difficulty = exit_df["difficulty"].mean()
            st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")
        else:
            st.info("No exit questionnaire data available yet.")


if __name__ == "__main__":
    main()

