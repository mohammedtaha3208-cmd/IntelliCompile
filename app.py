import html
import json
import streamlit as st

from lexer import tokenize
from parser import parse
from semantic import SemanticAnalyzer
from intermediate import IntermediateCodeGenerator
from optimizer import CodeOptimizer
from codegen import CodeGenerator
from virtual_machine import VirtualMachine
from ast_visualizer import generate_ast_dot

def build_compilation_report(
    source_code,
    tokens,
    ast,
    symbol_table,
    intermediate_code,
    optimized_code,
    original_count,
    optimized_count,
    removed_count,
    reduction,
    bytecode,
    execution_trace,
    output,
    variables
):
    def safe(value):
        return html.escape(str(value))

    def pretty(value):
        return safe(json.dumps(value, indent=2, default=str))

    token_rows = "".join(
        f"<tr><td>{safe(token[0])}</td>"
        f"<td>{safe(token[1])}</td>"
        f"<td>{safe(token[2])}</td></tr>"
        for token in tokens
    )

    trace_data = (
        execution_trace.to_dict(orient="records")
        if hasattr(execution_trace, "to_dict")
        else execution_trace
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>IntelliCompile Compilation Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; color: #24344d; }}
h1, h2 {{ color: #24466f; }}
section {{ margin: 24px 0; page-break-inside: avoid; }}
pre {{ background: #f4f7fb; border: 1px solid #dce4ef; padding: 14px;
       border-radius: 8px; white-space: pre-wrap; overflow-wrap: anywhere; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #dce4ef; padding: 8px; text-align: left; }}
th {{ background: #eaf0f8; }}
@media print {{ body {{ margin: 16mm; }} }}
</style>
</head>
<body>
<h1>IntelliCompile — Compilation Report</h1>
<p>Integrated Compiler Phase Simulator for Source Code Translation</p>

<section><h2>1. Source Code</h2><pre>{safe(source_code)}</pre></section>
<section><h2>2. Token Table</h2>
<table><thead><tr><th>Type</th><th>Value</th><th>Line</th></tr></thead>
<tbody>{token_rows}</tbody></table></section>
<section><h2>3. Abstract Syntax Tree</h2><pre>{pretty(ast)}</pre></section>
<section><h2>4. Symbol Table</h2><pre>{pretty(symbol_table)}</pre></section>
<section><h2>5. Intermediate Code</h2><pre>{safe(chr(10).join(intermediate_code))}</pre></section>
<section><h2>6. Optimized Code</h2>
<pre>{safe(chr(10).join(optimized_code))}</pre>
<p>Original instructions: {original_count} |
Optimized instructions: {optimized_count} |
Removed: {removed_count} |
Reduction: {reduction:.1f}%</p></section>
<section><h2>7. Target Bytecode</h2><pre>{safe(chr(10).join(bytecode))}</pre></section>
<section><h2>8. VM Execution Trace</h2><pre>{pretty(trace_data)}</pre>
<h3>Program Output</h3><pre>{pretty(output)}</pre></section>
<section><h2>9. Final Variable Values</h2><pre>{pretty(variables)}</pre></section>
</body>
</html>"""

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="IntelliCompile",
    page_icon="⚙️",
    layout="wide"
)


# =====================================================
# PROFESSIONAL LIGHT THEME
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #F5F7FC;
    color: #26354A;
    font-family: "Segoe UI", sans-serif;
}

[data-testid="stHeader"] {
    background-color: #F5F7FC;
}

[data-testid="stSidebar"] {
    background-color: #EAF0F8;
    border-right: 1px solid #D9E2EF;
}

[data-testid="stSidebar"] * {
    color: #26354A;
}

h1, h2, h3, h4 {
    color: #24466F !important;
}

p, label, li {
    color: #42536B;
}

.stCaption {
    color: #718096 !important;
}

/* Source code editor */
div[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    color: #243B63 !important;
    -webkit-text-fill-color: #243B63 !important;
    caret-color: #2563EB !important;
    border: 1px solid #CAD5E4 !important;
    border-radius: 10px !important;
    font-family: Consolas, monospace !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border: 1px solid #5488D8 !important;
    box-shadow: 0 0 0 2px #DCE9FC !important;
}

/* Dropdown styling */
.stApp [data-testid="stSelectbox"] [data-baseweb="select"],
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,
.stApp [data-testid="stSelectbox"] [role="combobox"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #26354A !important;
    border-color: #CAD5E4 !important;
    opacity: 1 !important;
}

.stApp [data-testid="stSelectbox"] [data-baseweb="select"] *,
.stApp [data-testid="stSelectbox"] [role="combobox"] * {
    color: #26354A !important;
    -webkit-text-fill-color: #26354A !important;
}

.stApp [data-testid="stSelectbox"] svg {
    fill: #26354A !important;
    color: #26354A !important;
}

div[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
}

div[data-baseweb="popover"] * {
    color: #26354A !important;
}

/* Main buttons */
div.stButton > button {
    background-color: #356AC3 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.55rem 1.1rem !important;
    font-weight: 600 !important;
}

div.stButton > button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

div.stButton > button:hover {
    background-color: #2856A5 !important;
}

/* Download buttons */
div.stDownloadButton > button {
    background-color: #E5EEFC !important;
    color: #24569E !important;
    border: 1px solid #C7D8F3 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
}

div.stDownloadButton > button * {
    color: #24569E !important;
    -webkit-text-fill-color: #24569E !important;
}

/* Code blocks */
div[data-testid="stCode"],
div[data-testid="stCode"] pre,
div[data-testid="stCode"] code {
    background-color: #FFFFFF !important;
    color: #243B63 !important;
    border-radius: 9px !important;
}

div[data-testid="stCode"] {
    border: 1px solid #DCE4EF !important;
}

/* Tables */
div[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DCE4EF !important;
    border-radius: 9px !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DCE4EF !important;
    border-radius: 11px !important;
    padding: 16px !important;
}

div[data-testid="stMetric"] label {
    color: #64748B !important;
}

div[data-testid="stMetricValue"] {
    color: #24466F !important;
}

/* JSON output */
div[data-testid="stJson"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DCE4EF !important;
    border-radius: 9px !important;
    padding: 12px !important;
}

/* Alerts and dividers */
div[data-testid="stAlert"] {
    border-radius: 9px !important;
}

hr {
    border-color: #DCE4EF !important;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SAMPLE PROGRAMS
# =====================================================

sample_programs = {
    "Basic Arithmetic": """int a = 10;
int b = 20;
int c = a + b;
print(c);""",

    "Operator Precedence": """int x = 12;
int y = 3;
int z = (x + y) * 2;
print(z);""",

    "Variable Reassignment": """int a = 10;
a = 20;
int b = a + 5;
print(b);""",

    "Dead Code Elimination": """int a = 10;
int b = 20;
int c = a + b;
int unused = 100;
print(c);"""
}


# =====================================================
# SESSION STATE
# =====================================================

if "source_editor" not in st.session_state:
    st.session_state.source_editor = sample_programs["Basic Arithmetic"]

if "sample_choice" not in st.session_state:
    st.session_state.sample_choice = "Basic Arithmetic"


def update_sample_code():

    selected = st.session_state.sample_choice

    if selected == "Custom Program":
        st.session_state.source_editor = ""
    else:
        st.session_state.source_editor = sample_programs[selected]


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("⚙️ IntelliCompile")
    st.caption("COMPILER DESIGN PROJECT")

    st.divider()

    st.subheader("Compiler Pipeline")

    st.markdown("""
    **01**  Lexical Analysis

    **02**  Syntax Analysis

    **03**  Semantic Analysis

    **04**  Intermediate Code Generation

    **05**  Code Optimization

    **06**  Target Code Generation

    **07**  Virtual Machine Execution
    """)

    st.divider()

    st.subheader("Supported Language")

    st.code(
        "int\nidentifiers\narithmetic\nprint",
        language="text"
    )

    st.caption("Custom Educational Programming Language")

    st.divider()

    st.caption("IntelliCompile | Version 1.0")


# =====================================================
# MAIN DASHBOARD
# =====================================================

st.title("⚙️ IntelliCompile")

st.subheader("Integrated Compiler Phase Simulator")

st.write(
    "Explore how source code is translated through "
    "different compiler phases, optimized and executed "
    "using a custom virtual machine."
)

st.divider()


# =====================================================
# SOURCE CODE EDITOR
# =====================================================

st.subheader("Source Code Editor")

st.selectbox(
    "Choose a sample program",
    ["Custom Program"] + list(sample_programs.keys()),
    key="sample_choice",
    on_change=update_sample_code
)

source_code = st.text_area(
    "Enter your program",
    height=220,
    key="source_editor"
)


# =====================================================
# PHASE-WISE EXECUTION CONTROL
# =====================================================

st.divider()

st.subheader("Compilation Controls")

execution_modes = [
    "Full Compilation",
    "1. Lexical Analysis",
    "2. Syntax Analysis",
    "3. Semantic Analysis",
    "4. Intermediate Code Generation",
    "5. Code Optimization",
    "6. Target Code Generation",
    "7. Virtual Machine Execution"
]

selected_mode = st.selectbox(
    "Select the phase to execute",
    execution_modes
)

st.caption(
    "Selecting a phase executes all prerequisite phases "
    "and displays the results up to your selected phase."
)

# =====================================================
# PIPELINE STATUS
# =====================================================

pipeline_phases = [
    "Lexical Analysis",
    "Syntax Analysis",
    "Semantic Analysis",
    "Intermediate Code Generation",
    "Code Optimization",
    "Target Code Generation",
    "Virtual Machine Execution"
]

phase_icons = ["🔍", "🌳", "📋", "⚙️", "🚀", "💻", "▶️"]

if "phase_status" not in st.session_state:
    st.session_state.phase_status = {
        phase: "Pending" for phase in pipeline_phases
    }


def render_pipeline_status():
    st.subheader("Compiler Pipeline Overview")
    columns = st.columns(7)

    status_styles = {
        "Pending": ("#718096", "#DCE4EF"),
        "Completed": ("#16804A", "#B7E4C7"),
        "Failed": ("#C0392B", "#F3B5B5")
    }

    for index, column in enumerate(columns):
        phase = pipeline_phases[index]
        status = st.session_state.phase_status.get(phase, "Pending")
        status_color, border_color = status_styles[status]

        with column:
            st.markdown(
                f"""
                <div style="
                    background-color: #FFFFFF;
                    border: 1px solid {border_color};
                    border-radius: 10px;
                    padding: 12px 5px;
                    text-align: center;
                    min-height: 112px;
                ">
                    <div style="font-size: 23px;">{phase_icons[index]}</div>
                    <div style="
                        font-size: 12px;
                        font-weight: 600;
                        color: #24466F;
                        min-height: 36px;
                    ">{phase}</div>
                    <div style="
                        font-size: 11px;
                        font-weight: 700;
                        color: {status_color};
                    ">{status}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# Display the most recent compilation status
render_pipeline_status()

# =====================================================
# COMPILATION PIPELINE
# =====================================================

if st.button("▶ Run Selected Phase", type="primary"):

    st.session_state.pop("compilation_report_html", None)
    phase_limits = {
        "Full Compilation": 7,
        "1. Lexical Analysis": 1,
        "2. Syntax Analysis": 2,
        "3. Semantic Analysis": 3,
        "4. Intermediate Code Generation": 4,
        "5. Code Optimization": 5,
        "6. Target Code Generation": 6,
        "7. Virtual Machine Execution": 7
    }

    phase_limit = phase_limits[selected_mode]

    st.session_state.phase_status = {
        phase: "Pending" for phase in pipeline_phases
    }
    current_phase = "Lexical Analysis"

    # -------------------------------------------------
    # 1. LEXICAL ANALYSIS
    # -------------------------------------------------

    tokens, errors = tokenize(source_code)

    if errors:
        st.session_state.phase_status["Lexical Analysis"] = "Failed"
        st.error("Lexical Analysis Failed")
        st.write(errors)
        render_pipeline_status()
        st.stop()

    st.session_state.phase_status["Lexical Analysis"] = "Completed"

    st.header("1. Lexical Analysis")

    st.success("Lexical Analysis Successful")

    st.subheader("Token Table")

    st.dataframe(
        [
            {
                "Type": t[0],
                "Value": t[1],
                "Line": t[2]
            }
            for t in tokens
        ],
        use_container_width=True
    )

    if phase_limit == 1:
        st.success("Lexical Analysis Completed!")
        render_pipeline_status()
        st.stop()

    try:

        # -------------------------------------------------
        # 2. SYNTAX ANALYSIS
        # -------------------------------------------------

        current_phase = "Syntax Analysis"
        ast = parse(tokens)

        st.header("2. Syntax Analysis")

        st.success("Syntax Analysis Successful")
        st.session_state.phase_status["Syntax Analysis"] = "Completed"

        st.subheader("Abstract Syntax Tree")

        st.json(ast)

        st.subheader("AST Visualization")

        ast_graph = generate_ast_dot(ast)

        st.graphviz_chart(
            ast_graph,
            use_container_width=True
        )

        if phase_limit == 2:
            st.success("Syntax Analysis Completed!")
            render_pipeline_status()
            st.stop()

        # -------------------------------------------------
        # 3. SEMANTIC ANALYSIS
        # -------------------------------------------------

        current_phase = "Semantic Analysis"
        st.header("3. Semantic Analysis")

        analyzer = SemanticAnalyzer()

        symbol_table, semantic_errors = analyzer.analyze(ast)

        if semantic_errors:
            st.session_state.phase_status["Semantic Analysis"] = "Failed"
            st.error("Semantic Analysis Failed")
            st.write(semantic_errors)
            render_pipeline_status()
            st.stop()

        st.success("Semantic Analysis Successful")
        st.session_state.phase_status["Semantic Analysis"] = "Completed"

        st.subheader("Symbol Table")

        st.json(symbol_table)

        if phase_limit == 3:
            st.success("Semantic Analysis Completed!")
            render_pipeline_status()
            st.stop()

        # -------------------------------------------------
        # 4. INTERMEDIATE CODE GENERATION
        # -------------------------------------------------

        current_phase = "Intermediate Code Generation"
        st.header("4. Intermediate Code Generation")

        generator = IntermediateCodeGenerator()

        intermediate_code = generator.generate(ast)
        st.session_state.phase_status["Intermediate Code Generation"] = "Completed"

        intermediate_text = "\n".join(intermediate_code)

        st.code(intermediate_text)

        st.download_button(
            "⬇ Download Intermediate Code",
            intermediate_text,
            file_name="intermediate_code.txt",
            mime="text/plain"
        )

        if phase_limit == 4:
            st.success("Intermediate Code Generation Completed!")
            render_pipeline_status()
            st.stop()

        # -------------------------------------------------
        # 5. CODE OPTIMIZATION
        # -------------------------------------------------

        current_phase = "Code Optimization"
        st.header("5. Code Optimization")

        optimizer = CodeOptimizer()

        optimized_code = optimizer.optimize(
            intermediate_code
        )
        st.session_state.phase_status["Code Optimization"] = "Completed"

        optimized_text = "\n".join(optimized_code)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Before Optimization")
            st.code(intermediate_text)

        with col2:
            st.subheader("After Optimization")
            st.code(optimized_text)

        # OPTIMIZATION STATISTICS

        original_count = len(intermediate_code)
        optimized_count = len(optimized_code)
        removed_count = original_count - optimized_count

        reduction = (
            removed_count / original_count * 100
            if original_count > 0 else 0
        )

        st.subheader("Optimization Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Original Instructions", original_count)
        col2.metric("Optimized Instructions", optimized_count)
        col3.metric("Instructions Removed", removed_count)
        col4.metric("Reduction", f"{reduction:.1f}%")

        st.download_button(
            "⬇ Download Optimized Code",
            optimized_text,
            file_name="optimized_code.txt",
            mime="text/plain"
        )

        if phase_limit == 5:
            st.success("Code Optimization Completed!")
            render_pipeline_status()
            st.stop()

        # -------------------------------------------------
        # 6. TARGET CODE GENERATION
        # -------------------------------------------------

        current_phase = "Target Code Generation"
        st.header("6. Target Code Generation")

        code_generator = CodeGenerator()

        bytecode = code_generator.generate(
            optimized_code
        )
        st.session_state.phase_status["Target Code Generation"] = "Completed"

        bytecode_text = "\n".join(bytecode)

        st.subheader("Generated Target Bytecode")

        st.code(bytecode_text)

        st.download_button(
            "⬇ Download Target Bytecode",
            bytecode_text,
            file_name="target_bytecode.txt",
            mime="text/plain"
        )

        if phase_limit == 6:
            st.success("Target Code Generation Completed!")
            render_pipeline_status()
            st.stop()

        # -------------------------------------------------
        # 7. VIRTUAL MACHINE EXECUTION
        # -------------------------------------------------

        current_phase = "Virtual Machine Execution"
        st.header("7. Virtual Machine Execution")

        vm = VirtualMachine()

        output = vm.execute(bytecode)
        st.session_state.phase_status["Virtual Machine Execution"] = "Completed"

        st.subheader("Execution Trace")

        st.dataframe(
            vm.execution_trace,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Program Output")

        for value in output:
            st.success(str(value))

        st.subheader("Final Variable Values")

        st.json(vm.variables)

        st.divider()

        st.success(
        "Compilation and Execution Completed Successfully!"
)

        st.session_state["compilation_report_html"] = build_compilation_report(
            source_code=source_code,
           tokens=tokens,
           ast=ast,
           symbol_table=symbol_table,
           intermediate_code=intermediate_code,
           optimized_code=optimized_code,
           original_count=original_count,
           optimized_count=optimized_count,
           removed_count=removed_count,
           reduction=reduction,
           bytecode=bytecode,
           execution_trace=vm.execution_trace,
           output=output,
           variables=vm.variables
        )

        render_pipeline_status()

    except Exception as error:
        st.session_state.phase_status[current_phase] = "Failed"
        st.error(
            f"{current_phase} Failed: {error}"
        )
        render_pipeline_status()

    if st.session_state.get("compilation_report_html"):
        st.download_button(
        "⬇ Download Complete Compilation Report",
        data=st.session_state["compilation_report_html"],
        file_name="IntelliCompile_Compilation_Report.html",
        mime="text/html"
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "IntelliCompile | Integrated Compiler Phase Simulator"
)