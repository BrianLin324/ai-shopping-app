import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("password123");
  const [token, setToken] = useState("");
  const [query, setQuery] = useState("things for cooking dinner at home");
  const [interests, setInterests] = useState("I like kitchen appliances, coffee, cooking, and home gadgets");
  const [products, setProducts] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [message, setMessage] = useState("");

  const authHeaders = { Authorization: `Bearer ${token}` };

  async function signup() {
    const res = await fetch(`${API}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.access_token) setToken(data.access_token);
    setMessage(data.message || data.detail || "Signup done");
  }

  async function login() {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.access_token) setToken(data.access_token);
    setMessage(data.detail || "Login done");
  }

  async function saveOnboarding() {
    const res = await fetch(`${API}/onboarding`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders },
      body: JSON.stringify({ interests }),
    });
    const data = await res.json();
    setMessage(data.message || data.detail);
  }

  async function loadProducts() {
    const res = await fetch(`${API}/products?page=1&limit=12`);
    const data = await res.json();
    setProducts(data);
  }

  async function search() {
    const res = await fetch(`${API}/search?q=${encodeURIComponent(query)}`, {
      headers: authHeaders,
    });
    const data = await res.json();
    setSearchResults(data);
  }

  async function buy(productId) {
    const res = await fetch(`${API}/purchase`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders },
      body: JSON.stringify({ product_id: productId }),
    });
    const data = await res.json();
    setMessage(data.message || data.detail);
  }

  async function loadRecommendations() {
    const res = await fetch(`${API}/recommendations`, {
      headers: authHeaders,
    });
    const data = await res.json();
    setRecommendations(data);
  }

  function ProductCard({ item }) {
    const product = item.product || item;

    return (
      <div className="card">
        {product.image_url && <img src={product.image_url} alt={product.name} />}
        <h3>{product.name}</h3>
        <p>{product.brand} — {product.category}</p>
        <p>${product.price}</p>
        {item.score && <p>Score: {item.score.toFixed(3)}</p>}
        <button onClick={() => buy(product.product_id)}>Buy</button>
      </div>
    );
  }

  return (
    <div className="app">
      <h1>AI Shopping App</h1>
      <p><strong>Status:</strong> {message}</p>

      <section>
        <h2>Account</h2>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button onClick={signup}>Sign Up</button>
        <button onClick={login}>Log In</button>
        <p>{token ? "Logged in ✅" : "Not logged in"}</p>
      </section>

      <section>
        <h2>Onboarding</h2>
        <textarea value={interests} onChange={(e) => setInterests(e.target.value)} />
        <button onClick={saveOnboarding}>Save Interests</button>
      </section>

      <section>
        <h2>Products</h2>
        <button onClick={loadProducts}>Load Products</button>
        <div className="grid">
          {products.map((p) => <ProductCard key={p.product_id} item={p} />)}
        </div>
      </section>

      <section>
        <h2>Semantic Search</h2>
        <input value={query} onChange={(e) => setQuery(e.target.value)} />
        <button onClick={search}>Search</button>
        <div className="grid">
          {searchResults.map((item) => <ProductCard key={item.product.product_id} item={item} />)}
        </div>
      </section>

      <section>
        <h2>For You</h2>
        <button onClick={loadRecommendations}>Load Recommendations</button>
        <div className="grid">
          {recommendations.map((item) => <ProductCard key={item.product.product_id} item={item} />)}
        </div>
      </section>
    </div>
  );
}

export default App;