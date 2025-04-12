import { useState, useEffect } from 'react';
import nyom from './assets/nyom.png'; 
import './App.css';
import { login, logout, register, checkSession, getMessages, sendMessage, uploadProfilePicture, deleteMessage} from './api.js';
import { generateText } from "ai"
import { groq } from "./ai_slop.js";


function Header({ setPage, isAuthenticated }) {
  async function handleLogout() {
    const response = await logout();
    if (response.error) {
      alert("Logout failed: " + response.error);
      return;
    }
    alert("Logout successful!");
    setPage('login');
    // window.location.reload();
  }

  return (
    <div className="title_bar">
      <div className="title_bar">
        <h1 className="title">WEBCHAT</h1>
        <nav>
          <button className="title_text" onClick={() => setPage('chat')}>CHAT</button>
          <button className="title_text" onClick={() => setPage('about')}>ABOUT</button>
          {isAuthenticated ? <button className="title_text" onClick={() => setPage('aiSlop')}>AI SLOP</button> : null}
        </nav>
      </div>
      <div className="title_bar_right">
        <nav>
          {isAuthenticated ? <button className="title_text" onClick={handleLogout}>LOGOUT</button> : <button className="title_text" onClick={() => setPage('login')}>LOGIN</button>}
          {isAuthenticated ? <button className="title_text" onClick={() => setPage('profile')}>PROFILE</button> : null}
        </nav>
      </div>
    </div>
  );
}

function MessageBlock({author, content, profile_picture_url, messageId, onDelete, username}){
  return  (
    <div className="panel">
      <div className='message_block'>
        <div className="user secondary_panel">
          <img src={profile_picture_url} alt="Profile" width={64} height={64}/>
          {author}
        </div>
        <div className="message">
          <div className="message_content">
            <p className="message_text">{content}</p>
          </div>
        </div>
        {author === username && (
            <button id="delete_button" onClick={() => onDelete(messageId)}>
              Delete
            </button>
          )}
      </div>
    </div>
  )
}

function Chat({isAuthenticated, username}) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [reload, setReload] = useState(false);

  useEffect(() => {
    async function fetchMessages() {
      const response = await getMessages();
      if (response.error) {
        alert("Failed to fetch messages: " + response.error);
        return;
      }
      setMessages(response);
    }
    fetchMessages();
  }, [reload]);

  async function handleSendMessage() {
    if (input.trim()) {
      const response = await sendMessage(input);
      if (response.error) {
        alert("Message sending failed: " + response.error);
        return;
      }
      setInput('');
      setReload(!reload);
    }
  }

  async function handleDeleteMessage(messageId) {

    const response = await deleteMessage(messageId);
    if (response.error) {
      alert("Failed to delete message: " + response.error);
      return;
    }
    setReload(!reload);
  }

  return (
    <div className="center">
      <div className="contents">
        {isAuthenticated ? (
          <>
            <div className="messages">
              {messages.map((msg, index) => (
                <MessageBlock 
                  key={index}
                  author={msg.author} 
                  content={msg.content} 
                  profile_picture_url={msg.profile_picture} 
                  messageId={msg.id}
                  username={username}
                  onDelete={handleDeleteMessage} 
                />
              ))}
            </div>
            <div className='panel no_bob' id="input_panel">
              <div id="input">
                <input 
                  className="input_text"
                  type="text" 
                  value={input} 
                  onChange={(e) => setInput(e.target.value)} 
                  placeholder="Type a message..." 
                />
                <button onClick={handleSendMessage} className='input_button'>Send</button>
              </div>
            </div>
          </>
        ) : <p>Please login.</p>}
      </div>
    </div>
  );
}

function About() {
  return (
    <div className="center">
      <div className="contents">
        <div className="panel" id="about">
          <div className="secondary_panel">
            <img src={ nyom } alt="Photo" />
            <p className="about_text">NTU CSIE 林靖昀</p>
          </div>
          <div>
            <h2 className="about_text">Hi!</h2>
            <p className="about_text">I am a sophomore student from NTU CSIE.</p>
            <p className="about_text">:3 is my icon, :3</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Profile() {
  const [selectedFile, setSelectedFile] = useState(null);
  
  async function handleFileChange(event) {
    setSelectedFile(event.target.files[0]);
  }

  async function handleUpload() {
    if (!selectedFile) {
      alert("Please select a file to upload.");
      return;
    }

    const response = await uploadProfilePicture(selectedFile);
    if (response.error) {
      alert("Failed to upload profile picture: " + response.error);
      return;
    }

    alert("Profile picture changed successfully!");
    setSelectedFile(null);
  }

  return (
    <div className='center'>
      <div className="contents">
        <div className="panel" id="profile">
          <h2 className="about_text" id="profile_title">Profile</h2>
          <div className="secondary_panel" id="profile_settings">
            <p className="about_text">Profile Picture: </p>
            <form>
              <input
                type="file"
                id="myFile"
                name="filename"
                onChange={handleFileChange} // Handle file selection
              />
              <button type="button" onClick={handleUpload}>Upload</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

function Login({ setPage }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin() {
      const response = await login(username, password);
      if (response.error) {
          alert("Login failed: " + response.error);
          return;
      }
      alert("Login successful!");
      window.location.reload();
  }
  async function handleRegister() {
      const response = await register(username, password);
      if (response.error) {
          alert("Registration failed: " + response.error);
          return;
      }
      alert("Registration successful!");
      window.location.reload();
      setPage('login');
  }

  return (
      <div className='center'>
        <div className="contents">
          <div className="panel" id="login">
            <div className='secondary_panel' id="login_settings">
                Username:
                <input className="input_text" id="login_text" placeholder="Username" onChange={e => setUsername(e.target.value)} />
                Password:
                <input className="input_text" id="login_text" type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
            </div>
            <button id="login_button" onClick={handleLogin}>Login</button>
            <button id="register_button" onClick={handleRegister}>Register</button>
          </div>
        </div>
      </div>
  );
}


function AISlop() {
  const [aiText, setAiText] = useState("");

  async function handleAiTextChange(event) {
    const { text } = await generateText({
      model: groq('llama-3.1-8b-instant'),
      prompt: "Give me AI Slop, like bombardino crocodilo, be extremely creative, less than 10 words.",
    })
    setAiText(text);
  }
  return (
    <div className="center">
      <div className="contents">
        <div className="panel" id="ai_slop">
          <div className='about_text'>
            <h2>✨AI Slop✨</h2>
            <p className='secondary_panel' id="ai_text">{aiText}</p>
          </div>
          <button className="delete_button" onClick={handleAiTextChange}>Generate AI Slop</button>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [page, setPage] = useState('chat');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");
  
  {page === 'chat' ? (
        <Chat isAuthenticated={isAuthenticated} />
      ) : page === 'about' ? (
        <About />
      ) : page === 'login' ? (
        <Login setPage={setPage} />
      ) : (
        <Profile />
      )}
  useEffect(() => {
    async function session() {
      const response = await checkSession();

      if(!response.error){
        setIsAuthenticated(true); 
        setUsername(response.username);
      }
    }
    session();
  }, []);


  return (
    <>
      <Header setPage={setPage} isAuthenticated={isAuthenticated} />
      {page === 'chat' ? (
        <Chat isAuthenticated={isAuthenticated} username={username} />
      ) : page === 'about' ? (
        <About />
      ) : page === 'login' ? (
        <Login setPage={setPage} />
      ) : page === 'profile' ? (
        <Profile />
      ) : (
        <AISlop />
      )}
    </>
  );
}

export default App;
