# OVSGUI - Online Variable System GUI

**OVSGUI** is a graphical user interface (GUI) for managing online variables through Firebase. It provides an intuitive interface for users to interact with variables, retrieve, delete, and manage them. The application supports token-based access and displays variable details such as creator information, creation time, and more.

## Features

- **Token Authentication**: Secure access to the variable system using unique tokens.
- **Variable Management**: View and manage variables, including deletion of variables.
- **Real-time Updates**: Dynamic interaction with Firebase data.
- **User Interface**: Modern GUI built with `customtkinter` for a smooth user experience.
- **Variable Details**: View detailed information about each variable, including creator, IP, creation date, and value.

## Installation

To install **OVSGUI** and use it in your Python environment, follow the steps below.

### Using pip

You can install the package directly from PyPI:

```bash
pip install ovsgui
```

### Use

```bash
ovsgui
```

## Integration with ovsystem

**ovsgui** is designed to work seamlessly with the **ovsystem** library. **ovsystem** manages variables through Firebase, while **ovsgui** provides a graphical interface to visualize and manage these variables. Users can manage Firebase variables using **ovsystem**, and with **ovsgui**, they can easily view and modify these variables. 

This integration allows both libraries to be used together for more efficient system management.
