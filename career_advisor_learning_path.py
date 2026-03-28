# ============================================================
#
# Scenario 2: AI Career Advisor & Learning Path Generator
#
# Objective:
#   Build a multi-step intelligent advisor system using agent
#   workflows.
#
# Problem Statement:
#   Students need guidance on career paths based on their
#   skills. The system should:
#     - Analyze student profile
#     - Suggest career roles
#     - Generate learning roadmap
#
# Agents to Build:
#   1. Profile Analyzer Agent
#      - Understands student background
#   2. Career Recommendation Agent
#      - Suggests suitable roles
#   3. Skill Gap Agent
#      - Identifies missing skills
#   4. Learning Path Agent
#      - Creates step-by-step roadmap
#
# Tasks to Implement:
#   - Sequential workflow
#   - State passing between agents
#   - Conditional logic (beginner vs intermediate)
#
# Sample Input:
#   "I know Python basics and statistics, and I want to
#    become a Data Scientist"
#
# Expected Output:
#   - Suggested roles (e.g., Data Scientist, Analyst)
#   - Skill gaps (ML, SQL, etc.)
#   - Learning roadmap (step-by-step)
#
# Tools Used: Python (logic-based workflow)
#


from typing import TypedDict, List

# ── Shared State ─────────────────────────────────────────────

class StudentState(TypedDict):
    raw_input: str
    skills: List[str]
    level: str                  # "beginner" | "intermediate" | "advanced"
    goal: str
    recommended_roles: List[str]
    skill_gaps: List[str]
    learning_path: List[str]


# ── Agent 1: Profile Analyzer ─────────────────────────────────

def profile_analyzer_agent(state: StudentState) -> StudentState:
    """Extracts skills, level, and goal from raw student input."""
    text = state["raw_input"].lower()

    # Known skills to detect
    all_skills = [
        "python", "java", "javascript", "sql", "r", "c++",
        "statistics", "machine learning", "ml", "deep learning",
        "excel", "tableau", "power bi", "html", "css", "react",
        "node", "django", "flask", "tensorflow", "pytorch",
        "data analysis", "nlp", "computer vision", "git"
    ]

    detected_skills = [skill for skill in all_skills if skill in text]

    # Normalize "ml" -> "machine learning"
    if "ml" in detected_skills and "machine learning" not in detected_skills:
        detected_skills.append("machine learning")

    # Determine level
    if any(w in text for w in ["advanced", "expert", "professional", "experienced"]):
        level = "advanced"
    elif any(w in text for w in ["intermediate", "some experience", "familiar", "working knowledge"]):
        level = "intermediate"
    else:
        level = "beginner"

    # Extract goal
    goal = "data scientist"  # default
    goal_keywords = {
        "data scientist": ["data scientist", "data science"],
        "web developer": ["web developer", "web development", "frontend", "backend", "full stack"],
        "ml engineer": ["ml engineer", "machine learning engineer"],
        "data analyst": ["data analyst", "data analysis"],
        "software engineer": ["software engineer", "software developer"],
    }
    for role, keywords in goal_keywords.items():
        if any(kw in text for kw in keywords):
            goal = role
            break

    state["skills"] = detected_skills
    state["level"] = level
    state["goal"] = goal
    return state


# ── Agent 2: Career Recommendation ───────────────────────────

def career_recommendation_agent(state: StudentState) -> StudentState:
    """Suggests suitable career roles based on skills and goal."""
    skills = state["skills"]
    goal = state["goal"]

    role_map = {
        "data scientist": {
            "primary": "Data Scientist",
            "related": ["ML Engineer", "Data Analyst", "AI Researcher", "Business Intelligence Analyst"]
        },
        "web developer": {
            "primary": "Full Stack Developer",
            "related": ["Frontend Developer", "Backend Developer", "UI/UX Engineer", "DevOps Engineer"]
        },
        "ml engineer": {
            "primary": "Machine Learning Engineer",
            "related": ["Data Scientist", "AI Engineer", "MLOps Engineer", "Research Scientist"]
        },
        "data analyst": {
            "primary": "Data Analyst",
            "related": ["Business Analyst", "BI Developer", "Data Engineer", "Reporting Analyst"]
        },
        "software engineer": {
            "primary": "Software Engineer",
            "related": ["Backend Developer", "Systems Engineer", "Cloud Engineer", "DevOps Engineer"]
        },
    }

    mapping = role_map.get(goal, role_map["data scientist"])
    recommended = [mapping["primary"]] + mapping["related"][:3]

    state["recommended_roles"] = recommended
    return state


# ── Agent 3: Skill Gap ────────────────────────────────────────

def skill_gap_agent(state: StudentState) -> StudentState:
    """Identifies missing skills for the target career."""
    goal = state["goal"]
    current_skills = set(state["skills"])

    required_skills_map = {
        "data scientist": ["python", "statistics", "machine learning", "sql", "deep learning", "tensorflow", "data analysis", "git"],
        "web developer": ["html", "css", "javascript", "react", "node", "git", "sql"],
        "ml engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "sql", "git", "docker"],
        "data analyst": ["python", "sql", "excel", "tableau", "statistics", "data analysis", "power bi"],
        "software engineer": ["python", "java", "sql", "git", "data structures", "algorithms", "system design"],
    }

    required = required_skills_map.get(goal, required_skills_map["data scientist"])
    gaps = [skill for skill in required if skill not in current_skills]

    state["skill_gaps"] = gaps
    return state


# ── Agent 4: Learning Path ────────────────────────────────────

def learning_path_agent(state: StudentState) -> StudentState:
    """Creates a step-by-step learning roadmap based on level and gaps."""
    gaps = state["skill_gaps"]
    level = state["level"]
    goal = state["goal"]

    path = []

    # Foundation phase (only for beginners)
    if level == "beginner":
        path.append("Phase 1 – Foundation (4 weeks)")
        path.append("  • Learn Python fundamentals (variables, loops, functions, OOP)")
        path.append("  • Practice on HackerRank / LeetCode (Easy problems)")
        path.append("  • Version control with Git & GitHub basics")

    # Core skills phase
    path.append(f"Phase {'2' if level == 'beginner' else '1'} – Core Skills (6 weeks)")
    for skill in gaps[:4]:
        path.append(f"  • Master: {skill.title()} — use freeCodeCamp / Coursera / YouTube")

    # Specialization phase
    path.append(f"Phase {'3' if level == 'beginner' else '2'} – Specialization (4 weeks)")
    for skill in gaps[4:]:
        path.append(f"  • Deep dive: {skill.title()} — Kaggle / official docs / projects")

    if not gaps[4:]:
        path.append(f"  • Build 2 end-to-end projects for {goal.title()}")
        path.append("  • Contribute to open-source or Kaggle competitions")

    # Career prep
    path.append(f"Phase {'4' if level == 'beginner' else '3'} – Career Prep (2 weeks)")
    path.append("  • Build portfolio on GitHub")
    path.append("  • Create LinkedIn profile with projects")
    path.append("  • Apply to internships / entry-level roles")
    path.append("  • Practice mock interviews on Pramp / Interviewing.io")

    state["learning_path"] = path
    return state


# ── Orchestrator ─────────────────────────────────────────────

def career_advisor_system(raw_input: str) -> str:
    """Sequential workflow: runs all 4 agents in order."""
    state: StudentState = {
        "raw_input": raw_input,
        "skills": [],
        "level": "",
        "goal": "",
        "recommended_roles": [],
        "skill_gaps": [],
        "learning_path": []
    }

    # Sequential agent pipeline
    state = profile_analyzer_agent(state)
    state = career_recommendation_agent(state)
    state = skill_gap_agent(state)
    state = learning_path_agent(state)

    # Format output
    output = []
    output.append("\n" + "="*55)
    output.append("  AI CAREER ADVISOR — PERSONALIZED REPORT")
    output.append("="*55)
    output.append(f"  Input    : {state['raw_input']}")
    output.append(f"  Level    : {state['level'].capitalize()}")
    output.append(f"  Goal     : {state['goal'].title()}")
    output.append(f"  Skills   : {', '.join(state['skills']) if state['skills'] else 'None detected'}")
    output.append("─"*55)

    output.append("\n  RECOMMENDED ROLES:")
    for i, role in enumerate(state["recommended_roles"], 1):
        output.append(f"    {i}. {role}")

    output.append("\n  SKILL GAPS TO FILL:")
    if state["skill_gaps"]:
        for gap in state["skill_gaps"]:
            output.append(f"    ✗ {gap.title()}")
    else:
        output.append("    ✓ No major gaps — you're well prepared!")

    output.append("\n  LEARNING ROADMAP:")
    for step in state["learning_path"]:
        output.append(f"    {step}")

    output.append("="*55 + "\n")
    return "\n".join(output)


# ── Test Cases ───────────────────────────────────────────────

if __name__ == "__main__":
    profiles = [
        "I know Python basics and statistics, and I want to become a Data Scientist",
        "I have intermediate knowledge of HTML, CSS and JavaScript and want to become a web developer"
    ]

    for profile in profiles:
        print(career_advisor_system(profile))
