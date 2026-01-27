document.addEventListener("DOMContentLoaded", async () => {

    const MOVIE_URL = "/movie_detail/";
    const TV_URL = "/tv_detail/";

    const personId = location.pathname.split('/').filter(Boolean).pop();

    const response = await fetch(`/api/person/${personId}/credits/`);
    const credits = await response.json();


    const worksContainer = document.getElementById("worksContainer");

    worksContainer.innerHTML = "読み込み中…";

    try {

        const response = await fetch(
            `https://api.themoviedb.org/3/person/${personId}/combined_credits?api_key=${API_KEY}&language=ja-JP`
        );

        const credits = await response.json();

        worksContainer.innerHTML = "";

        if (!credits.cast || credits.cast.length === 0) {
            worksContainer.innerHTML = "<p>出演作がありません。</p>";
            return;
        }

        const sortedWorks = credits.cast.sort((a, b) => {
            const dateA = a.release_date || a.first_air_date || "";
            const dateB = b.release_date || b.first_air_date || "";
            return dateB.localeCompare(dateA);
        });

        sortedWorks.forEach(work => {

            const img = work.poster_path
                ? `https://image.tmdb.org/t/p/w200${work.poster_path}`
                : "/static/noimage.png";

            const title = work.title || work.name || "タイトル不明";

            const date =
                work.media_type === "movie"
                    ? work.release_date
                    : work.first_air_date;

            const displayDate = date || "不明";

            const dateLabel =
                work.media_type === "movie" ? "公開日" : "放送開始日";

            const detailUrl =
                work.media_type === "movie"
                    ? `${MOVIE_URL}${work.id}/`
                    : `${TV_URL}${work.id}/`;

            const div = document.createElement("div");
            div.className = "work-card";

            div.innerHTML = `
                <div class="work-card-inner">
                    <img src="${img}">
                    <div class="work-info">
                        <p class="work-title">${title}</p>
                        <p class="work-date">${dateLabel}：${displayDate}</p>
                    </div>
                </div>
            `;

            div.addEventListener("click", () => {
                console.log("作品詳細URL →", detailUrl);
                window.location.href = detailUrl;
            });

            worksContainer.appendChild(div);
        });

    } catch (error) {

        console.error(error);
        worksContainer.innerHTML = "<p>データ取得に失敗しました。</p>";

    }

});


