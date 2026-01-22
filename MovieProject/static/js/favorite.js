// 例：お気に入り追加
fetch('/favorites/add/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ movie_id: 550, favorite: true })
})
    .then(res => res.json())
    .then(data => console.log(data));
