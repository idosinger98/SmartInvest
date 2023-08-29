

for(const post of posts_images){
    const postHtml = document.getElementById("post-" + post['id'] + "-img");
    if(Object.keys(post['stock_image']).length !== 0) {         // for cases that the post is old test data
        const postImage = JSON.parse(post['stock_image']);
        if ('image' in postImage && postImage['image'] !== '') {
            postHtml.src = postImage['image'];
        }
    }
}
