// Fetch and display today's report and news
async function fetchText(path) {
  const res = await fetch(path);
  if (!res.ok) return '';
  return await res.text();
}

async function fetchJSON(path) {
  const res = await fetch(path);
  if (!res.ok) return [];
  return await res.json();
}

async function renderReport() {
  // Try to load today's report
  const today = new Date().toISOString().slice(0, 10);
  const reportPath = `../reports/${today}.md`;
  const report = await fetchText(reportPath);
  document.getElementById('report').textContent = report || 'No report found.';
}

async function renderNews() {
  const news = await fetchJSON('../data/news.json');
  const list = document.getElementById('news-list');
  if (!news.length) {
    list.innerHTML = '<li>No news found.</li>';
    return;
  }
  list.innerHTML = '';
  news.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span class="source">${item.source}</span>: 
      <span class="title">${item.title}</span><br>
      <span class="summary">${item.summary}</span><br>
      <a class="link" href="${item.link}" target="_blank">Read more</a>
    `;
    list.appendChild(li);
  });
}

renderReport();
renderNews();
