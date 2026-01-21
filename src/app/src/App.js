import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState("");

  const fetchTodos = async () => {
    const res = await fetch("http://localhost:8000/todos/");
    const data = await res.json();
    setTodos(Array.isArray(data) ? data : []);
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const submitTodo = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    await fetch("http://localhost:8000/todos/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    setText("");
    fetchTodos();
  };

  return (
    <div className="App">
      <h1>List of TODOs</h1>

      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>

      <h1>Create a TODO</h1>

      <form onSubmit={submitTodo}>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button>Add TODO</button>
      </form>
    </div>
  );
}

export default App;
