import os
import ast
import json
import argparse

# -----------------------------
# File Scanner
# -----------------------------
def get_python_files(path):
    files = []

    if os.path.isfile(path) and path.endswith(".py"):
        return [path]

    for root, _, filenames in os.walk(path):
        for file in filenames:
            if file.endswith(".py"):
                files.append(os.path.join(root, file))

    return files


# -----------------------------
# Rule Base Class
# -----------------------------
class Rule(ast.NodeVisitor):
    RULE_ID = ""
    CATEGORY = ""
    SEVERITY = ""

    def __init__(self, file_path):
        self.file_path = file_path
        self.issues = []

    def report(self, message, line):
        self.issues.append({
            "file": self.file_path,
            "rule_id": self.RULE_ID,
            "category": self.CATEGORY,
            "severity": self.SEVERITY,
            "message": message,
            "line": line
        })


# -----------------------------
# RULES
# -----------------------------

# 1. Long Function Rule
class LongFunctionRule(Rule):
    RULE_ID = "MAINT_001"
    CATEGORY = "Maintainability"
    SEVERITY = "MEDIUM"
    MAX_LINES = 50

    def visit_FunctionDef(self, node):
        length = node.end_lineno - node.lineno
        if length > self.MAX_LINES:
            self.report(
                f"Function '{node.name}' too long ({length} lines)",
                node.lineno
            )
        self.generic_visit(node)


# 2. Deprecated Import Rule
class DeprecatedImportRule(Rule):
    RULE_ID = "DEPR_001"
    CATEGORY = "Deprecated"
    SEVERITY = "HIGH"

    DEPRECATED_MODULES = {"imp", "optparse"}

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in self.DEPRECATED_MODULES:
                self.report(
                    f"Deprecated module '{alias.name}' used",
                    node.lineno
                )

    def visit_ImportFrom(self, node):
        if node.module in self.DEPRECATED_MODULES:
            self.report(
                f"Deprecated module '{node.module}' used",
                node.lineno
            )


# 3. Too Many Parameters Rule
class TooManyParametersRule(Rule):
    RULE_ID = "MAINT_002"
    CATEGORY = "Maintainability"
    SEVERITY = "MEDIUM"
    MAX_PARAMS = 5

    def visit_FunctionDef(self, node):
        if len(node.args.args) > self.MAX_PARAMS:
            self.report(
                f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                node.lineno
            )
        self.generic_visit(node)


# 4. Deep Nesting Rule
class DeepNestingRule(Rule):
    RULE_ID = "SMELL_001"
    CATEGORY = "Code Smell"
    SEVERITY = "MEDIUM"
    MAX_DEPTH = 3

    def visit(self, node, depth=0):
        if isinstance(node, (ast.If, ast.For, ast.While)):
            depth += 1
            if depth > self.MAX_DEPTH:
                self.report("Deep nesting detected", node.lineno)

        for child in ast.iter_child_nodes(node):
            self.visit(child, depth)


# 5. Large File Rule (Non-AST)
def check_large_file(file_path, max_lines=500):
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) > max_lines:
        return {
            "file": file_path,
            "rule_id": "ORG_001",
            "category": "Organization",
            "severity": "MEDIUM",
            "message": f"File too large ({len(lines)} lines)",
            "line": 1
        }


# -----------------------------
# Analyzer
# -----------------------------
def analyze_file(file_path):
    issues = []

    # Non-AST rule
    large_file_issue = check_large_file(file_path)
    if large_file_issue:
        issues.append(large_file_issue)

    try:
        with open(file_path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except SyntaxError:
        return issues

    rules = [
        LongFunctionRule(file_path),
        DeprecatedImportRule(file_path),
        TooManyParametersRule(file_path),
        DeepNestingRule(file_path)
    ]

    for rule in rules:
        rule.visit(tree)
        issues.extend(rule.issues)

    return issues


# -----------------------------
# Main Entry
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Codebase Quality Reviewer")
    parser.add_argument("path", help="File or folder to analyze")
    parser.add_argument("-o", "--output", default="report.json")

    args = parser.parse_args()

    files = get_python_files(args.path)
    all_issues = []

    for file in files:
        all_issues.extend(analyze_file(file))

    with open(args.output, "w") as f:
        json.dump(all_issues, f, indent=2)

    print(f"✔ Analysis complete. Report saved to {args.output}")
    print(f"✔ Issues found: {len(all_issues)}")


if __name__ == "__main__":
    main()
