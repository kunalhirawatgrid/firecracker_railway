import React, { useState } from 'react'
import Editor from '@monaco-editor/react'
import './CodeEditor.css'

const CodeEditor = ({ code, language, onChange, onLanguageChange }) => {
  const [editorTheme, setEditorTheme] = useState('vs-dark')

  const languageMap = {
    python: 'python',
    java: 'java',
    cpp: 'cpp',
    javascript: 'javascript',
  }

  const defaultCode = {
    python: `def solution():
    # Write your code here
    pass

# Test your solution
if __name__ == "__main__":
    result = solution()
    print(result)
`,
    java: `public class Solution {
    public static void main(String[] args) {
        // Write your code here
    }
}
`,
    cpp: `#include <iostream>
using namespace std;

int main() {
    // Write your code here
    return 0;
}
`,
    javascript: `function solution() {
    // Write your code here
}

// Test your solution
console.log(solution());
`,
  }

  const handleEditorChange = (value) => {
    if (onChange) {
      onChange(value || '')
    }
  }

  return (
    <div className="code-editor-container">
      <div className="code-editor-header">
        <select
          value={language}
          onChange={(e) => onLanguageChange && onLanguageChange(e.target.value)}
          className="language-selector"
        >
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
          <option value="javascript">JavaScript</option>
        </select>
        <button
          onClick={() => setEditorTheme(editorTheme === 'vs-dark' ? 'vs' : 'vs-dark')}
          className="theme-toggle"
        >
          {editorTheme === 'vs-dark' ? '☀️' : '🌙'}
        </button>
      </div>
      <div className="editor-wrapper">
        <Editor
          height="500px"
          language={languageMap[language] || 'python'}
          value={code || defaultCode[language] || ''}
          onChange={handleEditorChange}
          theme={editorTheme}
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            roundedSelection: false,
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            wordWrap: 'on',
          }}
        />
      </div>
    </div>
  )
}

export default CodeEditor

