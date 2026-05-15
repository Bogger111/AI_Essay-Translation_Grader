import streamlit as st

from main import grade_submission
from ocr import OCR_AVAILABLE, extract_text_from_image
from prompt import EXAM_PROFILES, TASK_TYPES


st.set_page_config(
    page_title="AI English Essay Grader",
    page_icon="📝",
    layout="wide",
)


def recognize_uploaded_image(
    uploaded_file,
    target_key: str,
    processed_key: str,
    label: str,
    enhanced_ocr: bool,
) -> None:
    """Recognize text from one uploaded image and fill the target input."""
    if uploaded_file is None:
        return

    st.image(uploaded_file, caption=f"Uploaded {label} image", use_container_width=True)

    image_key = f"{uploaded_file.name}-{uploaded_file.size}-{enhanced_ocr}"
    if st.session_state.get(processed_key) == image_key:
        return

    st.session_state[processed_key] = image_key

    try:
        with st.spinner(f"Recognizing text from the {label} image..."):
            recognized_text = extract_text_from_image(
                uploaded_file,
                enhanced=enhanced_ocr,
            ).strip()

        if recognized_text:
            st.session_state[target_key] = recognized_text
            st.success(f"{label} recognized and filled in automatically.")
            st.rerun()
        else:
            st.warning(f"No text was recognized from the {label} image. Try a clearer image.")
    except ImportError as exc:
        st.error(f"OCR is not available: {exc}")
    except Exception as exc:
        st.error(f"Failed to recognize the {label} image: {exc}")


def field_labels(task_type: str) -> tuple[str, str, str, str]:
    if task_type == "translation":
        return (
            "Source text / prompt",
            "Paste the source text or upload an image for OCR:",
            "Student translation",
            "Paste the student's translation or upload an image for OCR:",
        )
    return (
        "Essay prompt",
        "Paste the essay prompt or upload an image for OCR:",
        "Student essay",
        "Paste the student's essay or upload an image for OCR:",
    )


with st.sidebar:
    st.header("Settings")

    exam_type = st.selectbox(
        "Exam type",
        options=list(EXAM_PROFILES.keys()),
        format_func=lambda key: EXAM_PROFILES[key]["name"],
    )

    task_type = st.radio(
        "Task",
        options=list(TASK_TYPES.keys()),
        format_func=lambda key: TASK_TYPES[key],
    )

    enhanced_ocr = st.toggle(
        "Enhanced handwriting OCR",
        value=True,
        disabled=not OCR_AVAILABLE,
    )

    if OCR_AVAILABLE:
        st.success("Image OCR is available")
    else:
        st.warning("Image OCR is unavailable. Text input still works.")

st.title("AI English Essay Grader")
st.caption(
    "Supports CET-4, CET-6, TOEFL, IELTS, and GRE. Paste text directly or upload images for OCR."
)

primary_label, primary_help, answer_label, answer_help = field_labels(task_type)

left_col, right_col = st.columns(2)

with left_col:
    st.subheader(primary_label)
    task_image = st.file_uploader(
        f"Upload {primary_label} image",
        type=["png", "jpg", "jpeg", "webp"],
        key=f"{task_type}_task_image",
        disabled=not OCR_AVAILABLE,
    )
    recognize_uploaded_image(
        task_image,
        "task_text_input",
        "task_ocr_processed",
        primary_label,
        enhanced_ocr,
    )

    task_text = st.text_area(
        primary_help,
        placeholder="Example: Should students use AI in education?",
        height=180,
        key="task_text_input",
    )

with right_col:
    st.subheader(answer_label)
    answer_image = st.file_uploader(
        f"Upload {answer_label} image",
        type=["png", "jpg", "jpeg", "webp"],
        key=f"{task_type}_answer_image",
        disabled=not OCR_AVAILABLE,
    )
    recognize_uploaded_image(
        answer_image,
        "answer_text_input",
        "answer_ocr_processed",
        answer_label,
        enhanced_ocr,
    )

    answer_text = st.text_area(
        answer_help,
        height=300,
        placeholder="Paste the student's answer here...",
        key="answer_text_input",
    )

with st.expander("Preview current input", expanded=False):
    st.write(f"{primary_label}:")
    st.code(st.session_state.get("task_text_input", "").strip() or "No content", language="text")
    st.write(f"{answer_label}:")
    st.code(st.session_state.get("answer_text_input", "").strip() or "No content", language="text")

if st.button("Grade", type="primary", use_container_width=True):
    task_text = st.session_state.get("task_text_input", "").strip()
    answer_text = st.session_state.get("answer_text_input", "").strip()

    if not task_text:
        st.warning(f"Please enter {primary_label} or upload an image first.")
    elif not answer_text:
        st.warning(f"Please enter {answer_label} or upload an image first.")
    else:
        with st.spinner("Grading..."):
            try:
                result = grade_submission(exam_type, task_type, task_text, answer_text)
            except Exception as exc:
                st.error(f"Grading failed: {exc}")
            else:
                st.subheader("Result")
                st.markdown(result)
