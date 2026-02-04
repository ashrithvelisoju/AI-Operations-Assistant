"""
AI Operations Assistant - Streamlit Interface
Beautiful UI for the multi-agent AI assistant
"""
import sys
import os
import json

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from main import AIOperationsAssistant
from tools import TOOL_DESCRIPTIONS

# Page configuration
st.set_page_config(
    page_title="AI Operations Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    .stApp {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: #00d4ff;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #a0aec0;
        font-size: 1.1rem;
    }
    
    .agent-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .agent-card h3 {
        color: #00d4ff;
        margin-bottom: 0.5rem;
    }
    
    .status-success {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-error {
        color: #ef4444;
        font-weight: 600;
    }
    
    .status-pending {
        color: #f59e0b;
        font-weight: 600;
    }
    
    .tool-badge {
        display: inline-block;
        background: #3b82f6;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    
    .step-container {
        background: #0f172a;
        border-left: 4px solid #00d4ff;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .final-answer {
        background: linear-gradient(135deg, #065f46 0%, #064e3b 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .final-answer h3 {
        color: #34d399;
        margin-bottom: 1rem;
    }
    
    .final-answer p {
        color: #d1fae5;
        line-height: 1.6;
    }
    
    .stTextInput > div > div > input {
        background: #1e293b;
        border: 2px solid #334155;
        border-radius: 12px;
        color: white;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: #0f172a;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.3);
    }
    
    .sidebar .stMarkdown h2 {
        color: #00d4ff;
    }
    
    code {
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stExpander {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "assistant" not in st.session_state:
    st.session_state.assistant = AIOperationsAssistant()
if "history" not in st.session_state:
    st.session_state.history = []
if "current_result" not in st.session_state:
    st.session_state.current_result = None

# Sidebar
with st.sidebar:
    st.markdown("## 🛠️ Available Tools")
    
    for tool_name, tool_desc in TOOL_DESCRIPTIONS.items():
        st.markdown(f"""
        <div style="background: #1e293b; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <strong style="color: #00d4ff;">{tool_name.upper()}</strong>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">{tool_desc}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 🏗️ Architecture")
    st.markdown("""
    <div style="background: #1e293b; padding: 1rem; border-radius: 8px;">
        <p style="color: #94a3b8;">
        <strong style="color: #f59e0b;">1. Planner</strong> → Creates execution plan<br>
        <strong style="color: #3b82f6;">2. Executor</strong> → Calls APIs & tools<br>
        <strong style="color: #10b981;">3. Verifier</strong> → Validates & synthesizes
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📝 Example Tasks")
    examples = [
        "What's the weather in New York?",
        "Get me the latest tech news",
        "Weather in London and top headlines",
        "Compare weather in Tokyo and Paris"
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.task_input = ex

# Main content
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Operations Assistant</h1>
    <p>Multi-agent AI system powered by Gemini 3 Flash</p>
</div>
""", unsafe_allow_html=True)

# Task input
col1, col2 = st.columns([4, 1])
with col1:
    task = st.text_input(
        "Enter your task",
        placeholder="e.g., What's the weather in San Francisco and show me tech news",
        key="task_input",
        label_visibility="collapsed"
    )
with col2:
    process_btn = st.button("🚀 Process", use_container_width=True, type="primary")

# Process task
if process_btn and task:
    with st.spinner("🔄 Processing through multi-agent pipeline..."):
        result = st.session_state.assistant.process_task(task)
        st.session_state.current_result = result
        st.session_state.history.append({"task": task, "result": result})

# Display results
if st.session_state.current_result:
    result = st.session_state.current_result
    
    # Status indicator
    status = result.get("status", "unknown")
    status_emoji = "✅" if status == "complete" else "⚠️" if status == "partial" else "❌"
    st.markdown(f"### {status_emoji} Status: {status.upper()}")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Final Answer", "📊 Planning", "⚡ Execution", "✔️ Verification"])
    
    with tab1:
        st.markdown(f"""
        <div class="final-answer">
            <h3>🎯 Answer</h3>
            <p>{result.get('final_answer', 'No answer generated')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        planning = result.get("stages", {}).get("planning", {})
        if planning.get("status") == "success":
            plan = planning.get("plan", {})
            
            st.markdown("#### 📝 Task Summary")
            st.info(plan.get("task_summary", "N/A"))
            
            st.markdown("#### 🔢 Execution Steps")
            for step in plan.get("steps", []):
                tool_badge = f'<span class="tool-badge">{step.get("tool", "reasoning")}</span>' if step.get("tool") else '<span class="tool-badge">reasoning</span>'
                st.markdown(f"""
                <div class="step-container">
                    <strong>Step {step.get('step_number', '?')}</strong> {tool_badge}<br>
                    <span style="color: #94a3b8;">Action:</span> {step.get('action', 'N/A')}<br>
                    <span style="color: #94a3b8;">Input:</span> {step.get('tool_input', 'N/A')}<br>
                    <span style="color: #94a3b8;">Expected:</span> {step.get('expected_output', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"Planning failed: {planning.get('error', 'Unknown error')}")
    
    with tab3:
        execution = result.get("stages", {}).get("execution", {})
        if execution.get("status") == "success":
            exec_results = execution.get("results", {})
            
            st.markdown(f"#### Overall Status: **{exec_results.get('overall_status', 'N/A').upper()}**")
            
            for step in exec_results.get("steps", []):
                status_class = "status-success" if step.get("status") == "success" else "status-error"
                
                with st.expander(f"Step {step.get('step_number', '?')}: {step.get('action', 'N/A')[:50]}..."):
                    st.markdown(f"**Status:** <span class='{status_class}'>{step.get('status', 'N/A').upper()}</span>", unsafe_allow_html=True)
                    
                    if step.get("tool_used"):
                        st.markdown(f"**Tool:** `{step.get('tool_used')}`")
                    
                    if step.get("error"):
                        st.error(step.get("error"))
                    
                    if step.get("output"):
                        st.json(step.get("output"))
        else:
            st.error(f"Execution failed: {execution.get('error', 'Unknown error')}")
    
    with tab4:
        verification = result.get("stages", {}).get("verification", {})
        if verification.get("status") == "success":
            verify_data = verification.get("verification", {})
            
            v_status = verify_data.get("verification_status", "unknown")
            status_color = "#10b981" if v_status == "complete" else "#f59e0b" if v_status == "partial" else "#ef4444"
            
            st.markdown(f"""
            <div style="background: #1e293b; padding: 1rem; border-radius: 8px; border-left: 4px solid {status_color};">
                <strong>Verification Status:</strong> <span style="color: {status_color};">{v_status.upper()}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if verify_data.get("issues_found"):
                st.markdown("#### ⚠️ Issues Found")
                for issue in verify_data.get("issues_found", []):
                    st.warning(issue)
            
            if verify_data.get("suggestions"):
                st.markdown("#### 💡 Suggestions")
                for suggestion in verify_data.get("suggestions", []):
                    st.info(suggestion)
        else:
            st.error(f"Verification failed: {verification.get('error', 'Unknown error')}")
    
    # Raw JSON view
    with st.expander("🔍 View Raw JSON Response"):
        st.json(result)

# History section
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 📜 Recent Tasks")
    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"Task: {item['task'][:50]}..."):
            st.markdown(f"**Answer:** {item['result'].get('final_answer', 'N/A')[:200]}...")
