import { createApp } from 'vue'
import App from './App.vue'

// Import CSS files
import './assets/plugins/bootstrap/bootstrap.min.css'
import './assets/plugins/bootstrap/bootstrap-slider.css'
import './assets/plugins/font-awesome/css/font-awesome.min.css'
import './assets/plugins/slick/slick.css'
import './assets/plugins/slick/slick-theme.css'
import './assets/plugins/jquery-nice-select/css/nice-select.css'
import './assets/css/style.css'

// Create and mount the Vue app
const app = createApp(App)

app.mount('#app')

// Import JavaScript files (if necessary, or handle via components)
import './assets/plugins/jquery/jquery.min.js'
import './assets/plugins/bootstrap/popper.min.js'
import './assets/plugins/bootstrap/bootstrap.min.js'
import './assets/plugins/bootstrap/bootstrap-slider.js'
import './assets/plugins/tether/js/tether.min.js'
import './assets/plugins/raty/jquery.raty-fa.js'
import './assets/plugins/slick/slick.min.js'
import './assets/plugins/jquery-nice-select/js/jquery.nice-select.min.js'
import './assets/js/script.js'
