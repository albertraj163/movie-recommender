const userSelect = document.getElementById("userSelect");
const recommendBtn = document.getElementById("recommendBtn");
const historyList = document.getElementById("historyList");
const recList = document.getElementById("recList");
const historySub = document.getElementById("historySub");
const recSub = document.getElementById("recSub");

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || "Request failed");
  }
  return res.json();
}

function showLoading(container) {
  container.className = "movie-list loading";
  container.innerHTML = '<div class="spinner"></div><span>Loading...</span>';
}

function renderHistory(ratings) {
  if (!ratings.length) {
    historyList.className = "movie-list empty-state";
    historyList.innerHTML = "<p>No ratings found for this user.</p>";
    return;
  }

  historyList.className = "movie-list";
  historyList.innerHTML = ratings
    .map(
      (m) => `
    <div class="movie-card">
      <div class="movie-info">
        <h4>${m.title}</h4>
        <div class="movie-meta">${m.genre} · ${m.year}</div>
      </div>
      <span class="rating-badge user">★ ${m.rating.toFixed(1)}</span>
    </div>`
    )
    .join("");
}

function renderRecommendations(recs) {
  if (!recs.length) {
    recList.className = "movie-list empty-state";
    recList.innerHTML = "<p>No new recommendations available.</p>";
    return;
  }

  recList.className = "movie-list";
  recList.innerHTML = recs
    .map(
      (m, i) => `
    <div class="movie-card rec">
      <span class="rank">${i + 1}</span>
      <div class="movie-info">
        <h4>${m.title}</h4>
        <div class="movie-meta">${m.genre} · ${m.year}</div>
      </div>
      <span class="rating-badge predicted">${m.predicted_rating.toFixed(1)}</span>
    </div>`
    )
    .join("");
}

async function loadStats() {
  const stats = await fetchJSON("/api/stats");
  document.getElementById("statUsers").textContent = stats.total_users;
  document.getElementById("statMovies").textContent = stats.total_movies;
  document.getElementById("statRatings").textContent = stats.total_ratings;
  document.getElementById("statAvg").textContent = stats.avg_rating;
}

async function loadUsers() {
  const users = await fetchJSON("/api/users");
  userSelect.innerHTML = users
    .map(
      (u) =>
        `<option value="${u.id}">User ${u.id} — ${u.rating_count} ratings (avg ${u.avg_rating})</option>`
    )
    .join("");
}

async function loadUserHistory(userId) {
  showLoading(historyList);
  historySub.textContent = `User ${userId}`;
  const ratings = await fetchJSON(`/api/users/${userId}/ratings`);
  renderHistory(ratings);
}

async function loadRecommendations(userId) {
  showLoading(recList);
  recommendBtn.disabled = true;
  recSub.textContent = `Top picks for User ${userId}`;
  try {
    const data = await fetchJSON(`/api/recommend/${userId}?top_n=5`);
    renderRecommendations(data.recommendations);
  } finally {
    recommendBtn.disabled = false;
  }
}

userSelect.addEventListener("change", () => {
  loadUserHistory(userSelect.value);
});

recommendBtn.addEventListener("click", () => {
  loadRecommendations(userSelect.value);
});

async function init() {
  await loadStats();
  await loadUsers();
  if (userSelect.options.length) {
    await loadUserHistory(userSelect.value);
    await loadRecommendations(userSelect.value);
  }
}

init().catch((err) => {
  console.error(err);
  historyList.innerHTML = `<p>Error: ${err.message}</p>`;
});
