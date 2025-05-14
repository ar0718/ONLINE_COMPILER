
import './styles/Ide.css'
import CDNEditor from './CDNEditor'
import {React, useState, useEffect} from 'react'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faPlay} from '@fortawesome/free-solid-svg-icons'

const languageModes = {
  python: 'python',
  cpp: 'text/x-c++src',
  java: 'text/x-java',
};

const defaultCode = {
  python: '# Python code\nprint("Hello, world!")',
  cpp: '// C++ code\n#include <iostream>\nint main() { std::cout << "Hello"; }',
  java: '// Java code\npublic class Main { public static void main(String[] args) { System.out.println("Hello"); } }',
};

const Ide = () => {
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState(defaultCode[language]);
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('~@Output:')

  useEffect(() => {
    window.addEventListener('click', (e) => {
      if (e.target.id === 'python-button') {
        document.getElementById('python-button').classList.add('active')
        setLanguage('python');
        setCode(defaultCode['python']);
        document.getElementById('c-button').classList.remove('active')
        document.getElementById('java-button').classList.remove('active')
      } else if (e.target.id === 'c-button') {
        document.getElementById('python-button').classList.remove('active')
        document.getElementById('c-button').classList.add('active')
        setLanguage('cpp');
        setCode(defaultCode['cpp']);
        document.getElementById('java-button').classList.remove('active')
      } else if (e.target.id === 'java-button') {
        document.getElementById('python-button').classList.remove('active')
        document.getElementById('c-button').classList.remove('active')
        document.getElementById('java-button').classList.add('active')
        setLanguage('java');
        setCode(defaultCode['java']);
      }
    })
  }, [])

  return (
    <div className="ide">
      <div className="header">
        <div id="python-button" className="python active">
          Python
        </div>
        <div id="c-button" className="c">
          C++
        </div>
        <div id="java-button" className="java">
          Java
        </div>
      </div>
      
      <div className="editor">
        <CDNEditor
          value={code}
          language={languageModes[language]}
          onChange={(updatedCode) => setCode(updatedCode)}
        /> 
      </div>
      <div className="terminal">
        <div className="inputbox">
          <textarea onChange={(e) => setInput(e.target.value)}></textarea>
        </div>
        <div className="outputbox">
          <textarea value={output} onChange={(e) => setOutput(e.target.value)} readOnly></textarea>
          <div className="panel">
            <div className="runner">
              <FontAwesomeIcon icon={faPlay} style={{color: 'var(--primary-text)', fontSize: '3rem', cursor: 'pointer'}} />
            </div>
            <div className="runtime">
              
            </div>  
            <div className="memory">
              
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Ide
