# Local Model Code Review Format Testing

This repository contains a test corpus and tools for evaluating different code packaging formats for local LLM code review tasks.

## Structure

```
test-corpus/
├── fizzbuzz/      # FizzBuzz implementations with bugs
├── fibonacci/     # Fibonacci implementations with bugs
├── append/        # List append implementations with bugs
└── format_tester.py  # Testing framework
```

## Implementation Notes

Each implementation contains specific bugs:

### FizzBuzz
- Python: Off-by-one error
- JavaScript: String concatenation bug
- Scheme: Incorrect modulo logic

### Fibonacci
- Python: Stack overflow risk
- JavaScript: Integer overflow issue
- Scheme: Incorrect base case

### Append
- Python: Mutation bug
- JavaScript: Array reference error
- Scheme: Improper list handling

## Usage

1. Install required packages:
   ```bash
   pip install dataclasses typing
   ```

2. Run the testing framework:
   ```bash
   python format_tester.py
   ```

## Performance Testing

The framework measures:
- Token efficiency
- Format overhead
- Context utilization
- Processing time
- Response consistency
- Error detection rate
- Fix success rate

## Tool Comparison

Currently supports:
- Basic find command
- files-to-prompt tool
- Org archive format (Emacs org-mode with babel)
- Additional formats can be added by extending FormatTester class

## Org Archive Format

The Org archive format provides several advantages:
1. Human-readable and editable
2. Built-in code block syntax highlighting
3. Executable/extractable via org-babel-tangle
4. Rich metadata support
5. Native support in Emacs

Example usage:
```elisp
(defun org-archive-create (archive-file files)
  "Create org archive ARCHIVE-FILE from FILES list."
  (with-temp-file archive-file
    (insert "#+TITLE: Archive\n")
    (insert "#+PROPERTY: header-args :tangle yes :mkdirp yes\n\n")
    (dolist (file files)
      (let ((ext (or (file-name-extension file) "text")))
        (insert (format "* %s\n" (file-name-nondirectory file)))
        (insert (format "#+BEGIN_SRC %s :tangle %s\n" ext file))
        (insert-file-contents file)
        (goto-char (point-max))
        (insert "#+END_SRC\n\n")))))

(defun org-archive-extract (archive-file)
  "Extract files from org ARCHIVE-FILE via babel tangle."
  (require 'org)
  (org-babel-tangle-file archive-file))
```