document.addEventListener('DOMContentLoaded', () => {

    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const movieResults = document.getElementById('movieResults');

    let selectedProvider = "";
    let selectedGenre = "";

    /* =========================
       経由のワード検索 
    ========================= */

    async function searchWordTMDB(query, type) {
        const url = `/api/tmdb/search/?query=${encodeURIComponent(query)}&type=${type}`;

        const res = await fetch(url);
        const data = await res.json();
        return { type, results: data.results || [] };
    }

    /* =========================
       🔍 ワード検索
    ========================= */

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = searchInput.value.trim();
        if (!query) return;

        resetFilterState();
        searchByWord(query);
    });

    async function searchByWord(query) {
        movieResults.innerHTML = '<p>検索中…</p>';

        try {
            const [movies, tvs, people] = await Promise.all([
                searchWordTMDB(query, 'movie'),
                searchWordTMDB(query, 'tv'),
                searchWordTMDB(query, 'person')
            ]);

            displayAllResults(movies, tvs, people);
        } catch {
            movieResults.innerHTML = '<p>検索エラー</p>';
        }
    }

    /* =========================
       🎛 絞り込みトグル
    ========================= */

    setupToggleButtons('.provider-btn', 'provider');
    setupToggleButtons('.genre-btn', 'genre');

    function setupToggleButtons(selector, type) {
        document.querySelectorAll(selector).forEach(btn => {
            btn.addEventListener('click', () => {
                const value = btn.dataset[type];
                const isSame =
                    (type === 'provider' && selectedProvider === value) ||
                    (type === 'genre' && selectedGenre === value);

                clearActive(selector);

                if (isSame) {
                    if (type === 'provider') selectedProvider = "";
                    if (type === 'genre') selectedGenre = "";
                } else {
                    btn.classList.add('active');
                    if (type === 'provider') selectedProvider = value;
                    if (type === 'genre') selectedGenre = value;
                }

                searchByFilter();
            });
        });
    }

    function clearActive(selector) {
        document.querySelectorAll(selector)
            .forEach(btn => btn.classList.remove('active'));
    }

    function resetFilterState() {
        selectedProvider = "";
        selectedGenre = "";
        clearActive('.provider-btn');
        clearActive('.genre-btn');
    }

    /* =========================
       🔎 絞り込み検索（Django 経由）
    ========================= */

    async function searchByFilter() {
        if (!selectedProvider && !selectedGenre) {
            movieResults.innerHTML = '';
            return;
        }

        movieResults.innerHTML = '<p>絞り込み中…</p>';

        try {
            const [movies, tvs] = await Promise.all([
                discoverTMDB('movie'),
                discoverTMDB('tv')
            ]);

            if (!movies.results.length && !tvs.results.length) {
                movieResults.innerHTML = '<p>条件に合う作品が見つかりません。</p>';
                return;
            }

            displayAllResults(movies, tvs, { type: 'person', results: [] });

        } catch {
            movieResults.innerHTML = '<p>絞り込みエラー</p>';
        }
    }


    /* =========================
       🛰 Django 経由の discover API
    ========================= */

    async function discoverTMDB(type) {
        const params = new URLSearchParams();
        params.append("type", type);

        if (selectedGenre) params.append("genre", selectedGenre);
        if (selectedProvider) params.append("provider", selectedProvider);

        const url = `/api/tmdb/discover/?${params.toString()}`;

        const res = await fetch(url);
        const data = await res.json();
        return { type, results: data.results || [] };
    }




    /* =========================
       📅 最新順ソート
    ========================= */

    function sortByDateDesc(results, type) {
        return results.sort((a, b) => {
            const dateA =
                type === 'movie' ? a.release_date :
                    type === 'tv' ? a.first_air_date :
                        '';
            const dateB =
                type === 'movie' ? b.release_date :
                    type === 'tv' ? b.first_air_date :
                        '';

            return (dateB || '').localeCompare(dateA || '');
        });
    }

    /* =========================
       🖼 表示処理
    ========================= */

    function displayAllResults(movies, tvs, people) {
        movieResults.innerHTML = '';

        const categories = [movies, tvs, people];

        categories.forEach(category => {
            if (!category.results.length) return;

            const h2 = document.createElement('h2');
            h2.textContent =
                category.type === 'movie' ? '映画'
                    : category.type === 'tv' ? 'TV/ドラマ'
                        : 'キャスト/監督';

            movieResults.appendChild(h2);

            const sortedResults =
                category.type === 'person'
                    ? category.results
                    : sortByDateDesc(category.results, category.type);

            sortedResults.forEach(item => {
                const div = document.createElement('div');
                div.className = 'movie';

                const imgPath = item.poster_path || item.profile_path;
                const img = imgPath
                    ? `https://image.tmdb.org/t/p/w500${imgPath}`
                    : '/static/images/20220401_object.png';

                const title = item.title || item.name;
                const detail =
                    category.type === 'movie'
                        ? `公開日: ${item.release_date || '不明'}`
                        : category.type === 'tv'
                            ? `初回放送: ${item.first_air_date || '不明'}`
                            : `代表作: ${item.known_for?.[0]?.title || item.known_for?.[0]?.name || '不明'}`;

                div.innerHTML = `
                    <img src="${img}" width="120">
                    <h3>${title}</h3>
                    <p>${detail}</p>
                `;

                div.onclick = () => {
                    location.href = `/${category.type}/${item.id}/`;
                };

                movieResults.appendChild(div);
            });
        });
    }

});
