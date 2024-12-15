# Ai-Notebook

A powerful, open-source tool to work with local large language models (LLMs) for document processing and analysis without an internet connection.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Supported Inputs](#supported-inputs)
  - [Available Outputs](#available-outputs)
  - [Advanced Options](#advanced-options)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Introduction

Ai Notebook is an open-source alternative to Google’s Notebook LM, designed to bring document analysis and processing capabilities to your local machine—no internet connection required. Inspired by the need for seamless offline access, this tool leverages local LLMs to support various document formats, from text files to web-based PDFs, making it a versatile solution for researchers, students, and professionals alike.

---

## Features

- **Offline Functionality**: Access your documents and run analyses without needing an internet connection, ensuring seamless usage in any environment.

- **Multiple Input Formats**: Supports a variety of input types, including:

  - Text files
  - Copied text
  - YouTube videos
  - Web articles
  - Web PDFs (a feature not currently available in Notebook LM)

- **Heuristic-based PDF Chunking**: Efficiently process large PDF documents by breaking them into manageable chunks, accommodating the context length limitations of local models.

- **Enhanced Response Quality**: Leverage multiple local LLMs to select the most accurate and relevant responses for user queries, improving overall output quality.

- **Predefined Document Outputs**: Generate structured outputs such as:

  - Timelines
  - Briefing documents
  - Study guides
  - Outlines
  - Tables of Contents (TOCs)
  - Frequently Asked Questions (FAQs)

- **Gemini Flash Integration**: Utilizes Gemini Flash for extended context capabilities, enhancing the quality of responses when an internet connection is available.

- **User-friendly Interface**: Designed for ease of use, allowing users to quickly navigate through the features and functionalities of the application.

---

## Installation

To set up **Ai Notebook**, follow these steps:

1. **Clone the Repository**: Start by cloning the project repository to your local machine:

   ```bash
   git clone https://github.com/Ritvik19/Ai-Notebook.git
   cd Ai-Notebook
   ```

2. **Install Ollama**: Ensure you have [Ollama](https://ollama.com/) installed on your machine. You can do this by following the installation instructions provided on their website.

3. **Create a Conda Virtual Environment**: It's recommended to create a virtual environment to manage dependencies. Use the following command:

   ```bash
   conda create --name ai_notebook python=3.9
   ```

4. **Activate the Virtual Environment**: Once the environment is created, activate it:

   ```bash
   conda activate ai_notebook
   ```

5. **Install Dependencies**: Install the required packages using the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Application**: Navigate to the `src` directory and run the Streamlit app:

   ```bash
   cd src
   streamlit run app.py
   ```

7. **Access the App**: Open your web browser and go to `http://localhost:8501` to access the Ai Notebook interface.

---

## Usage

Once the **Ai Notebook** application is running, you can start using its features to process and analyze your documents. Follow these guidelines for optimal use:

### Supported Inputs

**Ai Notebook** allows you to input various document formats, including:

- **Text Files**: Upload .txt or .md files containing plain text.
- **Spreadsheets**: Upload spreadsheets in any format for handling data tables and structured information.
- **Copied Text**: Paste text directly into the input field.
- **YouTube Videos**: Provide links to YouTube videos for analysis or summarization.
- **Web Articles**: Input URLs of web articles for retrieval and processing.
- **PDFs**: Upload PDFs from the web or your local system for enhanced document analysis.

### Example Use Cases

Here are a few scenarios where **Ai Notebook** can be particularly useful:

- **Academic Research**: Upload arXiv papers in PDF format for analysis and generate study guides or outlines based on the key findings, making it easier to prepare for presentations or discussions.
- **Content Creation**: Paste copied text from various sources or provide URLs of web articles to create briefing documents or FAQs, streamlining the content creation process for blogs or reports.

- **Video Summarization**: Input a YouTube video link to receive a concise summary of the video's key points, saving time and allowing you to focus on essential information.

- **Project Management**: Create timelines based on the events or milestones outlined in a document, helping visualize project progress and deadlines.

### Available Outputs

After processing your inputs, **Ai Notebook** generates structured outputs, including:

- **Timelines**: Visual representations of events or processes.
- **Briefing Documents**: Summaries of key information extracted from your inputs.
- **Study Guides**: Compiled notes and highlights for academic use.
- **Outlines**: Structured outlines based on the content provided.
- **Tables of Contents (TOCs)**: Organized listings of sections in a document.
- **Frequently Asked Questions (FAQs)**: Common questions and their answers related to the input content.
- **Interactive Queries**: Users can ask any question related to the selected chunk of text, allowing for in-depth exploration and understanding of the material.

### Advanced Options

**Ai Notebook** also offers advanced features for users looking to customize their experience:

- **Heuristic-based PDF Chunking**: Automatically breaks down large PDF documents into smaller, manageable chunks to ensure thorough analysis within the context limitations of local models.
- **Response Selection**: Choose the best response from multiple local LLMs to ensure the highest quality output.

---

## Technical Details

**Ai Notebook** is built to leverage the capabilities of local large language models (LLMs) while providing an intuitive interface for document processing. Below are the key technical aspects of the project:

### Technology Stack

- **Framework**: The application is built using [Streamlit](https://streamlit.io/), a powerful library for creating interactive web applications in Python, which allows for easy deployment and user interaction.

- **Local LLMs**: **Ai Notebook** utilizes [Ollama](https://ollama.com/) to run local large language models, enabling offline functionality and maintaining user control over data.

- **Gemini Flash API**: The application integrates the Gemini Flash API to enhance context length capabilities, providing improved quality and relevance of responses when an internet connection is available.

---

## Roadmap

The development of **Ai Notebook** is an ongoing process, and we have exciting plans for future enhancements. Below is a roadmap outlining key features and improvements to be implemented:

### Upcoming Features

- **Podcast Feature**: Implement a podcast feature that utilizes text-to-speech technology to generate audio summaries and discussions based on processed documents.
- **Multiple Document Support**: Add support for various document types, including Word documents, slides, to enable comprehensive document processing across multiple formats.
- **Vision Based Chunking of Documents**: Implement an image-based document chunking system to break down the document more effectively based on visual cues. 
- **Enhanced Query Functionality**: Improve the interactive querying system to support more complex queries and provide contextual answers based on user inputs.
- **Multimodal Support**: Introduce support for images and videos, enabling users to process and analyze multimedia content alongside text documents.
- **Twitter Thread Input**: Enable users to input Twitter threads directly, allowing the application to analyze and summarize Twitter-based content alongside other document types.
- **Pinned Notes as Sources**: Allow users to use the pinned notes as sources for generating outputs, enhancing the customization and relevance of the generated content.

### Long-term Goals

- **Transition to FastAPI**: Move away from Streamlit and adopt FastAPI for improved performance and flexibility in building the application.
- **Edit Query**: Allow users to edit queries and responses generated by the local LLMs, enhancing user control and customization of outputs.
- **Custom Functionality Creation**: Enable users to create custom functionality on the go, allowing for a more tailored experience based on individual needs.

---

## Contributing

Contributions to **Ai Notebook** are welcome and encouraged! Here’s how you can get involved:

### How to Contribute

1. **Fork the Repository**: Start by forking the repository to your own GitHub account.

2. **Clone Your Fork**: Clone your forked repository to your local machine:

   ```bash
   git clone <your-fork-url>
   cd <repository-folder>
   ```

3. **Create a Branch**: Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**: Implement your changes or enhancements.

5. **Commit Your Changes**: Commit your changes with a clear and descriptive message:

   ```bash
   git commit -m "Add feature: your feature description"
   ```

6. **Push to Your Fork**: Push your changes to your forked repository:

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**: Go to the original repository and open a pull request. Provide a clear description of your changes and the reason for the contribution.

### Guidelines

- **Code Quality**: Ensure that your code adheres to the project's coding standards and is well-documented.
- **Issue Tracking**: If you encounter bugs or have suggestions for new features, please open an issue in the GitHub repository.

- **Respectful Communication**: Maintain a positive and respectful tone when communicating with other contributors and users.

### Acknowledgments

Contributors will be acknowledged in the project documentation. Your contributions help improve the **Ai Notebook** experience for everyone!

---

## Acknowledgements

**Ai Notebook** would not be possible without the support and contributions from the following individuals and resources:

- **Ollama**: For providing the local LLM infrastructure that powers the application's capabilities.

- **Streamlit**: For creating an accessible and user-friendly framework that allows for the rapid development of interactive applications.

- **Gemini Flash**: For enhancing the application's context length capabilities, contributing to higher-quality responses.

- **Notebook LM**: For serving as a foundational inspiration for the development of **Ai Notebook** and providing a reference for key features.

Your support and collaboration are invaluable in advancing the goals of **Ai Notebook**!
