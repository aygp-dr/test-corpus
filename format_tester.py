from dataclasses import dataclass
from typing import Dict, Any
import time
import subprocess
import json

@dataclass
class FormatMetrics:
    # Token efficiency
    tokens_per_file: int          # Average tokens used per file
    format_overhead: float        # Percentage of tokens used for formatting
    context_utilization: float    # Effective use of context window
    
    # Processing overhead
    generation_time: float        # Time to generate format
    parse_time: float            # Time to parse response
    
    # Model interaction
    response_consistency: float   # How consistently model follows format
    error_detection_rate: float   # Rate of successful bug detection
    fix_success_rate: float      # Rate of successful fixes
    
    # Tool-specific
    setup_complexity: int        # Steps required for setup (0-5)
    automation_friendly: bool    # Easy to use in scripts
    preserves_metadata: bool     # Keeps file attributes
    bidirectional: bool         # Can recreate files from output

class FormatTester:
    def __init__(self, 
                 corpus_path: str,
                 model_name: str = "codellama:7b",
                 format_tool: str = "find"):
        self.corpus_path = corpus_path
        self.model_name = model_name
        self.format_tool = format_tool
        
    def _package_with_find(self) -> str:
        """Package corpus using find command."""
        cmd = f'find {self.corpus_path} -type f \\( -name "*.py" -o -name "*.js" -o -name "*.scm" \\) -exec sh -c \'echo "### FILE: $1"; cat "$1"; echo "### END"\' sh {{}} \\;'
        start_time = time.time()
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self.generation_time = time.time() - start_time
        return result.stdout
    
    def _package_with_files_to_prompt(self) -> str:
        """Package corpus using files-to-prompt tool."""
        cmd = f'files-to-prompt {self.corpus_path} ' \
              f'--extensions py,js,scm ' \
              f'--comment-prefix "# " ' \
              f'--separator "---" ' \
              f'--include-filenames'
        start_time = time.time()
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        self.generation_time = time.time() - start_time
        return result.stdout

    def _package_with_markdown(self) -> str:
        """Package corpus using Markdown format with literate programming style."""
        start_time = time.time()
        output = "# Code Review Archive\n\n"
        output += "## Overview\n"
        output += "This archive contains code files for review in literate programming style.\n\n"
        
        # Find all relevant files
        cmd = f'find {self.corpus_path} -type f \\( -name "*.py" -o -name "*.js" -o -name "*.scm" \\)'
        files = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip().split('\n')
        
        for file in files:
            if not file:  # Skip empty lines
                continue
            filename = file.split('/')[-1]
            ext = filename.split('.')[-1] if '.' in filename else "text"
            
            # Add file header with metadata
            output += f"## {filename}\n\n"
            output += f"Language: {ext}\n"
            output += f"Path: {file}\n\n"
            
            # Read and analyze the file
            with open(file, 'r') as f:
                content = f.read()
                
            # Add code block with language-specific syntax highlighting
            output += "### Source Code\n\n"
            output += f"```{ext}\n{content}\n```\n\n"
            
            # Add placeholder for analysis section
            output += "### Analysis\n\n"
            output += "- Code structure:\n"
            output += "- Potential issues:\n"
            output += "- Improvement suggestions:\n\n"
            
            # Add separator between files
            output += "---\n\n"
            
        self.generation_time = time.time() - start_time
        return output

    def _package_with_org_archive(self) -> str:
        """Package corpus using Org archive format."""
        start_time = time.time()
        output = "#+TITLE: Code Review Archive\n"
        output += "#+PROPERTY: header-args :tangle yes :mkdirp yes\n\n"
        
        # Find all relevant files
        cmd = f'find {self.corpus_path} -type f \\( -name "*.py" -o -name "*.js" -o -name "*.scm" \\)'
        files = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip().split('\n')
        
        for file in files:
            if not file:  # Skip empty lines
                continue
            filename = file.split('/')[-1]
            ext = filename.split('.')[-1] if '.' in filename else "text"
            
            output += f"* {filename}\n"
            output += f"#+BEGIN_SRC {ext} :tangle {file}\n"
            with open(file, 'r') as f:
                output += f.read()
            output += "\n#+END_SRC\n\n"
            
        self.generation_time = time.time() - start_time
        return output
        
    def package_corpus(self) -> str:
        """Package corpus using selected tool."""
        if self.format_tool == "find":
            return self._package_with_find()
        elif self.format_tool == "files-to-prompt":
            return self._package_with_files_to_prompt()
        elif self.format_tool == "org-archive":
            return self._package_with_org_archive()
        elif self.format_tool == "markdown":
            return self._package_with_markdown()
        else:
            raise ValueError(f"Unsupported format tool: {self.format_tool}")
            
    def _measure_consistency(self, response: str) -> float:
        """Measure how consistently the model follows the format."""
        # Implementation details here
        return 0.85  # Example value
        
    def _measure_error_detection(self, response: str) -> float:
        """Measure rate of successful bug detection."""
        # Implementation details here
        return 0.82  # Example value
        
    def _measure_fix_success(self, response: str) -> float:
        """Measure rate of successful fixes."""
        # Implementation details here
        return 0.78  # Example value
        
    def evaluate_response(self, response: str) -> Dict[str, float]:
        """Evaluate model response metrics."""
        return {
            'response_consistency': self._measure_consistency(response),
            'error_detection': self._measure_error_detection(response),
            'fix_success': self._measure_fix_success(response)
        }
        
    def _measure_format_metrics(self, packed: str) -> FormatMetrics:
        """Measure format-specific metrics."""
        # Example implementation
        return FormatMetrics(
            tokens_per_file=500,          # Example values
            format_overhead=0.15,
            context_utilization=0.85,
            generation_time=self.generation_time,
            parse_time=0.05,
            response_consistency=0.9,
            error_detection_rate=0.85,
            fix_success_rate=0.8,
            setup_complexity=1,
            automation_friendly=True,
            preserves_metadata=True,
            bidirectional=True
        )
        
    def run_benchmark(self) -> Dict[str, Any]:
        """Run complete benchmark suite."""
        packed = self.package_corpus()
        metrics = self._measure_format_metrics(packed)
        response = "Example model response"  # Would actually call model here
        results = self.evaluate_response(response)
        
        return {
            'format_metrics': metrics,
            'model_results': results
        }

def generate_comparison_report(results: Dict[str, Dict[str, Any]]) -> str:
    """Generate a comparison report from benchmark results."""
    report = ["# Format Comparison Report\n"]
    
    for model, model_results in results.items():
        report.append(f"\n## Model: {model}\n")
        report.append("| Tool | Token Efficiency | Context Usage | Error Detection | Fix Success |")
        report.append("|------|-----------------|---------------|-----------------|-------------|")
        
        for tool, tool_results in model_results.items():
            metrics = tool_results['format_metrics']
            report.append(
                f"| {tool} | {metrics.context_utilization*100:.0f}% | "
                f"{metrics.context_utilization*100:.0f}% | "
                f"{metrics.error_detection_rate*100:.0f}% | "
                f"{metrics.fix_success_rate*100:.0f}% |"
            )
    
    return "\n".join(report)

if __name__ == "__main__":
    # Example usage
    tools = ['find', 'files-to-prompt', 'org-archive', 'markdown']
    models = ['codellama:7b', 'mistral:7b']
    
    results = {}
    for model in models:
        model_results = {}
        for tool in tools:
            tester = FormatTester(
                corpus_path="test-corpus",
                model_name=model,
                format_tool=tool
            )
            model_results[tool] = tester.run_benchmark()
        results[model] = model_results
    
    # Generate and print report
    print(generate_comparison_report(results))