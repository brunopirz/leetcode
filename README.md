# leetcode
leet code helper.py

# Selective Screen Capture with LLM Integration

This application allows you to selectively capture an area of ​​the screen using an intuitive graphical interface based on Tkinter, with capture preview and integration with language models (LLM). It has a hidden mode for greater privacy.

## Main Features
- **Selective screen capture:** Dynamically select any area of ​​the screen to capture.
- **Preview:** See a thumbnail of the capture before saving or processing.
- **Hidden mode:** Allows you to hide the preview window for greater privacy.
- **LLM integration:** Possibility to send the capture to a language model for analysis or processing (requires API configuration).

## Installation
1. Clone this repository or download the files.
2. Install the required dependencies:
```bash
pip install mss pillow
```
If you are going to use LLM integration (e.g. OpenAI):
```bash
pip install openai
```
3. (Optional) Create a Python virtual environment to isolate dependencies.

## Configuration
- For LLM integration, set your API key in a `.env` file or directly in the code (recommended to use environment variables for security).
- Example of environment variable:
```env
OPENAI_API_KEY=your-key-here
```

## Basic Usage
1. Run the main file:
```bash
python main.py
```
2. Use the mouse to select the desired area of ​​the screen.
3. View the capture and use the available options.

## Dependencies
- Python 3.7+
- [mss](https://pypi.org/project/mss/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (already included in most Python installations)
- (Optional) openai

## Security Best Practices
- **Never share your API key publicly.**
- Use `.env` files and add them to `.gitignore`.
- Review access permissions to the screen and sensitive data.

## License
This project is distributed under the MIT license.
