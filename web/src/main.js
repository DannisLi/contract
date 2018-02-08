import Vue from 'vue'
import 'iview/dist/styles/iview.css'
import single from './single.vue'
import multiple from './multiple.vue';

var routes = {
	'/single': single,
	'/multiple': multiple,
}

new Vue({
	el: '#app',
	data: {
		currentRoute: window.location.pathname
	},
	computed: {
		ViewComponent () {
		return routes[this.currentRoute]
		}
	},
	render (h) {
		return h(this.ViewComponent)
	}
})
