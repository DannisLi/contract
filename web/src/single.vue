<template>
	<div>
		<div style="display:flex;">
			<Input v-model="vari" size="large" style="width:240px;">
				<span slot="prepend" style="width:100px;text-align:left;">品种：</span>
			</Input>
			<Input v-model="deli" size="large" style="width:240px;">
				<span slot="prepend" style="width:100px;text-align:left;">交割期：</span>
			</Input>
		</div>
		<br />
		<scatter field="settle" :vari="vari" :deli="deli"></scatter>
		<br />
		<scatter field="volume" :vari="vari" :deli="deli"></scatter>
		<br />
		<scatter field="oi" :vari="vari" :deli="deli"></scatter>
		<br />
	</div>
</template>
<script>
	import { Input } from 'iview';
	import scatter from './scatter.vue';
	
	export default {
		data () {
			return {
				vari: 'rb',
				deli: '1711'
			}
		},
		components: {
			Input,
			scatter,
		}
	}
</script>
