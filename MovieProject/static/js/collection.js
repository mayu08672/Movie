/* ────────────────────────────
    🎬 シリーズ（コレクション）詳細を取得
──────────────────────────── */

async function fetchCollectionDetail(id) {
    const collectionDiv = document.getElementById("collectionDetail");
    collectionDiv.innerHTML = "<p>読み込み中…</p>";

    try {
        const res = await fetch(`/api/collection/${id}/`, {
            method: "GET",
            headers: { "Accept": "application/json" }
        });

        // ❗ HTTP ステータスでエラー判定
        if (!res.ok) {
            console.error("HTTP Error:", res.status);
            collectionDiv.innerHTML = "<p>シリーズ情報の取得に失敗しました。（HTTPエラー）</p>";
            return;
        }

        const data = await res.json();

        // ❗ Django からの JSON エラー
        if (data.error) {
            console.error("API Error:", data.error);
            collectionDiv.innerHTML = "<p>シリーズ情報の取得に失敗しました。（APIエラー）</p>";
            return;
        }

        displayCollectionDetail(data.detail);

    } catch (err) {
        console.error("Collection detail error:", err);
        collectionDiv.innerHTML = "<p>シリーズ情報の取得に失敗しました。（例外発生）</p>";
    }
}


/* ────────────────────────────
    🎬 シリーズ情報の表示
──────────────────────────── */

function displayCollectionDetail(detail) {
    const collectionDiv = document.getElementById("collectionDetail");

    if (!detail) {
        collectionDiv.innerHTML = "<p>シリーズ情報がありません。</p>";
        return;
    }

    const poster = detail.poster_path
        ? `https://image.tmdb.org/t/p/w500${detail.poster_path}`
        : "https://via.placeholder.com/300x450?text=No+Image";

    const parts = detail.parts || [];

    const partsHtml = parts.length
        ? `
        <div class="movie-list">
            ${parts
            .map(
                (movie) => `
                <a class="movie-card" href="/movie/${movie.id}/">
                    <img src="${movie.poster_path
                        ? `https://image.tmdb.org/t/p/w300${movie.poster_path}`
                        : "https://via.placeholder.com/200x300?text=No+Image"
                    }">
                    <div class="title">${movie.title}</div>
                </a>
            `
            )
            .join("")}
        </div>`
        : "<p>シリーズに登録された作品はありません。</p>";

    collectionDiv.innerHTML = `
        <img class="poster" src="${poster}">
        <div class="info">
            <h1>${detail.name || "シリーズ名不明"}</h1>

            <p><strong>概要:</strong> ${detail.overview || "なし"}</p>

            <section class="movie-section">
                <h2>シリーズ作品一覧</h2>
                ${partsHtml}
            </section>

            <p class="back-link">
                <a href="javascript:history.back()">← 戻る</a>
            </p>
        </div>
    `;
}
