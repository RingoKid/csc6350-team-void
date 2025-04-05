<template>
  <div class="blog-container">
    <h1>Blog</h1>
    <p>Welcome to the blog page. Here you will find the latest articles and updates.</p>
    <div v-for="(post, index) in blogPosts" :key="index" class="blog-post">
      <h2>{{ post.title }}</h2>
      <p><strong>By:</strong> {{ post.author }} | <strong>Date:</strong> {{ post.date }}</p>
      <p>{{ post.content }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Blog",
  data() {
    return {
      blogPosts: [
        {
          title: "First Blog Post",
          author: "Author 1",
          date: "2023-10-01",
          content: "This is the content of the first blog post."
        },
        {
          title: "Second Blog Post",
          author: "Author 2",
          date: "2023-10-02",
          content: "This is the content of the second blog post."
        }
      ]
    };
  }
};
</script>

<style scoped>
.blog-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.blog-container h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.blog-container p {
  font-size: 1.2rem;
  color: #555;
}

.blog-post {
  margin-bottom: 40px;
  text-align: left;
}

.blog-post h2 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.blog-post p {
  font-size: 1rem;
  color: #333;
}
</style>
