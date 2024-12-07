#!/usr/bin/env python3
"""
Test harness for code review format evaluation.
"""

import subprocess
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Any, Tuple
import tempfile
import os

@dataclass
class TestResult:
    format_name: str
    model_name: str
    bugs_identified: int
    fixes_correct: int
    execution_time: float
    token_efficiency: float
    success_rate: float
    raw_response: str

class FormatTester:
    FORMATS = {
        'find': {
            'command': 'find_command',
            'options': {'basic': None}
        },
        'files-to-prompt': {
            'command': 'files_to_prompt',
            'options': {
                'default': None,
                'cxml': '-cxml'
            }
        },
        'org': {
            'command': 'org_archive',
            'options': {'basic': None}
        },
        'markdown': {
            'command': 'markdown_literate',
            'options': {'basic': None}
        }
    }

    MODELS = [
        'phi3:latest',
        'hf.co/MaziyarPanahi/Qwen2.5-7B-Instruct-abliterated-v2-GGUF:Q5_K_M',
        'llama3.2:latest',
        'zephyr:latest',
        'llama3.1:latest'
    ]

    def __init__(self, corpus_path: str):
        self.corpus_path = corpus_path
        self.results: Dict[str, Dict[str, TestResult]] = {}

    def _format_with_find(self, options: Dict = None) -> str:
        """Format using find command."""
        cmd = (f'find {self.corpus_path} -type f '
               '\\( -name "*.py" -o -name "*.js" -o -name "*.scm" \\) '
               '-exec sh -c \'echo "### FILE: $1"; cat "$1"; echo "### END"\' '
               'sh {} \\;')
        return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

    def _format_with_files_to_prompt(self, options: Dict = None) -> str:
        """Format using files-to-prompt."""
        cmd = ['files-to-prompt', self.corpus_path]
        if isinstance(options, dict) and options.get('cxml'):
            cmd.append('-cxml')
        return subprocess.run(cmd, capture_output=True, text=True).stdout

    def _package_with_markdown(self, options: Dict = None) -> str:
        """Package corpus using Markdown format."""
        output = "# Code Review Archive\n\n"
        
        cmd = (f'find {self.corpus_path} -type f '
               '\\( -name "*.py" -o -name "*.js" -o -name "*.scm" \\)')
        files = subprocess.run(cmd, shell=True, capture_output=True,
                             text=True).stdout.strip().split('\n')
        
        for file in files:
            if not file:
                continue
            filename = file.split('/')[-1]
            ext = filename.split('.')[-1] if '.' in filename else "text"
            
            output += f"## {filename}\n\n"
            output += f"Language: {ext}\n"
            output += f"Path: {file}\n\n"
            
            with open(file, 'r') as f:
                content = f.read()
                
            output += f"```{ext}\n{content}\n```\n\n"
            
        return output

    def _package_with_org_archive(self, options: Dict = None) -> str:
        """Package corpus using Org archive format."""
        output = "#+TITLE: Code Review Archive\n"
        output += "#+PROPERTY: header-args :tangle yes :mkdirp yes\n\n"
        
        cmd = (f'find {self.corpus_path} -type f '
               '\\( -name "*.py" -o -name "*.js" -o -name "*.scm" \\)')
        files = subprocess.run(cmd, shell=True, capture_output=True,
                             text=True).stdout.strip().split('\n')
        
        for file in files:
            if not file:
                continue
            filename = file.split('/')[-1]
            ext = filename.split('.')[-1] if '.' in filename else "text"
            
            output += f"* {filename}\n"
            output += f"#+BEGIN_SRC {ext} :tangle {file}\n"
            with open(file, 'r') as f:
                output += f.read()
            output += "\n#+END_SRC\n\n"
            
        return output

    def _get_ollama_response(self, model: str, prompt: str) -> Tuple[str, float]:
        """Get response from Ollama model using direct curl API calls."""
        start_time = time.time()
        
        # Prepare a focused code review prompt
        system_prompt = {
            "role": "system",
            "content": """You are a code review assistant specialized in finding bugs and suggesting fixes.
For each file:
1. Identify specific bugs and issues
2. Provide line numbers for each issue
3. Suggest concrete fixes
4. Rate severity of each issue (high/medium/low)
Format your response as:
[File: filename]
- Bug: description (line X) [severity]
  Fix: specific solution
Ensure all suggestions maintain the original code's intent."""
        }
        
        data = {
            "model": model,
            "messages": [
                system_prompt,
                {
                    "role": "user",
                    "content": f"Review this code for bugs and suggest fixes:\n\n{prompt}"
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower temperature for more focused analysis
                "top_p": 0.9,        # Maintain some creativity while being precise
                "max_tokens": 2048   # Allow for detailed analysis
            }
        }
        
        # Use heredoc to handle JSON properly
        curl_cmd = f"""curl -s -X POST http://localhost:11434/api/chat -d '{json.dumps(data)}'"""
        
        try:
            response = subprocess.run(
                curl_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # Add timeout to prevent hanging
            )
            
            if response.returncode != 0:
                print(f"Error calling Ollama API: {response.stderr}")
                return f"Error: API call failed - {response.stderr}", time.time() - start_time
            
            try:
                result = json.loads(response.stdout)
                return result.get('response', 'No response in API result'), time.time() - start_time
            except json.JSONDecodeError:
                print(f"Error parsing API response: {response.stdout}")
                return f"Error: Invalid JSON response - {response.stdout[:100]}...", time.time() - start_time
                
        except subprocess.TimeoutExpired:
            return "Error: API call timed out", time.time() - start_time
        except Exception as e:
            return f"Error: {str(e)}", time.time() - start_time

    def _evaluate_response(self, category: str, response: str) -> Dict[str, bool]:
        """Evaluate if response correctly identifies and fixes bugs."""
        expected_bugs = {
            'fizzbuzz': ['off_by_one', 'range error', 'modulo'],
            'fibonacci': ['stack overflow', 'integer overflow', 'base case'],
            'append': ['mutation', 'reference', 'improper list']
        }
        
        bugs = expected_bugs[category]
        identified = sum(1 for bug in bugs if bug.lower() in response.lower())
        
        # Look for specific fix patterns
        fixes = {
            'fizzbuzz': ['range(1, n + 1)', 'return', 'modulo'],
            'fibonacci': ['iterative', 'big_number', 'if n <= 1'],
            'append': ['new_list', 'slice', 'proper_list']
        }
        
        correct_fixes = sum(1 for fix in fixes[category] 
                          if fix.lower() in response.lower())
        
        return {
            'bugs_identified': identified,
            'fixes_correct': correct_fixes,
            'success_rate': (identified + correct_fixes) / (len(bugs) + len(fixes[category]))
        }

    def run_test(self, model: str, format_name: str, options: Dict = None) -> TestResult:
        """Run test for specific model and format combination."""
        format_funcs = {
            'find': self._format_with_find,
            'files-to-prompt': self._format_with_files_to_prompt,
            'org': self._package_with_org_archive,
            'markdown': self._package_with_markdown
        }
        
        # Format the code
        formatted_code = format_funcs[format_name](options)
        
        # Get model response
        response, exec_time = self._get_ollama_response(model, formatted_code)
        
        # Calculate token efficiency (formatted / original)
        orig_size = sum(len(open(f).read()) for f in self._get_files())
        token_efficiency = len(formatted_code) / orig_size if orig_size > 0 else 0
        
        # Evaluate results for each category
        results = []
        for category in ['fizzbuzz', 'fibonacci', 'append']:
            results.append(self._evaluate_response(category, response))
        
        # Average the results
        avg_bugs = sum(r['bugs_identified'] for r in results) / len(results)
        avg_fixes = sum(r['fixes_correct'] for r in results) / len(results)
        avg_success = sum(r['success_rate'] for r in results) / len(results)
        
        return TestResult(
            format_name=format_name,
            model_name=model,
            bugs_identified=avg_bugs,
            fixes_correct=avg_fixes,
            execution_time=exec_time,
            token_efficiency=token_efficiency,
            success_rate=avg_success,
            raw_response=response
        )

    def _get_files(self) -> List[str]:
        """Get list of test files."""
        cmd = (f'find {self.corpus_path} -type f '
               '\\( -name "*.py" -o -name "*.js" -o -name "*.scm" \\)')
        return subprocess.run(cmd, shell=True, capture_output=True, 
                            text=True).stdout.strip().split('\n')

    def run_all_tests(self):
        """Run tests for all model and format combinations."""
        for model in self.MODELS:
            self.results[model] = {}
            for format_name, format_config in self.FORMATS.items():
                for option_name, option in format_config['options'].items():
                    test_id = f"{format_name}_{option_name}"
                    self.results[model][test_id] = self.run_test(
                        model, format_name, option
                    )

    def generate_report(self) -> str:
        """Generate markdown report of test results."""
        report = ["# Code Review Format Test Results\n"]
        
        # Add summary table
        report.append("## Summary\n")
        report.append("| Format | Model | Success Rate | Token Efficiency | Avg Time |")
        report.append("|--------|-------|--------------|-----------------|----------|")
        
        for model, format_results in self.results.items():
            for format_id, result in format_results.items():
                report.append(
                    f"| {format_id} | {model} | "
                    f"{result.success_rate:.1%} | "
                    f"{result.token_efficiency:.1%} | "
                    f"{result.execution_time:.1f}s |"
                )
        
        # Add detailed results
        report.append("\n## Detailed Results\n")
        for model, format_results in self.results.items():
            report.append(f"\n### {model}\n")
            for format_id, result in format_results.items():
                report.append(f"\n#### {format_id}\n")
                report.append(f"- Bugs Identified: {result.bugs_identified}")
                report.append(f"- Correct Fixes: {result.fixes_correct}")
                report.append(f"- Token Efficiency: {result.token_efficiency:.1%}")
                report.append(f"- Execution Time: {result.execution_time:.1f}s")
                report.append("\nResponse Preview:")
                report.append("```")
                report.append(result.raw_response[:500] + "...")
                report.append("```")
        
        return "\n".join(report)

if __name__ == "__main__":
    # Run a minimal test first
    tester = FormatTester("/home/computeruse/test-corpus")
    
    # Test with just one model and format
    model = 'phi3:latest'
    format_name = 'find'
    result = tester.run_test(model, format_name, None)
    
    # Print results
    print(f"\nTest Results for {model} with {format_name}:")
    print(f"Success Rate: {result.success_rate:.1%}")
    print(f"Token Efficiency: {result.token_efficiency:.1%}")
    print(f"Execution Time: {result.execution_time:.1f}s")
    print("\nRaw Response Preview:")
    print("=" * 80)
    print(result.raw_response[:500])
    print("=" * 80)