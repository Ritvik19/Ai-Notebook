import glob
import json
import os

RAG = """
**Task:** Answer questions based on a given context.

**Additional Details:**
- The context will be provided as a string.
- Questions will be in natural language and require reasoning before providing an answer.
- Answers should be formatted using markdown with appropriate headings, bullet points, tables, etc., as required by the question.

# Steps

1. **Understand the Context:** Read and comprehend the given context to extract relevant information.
2. **Analyze the Question:** Break down the question into smaller parts if necessary. Identify what specific information is being asked for.
3. **Reason and Infer:** Use logical reasoning and inference based on the context to derive the answer.
4. **Format the Answer:** Structure the answer using markdown formatting, including headings, bullet points, tables, etc., as appropriate.

# Output Format

The output should be in markdown format with a clear heading for the question asked. The answer should be structured appropriately using bullet points, tables, or other markdown elements as necessary. For example:

# Notes
- Always ensure that the answer is based on the given context. If the question cannot be answered from the provided context, clearly state "Cannot be determined from the given context."
- Use tables sparingly and only when necessary to present complex data in a structured format.

{context}

---

Question: {query}
""".strip()

PAPER_SUMMARY_PROMPT = """
Summarize the key points of a machine learning research paper based on its abstract, capturing the main contributions, methods, and any unique aspects or findings. Your summary should be concise yet comprehensive, aiming to convey the essence of the paper without delving into excessive technical detail. Emphasize the core research problem, proposed solutions, and the implications or results of the study.

# Steps

1. **Read and Analyze**: Review the abstract to identify the main objectives, methods, findings, and significance of the research.
2. **Extract Key Elements**:
   - **Problem Statement**: Describe the core problem or research question the paper addresses.
   - **Methods**: Summarize the approach or techniques used to address the problem.
   - **Results**: Highlight the findings or outcomes of the research.
   - **Significance**: Note any unique contributions or implications of the research.
3. **Formulate Summary**: Combine these elements into a well-structured summary. Keep language accessible and avoid unnecessary technical jargon.

# Output

Provide a concise paragraph summary of the abstract. The summary should be 3-5 sentences, focusing on the main goals, methods, and findings of the paper. 

# Output Format
Do not include any bullet points, headings or any other surrounding text in the summary. Just provide the summary in a paragraph.
"""

instructions = json.load(open("./prompts/instructions.json"))

PROMPT_DICT = {
    os.path.splitext(os.path.basename(file))[0]: {
        "prompt": open(file).read(),
        "instruction": instructions[os.path.splitext(os.path.basename(file))[0]],
    }
    for file in glob.glob("./prompts/*.md")
}