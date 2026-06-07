import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("password123");
  const [token, setToken] = useState("");

  const [query, setQuery] = useState("things for cooking dinner at home");
  const [interests, setInterests] = useState(
    "I like kitchen appliances, coffee, cooking, and home gadgets"
  );

  const [products, setProducts] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [message, setMessage] = useState("Ready");

  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};

  async function signup() {
    const res = await fetch(`${API}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(data.detail || "Signup failed. Try logging in.");
      return;
    }

    setToken(data.access_token);
    setMessage("Signup successful. You are logged in.");
  }

  async function login() {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(data.detail || "Login failed.");
      return;
    }

    setToken(data.access_token);
    setMessage("Login successful. You are logged in.");
  }

  async function saveOnboarding() {
    if (!token) {
      setMessage("Please sign up or log in before saving interests.");
      return;
    }

    const res = await fetch(`${API}/onboarding`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders },
      body: JSON.stringify({ interests }),
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(data.detail || "Onboarding failed.");
      return;
    }

    setMessage("Interests saved. Recommendations are now personalized.");
  }

  async function loadProducts() {
    const res = await fetch(`${API}/products?page=1&limit=12`);
    const data = await res.json();

    setProducts(Array.isArray(data) ? data : []);
    setMessage("Products loaded.");
  }

  async function search() {
    if (!token) {
      setMessage("Please sign up or log in before searching.");
      return;
    }

    const res = await fetch(
      `${API}/search?q=${encodeURIComponent(query)}&limit=10`,
      { headers: authHeaders }
    );

    const data = await res.json();

    if (!res.ok || !Array.isArray(data)) {
      setSearchResults([]);
      setMessage(data.detail || "Search failed.");
      return;
    }

    setSearchResults(data);
    setMessage("Search complete.");
  }

  async function loadRecommendations() {
    if (!token) {
      setMessage("Please sign up or log in before loading recommendations.");
      return;
    }

    const res = await fetch(`${API}/recommendations?limit=10`, {
      headers: authHeaders,
    });

    const data = await res.json();

    if (!res.ok || !Array.isArray(data)) {
      setRecommendations([]);
      setMessage(data.detail || "Recommendations failed.");
      return;
    }

    setRecommendations(data);
    setMessage("Recommendations loaded.");
  }

  async function buy(productId) {
    if (!token) {
      setMessage("Please sign up or log in before buying.");
      return;
    }

    const res = await fetch(`${API}/purchase`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders },
      body: JSON.stringify({ product_id: productId }),
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(data.detail || "Purchase failed.");
      return;
    }

    setMessage("Purchase recorded.");
  }

  function ProductCard({ item }) {
    const product = item.product || item;
    if (!product) return null;

    return (
      <article className="product-card">
        <div className="image-box">
          {product.image_url ? (
            <img src={product.image_url} alt={product.name} />
          ) : (
            <div className="placeholder">No Image</div>
          )}
        </div>

        <div className="product-body">
          <p className="category">{product.category || "General"}</p>
          <h3>{product.name}</h3>
          <p className="brand">{product.brand || "Unknown brand"}</p>

          {typeof item.score === "number" && (
            <span className="score">AI Match {item.score.toFixed(2)}</span>
          )}

          <div className="card-footer">
            <strong>${product.price}</strong>
            <button onClick={() => buy(product.product_id)}>Buy</button>
          </div>
        </div>
      </article>
    );
  }

  return (
    <div className="app">
      <header className="hero">
        <nav>
          <div className="logo">AI Shop</div>
          <div className="login-status">{token ? "Logged in ✅" : "Guest mode"}</div>
        </nav>

        <div className="hero-content">
          <span className="pill">Semantic Search + Personalization</span>
          <h1>Find the right product with AI.</h1>
          <p>
            Search naturally, discover relevant products, and get recommendations
            that adapt to your behavior.
          </p>

          <div className="hero-search">
            <input value={query} onChange={(e) => setQuery(e.target.value)} />
            <button onClick={search}>Search</button>
          </div>

          <p className="status">{message}</p>
        </div>
      </header>

      <section className="panel account-panel">
        <div>
          <h2>Account</h2>
          <p>Create an account or log in to enable personalized AI results.</p>
        </div>

        <div className="account-form">
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={signup}>Sign Up</button>
          <button className="secondary" onClick={login}>
            Log In
          </button>
        </div>
      </section>

      <section className="panel">
        <div className="section-header">
          <div>
            <h2>Search Results</h2>
            <p>Ranked by semantic similarity, not simple keyword matching.</p>
          </div>
        </div>

        <div className="grid">
          {searchResults.map((item) => (
            <ProductCard key={item.product.product_id} item={item} />
          ))}
        </div>
      </section>

      <section className="panel onboarding-panel">
        <div>
          <h2>Personalization Setup</h2>
          <p>Tell the app what you like so recommendations start smarter.</p>
        </div>

        <textarea
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
        />

        <button onClick={saveOnboarding}>Save Interests</button>
      </section>

      <section className="panel">
        <div className="section-header">
          <div>
            <h2>Recommended For You</h2>
            <p>Generated from onboarding, searches, views, and purchases.</p>
          </div>
          <button onClick={loadRecommendations}>Load Recommendations</button>
        </div>

        <div className="grid">
          {recommendations.map((item) => (
            <ProductCard key={item.product.product_id} item={item} />
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="section-header">
          <div>
            <h2>Browse Products</h2>
            <p>Explore products from the full catalog.</p>
          </div>
          <button onClick={loadProducts}>Load Products</button>
        </div>

        <div className="grid">
          {products.map((p) => (
            <ProductCard key={p.product_id} item={p} />
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;