# Nexlify Explorer

**Nexlify Explorer** is a terminal-based file explorer built with Python and the `curses` library. It features a dual-panel interface for navigating and viewing files and directories, with a vibrant, boxed UI and clear section separation. The application is designed to be intuitive, visually appealing, and modular, making it easy to use and extend.

## Features 
- **Dual-Panel Interface**: Navigate files in the left panel and view file/directory contents in the right panel.
- **Vibrant Boxed UI**: 
- Full-width header with white text on a blue background.
- Section titles in cyan (current directory) and magenta (selected file/folder content). 
- Metadata in green and help text in yellow for a lively look. 
- **Clear Section Separation**: Vertical separator and boxed elements for distinct panels.
- **Navigation**: 
- Switch panels with `Tab`.
- Scroll panels independently with arrow keys (`↑`/`↓`).
- Open directories with `Enter`.
- Go up a directory with `u`.
- **Search**: Filter files with `/` to enter a search term.
- **Metadata Display**: View file modification time and size in a boxed panel.
- **Modular Codebase**: Organized into `core` (logic) and `ui` (rendering) modules for maintainability.

## Installation

### Prerequisites 
- Python 3.6 or higher
- A terminal that supports `curses` (Linux/macOS recommended; Windows may require WSL)
- No external dependencies required (uses standard library `curses`, `os`, `time`)
### Steps
1. Clone or download the repository: 
```bash 
    git clone cd melas_explorer 
``` 
2. (Optional) Create and activate a virtual environment:
```bash
    python3 -m venv .venv source .venv/bin/activate 
``` 
3. Ensure the directory structure is correct: 
``` 
    melas_explorer/ 
    ├── main.py 
    ├── core/ 
        │ ├── __init__.py 
        │ ├── interface.py 
        │ ├── navigation.py 
        │ ├── file_utils.py 
    ├── ui/ 
        │ ├── __init__.py 
        │ ├── draw.py 
        │ ├── components.py 
``` 

## Usage

1. Navigate to the project directory: 
```bash 
cd melas_explorer 
```
2. Run the application:
```bash
python3 main.py 
```
3. Use the following key bindings: 
- `↑`/`↓`: Navigate files in the left panel or scroll the right panel.
- `Tab`: Switch between left and right panels.
- `Enter`: Open a selected directory.
- `/`: Search files by name. 
- `u`: Go up to the parent directory. 
- `q`: Quit the application. 

## Directory Structure 
- `main.py`: Entry point for the application.
- `core/`: Core logic modules. 
- `interface.py`: Main loop and search functionality.
- `navigation.py`: Panel navigation logic. 
- `file_utils.py`: File system operations.
- `ui/`: UI rendering modules. 
- `draw.py`: Interface rendering with boxed elements. 
- `components.py`: Reusable UI components (e.g., boxes). 

## Call for Contributors 
We welcome contributions to enhance **Nexlify Explorer**! If you’re interested in adding new features or improving the codebase, please consider the following ideas: 
- **File Previews**: Add support for previewing specific file types (e.g., images, PDFs, code snippets) in the right panel. 
- **File Operations**: Implement copy, move, and delete functionality with confirmation prompts. 
- **Customizable Themes**: Allow users to define custom color schemes for the UI (e.g., via a configuration file). 
- **Bookmarks**: Enable saving and quick access to frequently visited directories. 
- **Advanced Search**: Support regex or fuzzy search for more powerful file filtering. To contribute: 
1. Fork the repository. 
2. Create a feature branch (`git checkout -b feature/new-feature`). 
3. Commit your changes (`git commit -m 'Add new feature'`). 
4. Push to the branch (`git push origin feature/new-feature`). 
5. Open a pull request with a clear description of your changes. Please ensure your code follows the project’s modular structure and includes appropriate comments. 
## License 
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.