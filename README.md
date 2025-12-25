Codebase Quality Reviewer : 
A static code analysis tool that reviews a given Python codebase and identifies quality issues across multiple categories such as formatting, deprecated usage, maintainability, organization, and code smells.This tool helps developers improve readability, scalability, and long-term maintainability of their code.

Features : 
Analyze single Python files or entire folders
AST-based static code analysis
Categorized rules with severity levels
Generates JSON report (CI/CD friendly)
Easily extensible rule-based architecture

Categories of Issues Detected:
Deprecated Usage-Deprecated modules (example: imp)
Maintainability-Long functions,Too many parameters
Code Smells-Deep nesting
Organization-Large files

Project Structure:
code_quality_reviewer/
│
├── reviewer.py        # Main analyzer script
├── sample_input.py    # Sample input file for testing
└── report.json        # Generated output (after execution)

Requirements:
Python 3.10 or higher
No external dependencies

How to Run:
Step 1: Navigate to the project folder
cd C:\Users\phani\OneDrive\Desktop\codebase\code_quality_reviewer

Step 2: Run on a single file
python reviewer.py sample_input.py

Step 3: Run on an entire folder
python reviewer.py .

Output:
After execution, a file named report.json is generated.

Sample Output
[
  {
    "file": "sample_input.py",
    "rule_id": "DEPR_001",
    "category": "Deprecated",
    "severity": "HIGH",
    "message": "Deprecated module 'imp' used",
    "line": 1
  }
]

Implemented Rules:
Rule ID	Category	Description	Severity
DEPR_001	Deprecated	Usage of deprecated modules	HIGH
MAINT_001	Maintainability	Function too long	MEDIUM
MAINT_002	Maintainability	Too many function parameters	MEDIUM
SMELL_001	Code Smell	Deep nesting detected	MEDIUM
ORG_001	Organization	File too large	MEDIUM
Extending the Tool

Author
Manaswini Navuluru
