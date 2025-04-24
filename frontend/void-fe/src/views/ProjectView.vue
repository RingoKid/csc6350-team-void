<div class="project-content">
  <div class="project-description">
    <h3>Description</h3>
    <p>{{ project.description }}</p>
  </div>

  <div v-if="project.video_url" class="project-video">
    <h3>Project Video</h3>
    <div class="video-container">
      <iframe
        :src="getEmbeddedVideoUrl(project.video_url)"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
  </div>

  <div class="project-details">
    <!-- ... existing code ... -->
  </div>
</div>

<script setup>
// ... existing code ...

const getEmbeddedVideoUrl = (url) => {
  // Extract video ID from various YouTube URL formats
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  const videoId = (match && match[2].length === 11) ? match[2] : null;
  
  if (videoId) {
    return `https://www.youtube.com/embed/${videoId}`;
  }
  return url; // Fallback to original URL if not a valid YouTube URL
}

// ... existing code ...
</script>

<style scoped>
// ... existing code ...

.project-video {
  margin: 2rem 0;
}

.project-video h3 {
  color: #1f2937;
  margin-bottom: 1rem;
}

.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
  height: 0;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

// ... existing code ...
</style> 