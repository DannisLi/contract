<template>
	<div id="3D" style="width:1500px;height:800px;margin:0 auto;"></div>
</template>
<script>
	import echarts from 'echarts';
	import $ from 'jquery';
	require('echarts-gl');
	
	function round (x, p) {
		var tmp = Math.pow(10,p);
		return Math.round(x*tmp) / tmp;
	}
	
	export default {
		data () {
			return {
				chart: null,
				option: {
					animation: false,
					title: {
						text: '(beta0, beta1, R2)',
					},
					tooltip: {
						trigger: 'item',
						formatter: function (obj) {
							return obj.value[3] + '  ' + obj.value[4];
						}
					},
					grid3D: {
						show: true,
					},
					xAxis3D: {
						show: true,
						name: 'beta0',
						type: 'value',
					},
					yAxis3D: {
						show: true,
						name: 'beta1',
						type: 'value',
					},
					zAxis3D: {
						show: true,
						name: 'R2',
						type: 'value',
					},
					series: [{
						type: 'scatter3D',
						coordinateSystem: 'cartesian3D',
						data: null,
						label: {
							show: false,
						},
						emphasis: {
							label: {
								show: false,
							},
						},
					}],
				},
			}
		},
		methods: {
			draw () {
				var opt = this.option;
				var chart = this.chart;
				opt.series[0].data = new Array();
				
				$.get('http://127.0.0.1:8888/multi_diff/', function (data) {
					data = JSON.parse(data);
					for (var i=0; i<data.length; i++) {
						var row = data[i];
						var beta0 = round(row.beta0, 3);
						var beta1 = round(row.beta1, 3);
						var R2 = round(row.R2, 3);
						opt.series[0].data.push([beta0, beta1, R2, row.vari, row.deli]);
					}
					chart.setOption(opt);
				});
			}
		},
		mounted () {
			this.chart = echarts.init(document.getElementById('3D'));
			this.draw();
		},
	}
</script>