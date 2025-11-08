import { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = ({ code, language, onChange, readOnly = false }) => {
  const [editorValue, setEditorValue] = useState(code || '');

  useEffect(() => {
    setEditorValue(code || '');
  }, [code]);

  const handleEditorChange = (value) => {
    setEditorValue(value);
    if (onChange) {
      onChange(value);
    }
  };

  const languageMap = {
    python: 'python',
    java: 'java',
    cpp: 'cpp',
    javascript: 'javascript',
  };

  return (
    <div className="code-editor-container">
      <Editor
        height="500px"
        language={languageMap[language] || 'python'}
        value={editorValue}
        onChange={handleEditorChange}
        theme="vs-dark"
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          roundedSelection: false,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          wordWrap: 'on',
        }}
      />
    </div>
  );
};

export default CodeEditor;

