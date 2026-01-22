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
        'dtv': title => `https://video.dmkt-sp.jp/search?keyword=${encodeURIComponent(title)}`
    };

    /* ───────────────
       🎬 Django 経由で映画詳細を取得
    ─────────────── */
    async function fetchMovieDetail(id) {
        try {
            const res = await fetch(`/api/movie/${id}/`);
            const data = await res.json();  // Django がまとめて返す JSON

            displayMovieDetail(data.detail, data.credits, data.providers);

        } catch (error) {
            console.error('Movie detail error:', error);
            movieDetailDiv.innerHTML = '<p>映画情報の取得に失敗しました。</p>';
        }
    }

    function displayMovieDetail(detail, credits, providers) {
        const poster = detail.poster_path
            ? `https://image.tmdb.org/t/p/w500${detail.poster_path}`
            : 'https://via.placeholder.com/300x450?text=No+Image';

        const castHtml = credits.cast?.length
            ? `<div class="cast-list">
                ${credits.cast.slice(0, 10).map(actor => `
                    <a class="cast-card" href="/person/${actor.id}">
                        <img src="${actor.profile_path
                    ? `https://image.tmdb.org/t/p/w200${actor.profile_path}`
                    : 'https://via.placeholder.com/100x140?text=No+Image'}">
                        <div class="name">${actor.name}</div>
                        <div class="character">${actor.character}</div>
                    </a>
                `).join('')}
               </div>`
            : 'なし';

        const providerHtml =
            providers.results?.JP?.flatrate?.length
                ? `<div class="provider-list">
                    ${providers.results.JP.flatrate.map(p => {
                    const key = p.provider_name.toLowerCase();
                    const url = providerSearchUrls[key]
                        ? providerSearchUrls[key](detail.title)
                        : '#';
                    return `
                        <a class="provider-card" href="${url}" target="_blank">
                            <img src="https://image.tmdb.org/t/p/original${p.logo_path}">
                        </a>`;
                }).join('')}
                   </div>`
                : 'なし';

        movieDetailDiv.innerHTML = `
            <img class="poster" src="${poster}">
            <div class="info">
                <h1>${detail.title}</h1>
                <p><strong>公開日:</strong> ${detail.release_date || '不明'}</p>
                <p><strong>あらすじ:</strong> ${detail.overview || 'なし'}</p>

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

    /* TV 用 */
    async function fetchTvDetail(id) {
        try {
            const res = await fetch(`/api/tv/${id}/`);
            const data = await res.json();

            displayTvDetail(data.detail, data.credits, data.providers);

        } catch (error) {
            movieDetailDiv.innerHTML = '<p>ドラマ情報の取得に失敗しました。</p>';
        }
    }

    /* Person 用 */
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
