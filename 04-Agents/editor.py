from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
import requests
import os
import subprocess


class Editor():

    def __init__(self):
                
        load_dotenv()

        self.client = OpenAI() 
        self.project_path = './Ai-Projects'  # To store the current project directory

        self.SYSTEM_PROMPT = """You are a code generation assistant tasked with creating complete, GitHub-ready starter projects for software developers.

        Communication Skill:
        Please maintain good communication with users. Greet them well and always be polite with user request.

        Your responsibilities:
        - Create a new project folder in my system as per user enter the project name
        - Generate production-quality, fully scaffolded codebases in response to user inputs.
        - Ensure each project has a proper file structure, clear naming conventions, and is ready to run or deploy.
        - Use best practices for the selected programming language or framework.
        - Edit files in my system as per user request.

        When generating a project, ALWAYS follow this checklist:
        1. Prompt the user for:
        - `project_name`: the desired name of the project.
        - `language_or_framework`: the main language or tech stack (e.g., Python, React, Next.js, Node.js, Django, Laravel).
        - `theme`: either "dark" or "light" for applicable frontend/UI projects.
        -  `github repo`: a valid github repo to commit and push the code.

        2. Create a clean, organized file/folder structure:
        - Include essential files: `README.md`, `.gitignore`, license (MIT by default), `package.json` or equivalent.
        - Add any required config files (`.env.example`, `vite.config.js`, `tailwind.config.js`, etc.).

        3. For frontend/UI projects:
        - Implement a basic theme switcher or pre-set styling according to "dark" or "light" mode.
        - Use Tailwind CSS, CSS Modules, or framework defaults unless specified otherwise.

        4. For backend/API projects:
        - Scaffold the project with RESTful or GraphQL routes if appropriate.
        - Include basic environment config and a health-check endpoint.

        5. Ensure code is:
        - Well-commented and easy to understand.
        - Free of errors and unnecessary boilerplate.
        - Compatible with `git init` and ready for GitHub commit.

        6. Generate a helpful `README.md` that includes:
        - Project description.
        - Setup instructions.
        - Technologies used.
        - How to run or deploy the project.

        Response user with a brief summary of steps completed after each query.

        Never assume technology preferences unless specified. Ask clarifying questions if the input is incomplete.

        Be consistent, efficient, and developer-friendly.

        If user enter anthing other than programming project, reply, I'm sorry, I am not authorized to do this task. I am here to help you for your programming projects.

        
        

        """
        self.messages = [
         { "role": "system", "content": self.SYSTEM_PROMPT }
            ]

 
    def chat(self, query):
        self.messages.append({"role": "user", "content": query})
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.messages
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        
        # Check if the response contains file content to write
        if "FILE_CONTENT:" in reply:
            self._handle_file_creation(reply)
        
        return reply

    def _handle_file_creation(self, reply):
        """Parse the AI response and create files accordingly"""
        try:
            # Extract file information from the response
            parts = reply.split("FILE_CONTENT:")
            file_info = json.loads(parts[1].strip())
            
            # Ensure project directory exists
            if not self.project_path:
                self.project_path = os.path.join(os.getcwd(), file_info.get("project_name", "new_project"))
                os.makedirs(self.project_path, exist_ok=True)
            
            # Create each file
            for file_path, content in file_info["files"].items():
                full_path = os.path.join(self.project_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                with open(full_path, 'w') as f:
                    f.write(content)
            
            # Initialize git repo if requested
            if file_info.get("init_git", False):
                self._init_git_repo()
                
            return f"Successfully created project at {self.project_path}"
        except Exception as e:
            return f"Error creating files: {str(e)}"

    def _init_git_repo(self, github_url):
        """Initialize git repository and make initial commit"""
        try:
            subprocess.run(["git", "init"], cwd=self.project_path, check=True)
            subprocess.run(["git", "add", "."], cwd=self.project_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=self.project_path, check=True)
            
            if "github_repo" in self.messages[-1]["content"]:
                 
                if github_url:
                    subprocess.run(["git", "remote", "add", "origin", github_url], cwd=self.project_path, check=True)
                    subprocess.run(["git", "push", "-u", "origin", "master"], cwd=self.project_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}")

 

    def get_github_url(self):
        # First try direct parsing
        for msg in reversed(self.messages):
            if msg["role"] == "user" and "github.com" in msg["content"]:
                # Use regex for more reliable extraction
                import re
                match = re.search(r'https?://github\.com/[^\s]+', msg["content"])
                if match:
                    return match.group(0)
        
        # Fall back to AI extraction if needed
        return self._ask_ai_for_github_url()

    def _ask_ai_for_github_url(self):
        prompt = """Review this conversation and return JUST the GitHub repository URL if one was mentioned, 
                    or 'false' if none was found. No commentary, just the URL or false."""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}] + self.messages[-3:],  # Last 3 messages for context
            temperature=0
        )
        
        result = response.choices[0].message.content.strip()
        return result if result.startswith(('http', 'git@')) else False