import './styles/Ide.css'

const Ide = () => {
  return (
    <div className="ide">
      <div className="header">
        <div className="python active">
          Python
        </div>
        <div className="cpp">
          C++
        </div>
        <div className="java">
          Java
        </div>
      </div>
      
      <div className="editor">
        
      </div>
      <div className="terminal">
        <div className="inputbox">
          <textarea></textarea>
        </div>
        <div className="outputbox">
          <textarea value="@output:" readonly></textarea>
          <div className="panel">
            <div className="runner">
            
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