document.addEventListener('DOMContentLoaded', () => {
    const movieDetailDiv = document.getElementById('movieDetail');
    const urlParts = window.location.pathname.split('/').filter(Boolean);

    const type = urlParts[urlParts.length - 2]; // movie, tv, person
    const itemId = urlParts[urlParts.length - 1];

    const providerSearchUrls = {
        'netflix': title => `https://www.netflix.com/search?q=${encodeURIComponent(title)}`,
        'hulu': title => `https://www.hulu.jp/search?q=${encodeURIComponent(title)}`,
        'u-next': title => `https://video.unext.jp/search?query=${encodeURIComponent(title)}`,
        'amazon prime video': title => `https://www.amazon.co.jp/s?k=${encodeURIComponent(title)}&i=instant-video`,
        'disney plus': title => `https://www.disneyplus.com/ja-jp/search?q=${encodeURIComponent(title)}`,
        'apple tv plus': title => `https://tv.apple.com/jp/search/${encodeURIComponent(title)}`,
    };

    const placeholderImg = '/static/images/20220401_object.png'; // 代替画像

    /* ─────────────── 映画詳細表示 ─────────────── */
    function displayMovieDetail(detail, credits, providers) {
        if (!movieDetailDiv) return;

        const poster = detail.poster_path
            ? `https://image.tmdb.org/t/p/w500${detail.poster_path}`
            : placeholderImg;

        /* キャスト */
        const castHtml = credits.cast?.length
            ? `<div class="cast-list">
                ${credits.cast.slice(0, 10).map(actor => `
                    <a class="cast-card" href="/person/${actor.id}">
                        <img src="${actor.profile_path
                    ? `https://image.tmdb.org/t/p/w200${actor.profile_path}`
                    : placeholderImg}">
                        <div class="name">${actor.name}</div>
                        <div class="character">${actor.character}</div>
                    </a>
                `).join('')}
              </div>`
            : '<p>キャスト情報なし</p>';

        /* 配信サービス */
        const providerHtml = providers.results?.JP?.flatrate?.length
            ? `<div class="provider-list">
                ${providers.results.JP.flatrate.map(p => {
                const key = p.provider_name.toLowerCase();
                const url = providerSearchUrls[key] ? providerSearchUrls[key](detail.title) : '#';
                return `
                        <a class="provider-card" href="${url}" target="_blank">
                            <img src="${p.logo_path ? 'https://image.tmdb.org/t/p/original' + p.logo_path : placeholderImg}">
                        </a>`;
            }).join('')}
              </div>`
            : '<p>配信情報なし</p>';

        /* シリーズ */
        const seriesHtml = detail.belongs_to_collection
            ? `<section class="movie-section">
                <h2>シリーズ</h2>
                <a class="series-card" href="/collection/${detail.belongs_to_collection.id}/">
                    <img src="${detail.belongs_to_collection.poster_path
                ? `https://image.tmdb.org/t/p/w300${detail.belongs_to_collection.poster_path}`
                : placeholderImg}">
                    <div class="series-name">${detail.belongs_to_collection.name}</div>
                </a>
            </section>`
            : '';

        /* 評価 */
        const ratingHtml = `<p><strong>評価:</strong> ⭐ ${detail.vote_average?.toFixed(1) ?? 'N/A'} 
            <span style="color:#888;">(${detail.vote_count || 0}件)</span></p>`;

        /* HTML出力 */
        movieDetailDiv.innerHTML = `
            <img class="poster" src="${poster}">
            <div class="info">
                <h1>${detail.title || 'タイトル不明'}</h1>
                <p><strong>原題:</strong> ${detail.original_title || '不明'}</p>
                <p><strong>公開日:</strong> ${detail.release_date || '不明'}</p>
                <p><strong>上映時間:</strong> ${detail.runtime ? detail.runtime + '分' : '不明'}</p>
                ${ratingHtml}
                <p><strong>あらすじ:</strong> ${detail.overview || 'なし'}</p>
                ${seriesHtml}
                <section class="movie-section">
                    <h2>キャスト</h2>
                    ${castHtml}
                </section>
                <section class="movie-section">
                    <h2>サブスク配信</h2>
                    ${providerHtml}
                </section>
                <p class="back-link"><a href="javascript:history.back()">← 一覧に戻る</a></p>
            </div>
        `;
    }

    /* ─────────────── 映画取得 ─────────────── */
    async function fetchMovieDetail(id) {
        if (!movieDetailDiv) return;
        movieDetailDiv.innerHTML = "<p>読み込み中…</p>";

        try {
            const res = await fetch(`/api/movie/${id}/`);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

            const data = await res.json();
            if (data.error) throw new Error(data.error);

            displayMovieDetail(data.detail, data.credits, data.providers);
        } catch (error) {
            console.error('Movie detail error:', error);
            movieDetailDiv.innerHTML = '<p>映画情報の取得に失敗しました。</p>';
        }
    }

    /* ─────────────── TV詳細表示 ─────────────── */
    function displayTvDetail(detail, credits, providers) {
        const poster = detail.poster_path
            ? `https://image.tmdb.org/t/p/w500${detail.poster_path}`
            : placeholderImg;

        const castHtml = credits.cast?.length
            ? `<div class="cast-list">
                ${credits.cast.slice(0, 10).map(actor => `
                    <a class="cast-card" href="/person/${actor.id}">
                        <img src="${actor.profile_path
                    ? `https://image.tmdb.org/t/p/w200${actor.profile_path}`
                    : placeholderImg}">
                        <div class="name">${actor.name}</div>
                        <div class="character">${actor.character}</div>
                    </a>
                `).join('')}
           </div>`
            : 'なし';

        const providerHtml = providers.results?.JP?.flatrate?.length
            ? `<div class="provider-list">
                ${providers.results.JP.flatrate.map(p => {
                const key = p.provider_name.toLowerCase();
                const url = providerSearchUrls[key] ? providerSearchUrls[key](detail.name) : '#';
                return `
                        <a class="provider-card" href="${url}" target="_blank">
                            <img src="${p.logo_path ? 'https://image.tmdb.org/t/p/original' + p.logo_path : placeholderImg}">
                        </a>`;
            }).join('')}
               </div>`
            : 'なし';

        movieDetailDiv.innerHTML = `
            <img class="poster" src="${poster}">
            <div class="info">
                <h1>${detail.name}</h1>
                <p><strong>原題:</strong> ${detail.original_name}</p>
                <p><strong>初回放送:</strong> ${detail.first_air_date || '不明'}</p>
                <p><strong>シーズン数:</strong> ${detail.number_of_seasons}</p>
                <p><strong>エピソード数:</strong> ${detail.number_of_episodes}</p>
                <p><strong>平均評価:</strong> ⭐ ${detail.vote_average}</p>
                <p><strong>あらすじ:</strong><br>${detail.overview || 'なし'}</p>
                <section class="movie-section">
                    <h2>キャスト</h2>
                    ${castHtml}
                </section>
                <section class="movie-section">
                    <h2>サブスク配信</h2>
                    ${providerHtml}
                </section>
                <p class="back-link"><a href="javascript:history.back()">← 一覧に戻る</a></p>
            </div>
        `;
    }

    async function fetchTvDetail(id) {
        try {
            const res = await fetch(`/api/tv/${id}/`);
            const data = await res.json();
            displayTvDetail(data.detail, data.credits, data.providers);
        } catch (error) {
            movieDetailDiv.innerHTML = '<p>ドラマ情報の取得に失敗しました。</p>';
        }
    }

    /* Person 詳細 */
    async function fetchPersonDetail(id) {
        try {
            const res = await fetch(`/api/person/${id}/`);
            const data = await res.json();
            displayPersonDetail(data.detail, data.credits);
        } catch (error) {
            movieDetailDiv.innerHTML = '<p>人物情報の取得に失敗しました。</p>';
        }
    }

    /* 最後に振り分け */
    if (type === 'movie') {
        fetchMovieDetail(itemId);
    } else if (type === 'tv') {
        fetchTvDetail(itemId);
    } else if (type === 'person') {
        fetchPersonDetail(itemId);
    }
});
