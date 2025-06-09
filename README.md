## Plagiarism Detector with AES Encryption

A tool for detecting plagiarism in text files using string matching algorithms (KMP by default), with optional AES encryption for secure submission handling.

---

### Setup

To get started, follow these steps:

1.  **Clone the repository and install dependencies:**

    ```bash
    git clone https://github.com/Harshitheccentric/secure-plagiarism-checker.git
    cd secure-plagiarism-checker
    pip install -r requirements.txt
    ```

2.  **Create required directories:**

    ```bash
    mkdir submissions decrypted
    ```

3.  **Place your `.txt` files in the `submissions/` directory.**

---

### Usage

**1. Basic Run:**

To run the plagiarism checker with the default KMP algorithm:

```bash
python checker.py
```
### Alternate Run Options

You can customize the comparison method or choose to keep decrypted files:

* **Run with different comparison methods:**
    ```bash
    python checker.py word_based
    python checker.py char_based
    python checker.py line_based
    ```

* **Keep decrypted files for inspection:**
    ```bash
    python checker.py --no-cleanup
    ```

* **Get help:**
    ```bash
    python checker.py --help
    ```

---

### Note

To use automatically generated demo files, **uncomment the demo generator lines** under the `run_full_pipeline()` method in `checker.py`.

Decrypted files are cleaned after processing by default, unless `--no-cleanup` is specified.
Decrypted files are cleaned after processing by default, unless --no-cleanup is specified.
